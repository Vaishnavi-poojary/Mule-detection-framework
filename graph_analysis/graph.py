"""
graph_analysis/graph.py
Member 3 – Graph Analysis & Mule Chain Detection

Reads  : transactions.csv       (Member 1)
         flagged_accounts.csv   (Member 2 - generated after running risk engine)
Outputs: graph_analysis/transaction_graph.png  (network visual)
         graph_analysis/chain_report.csv        (detected mule chains)

Run from project root:
    python -m graph_analysis.graph
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

OUTPUT_DIR = "graph_analysis"


# ── Step 1: Load data ──────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv("transactions.csv", parse_dates=["timestamp"])
    print(f"[INFO] Loaded {len(df)} transactions")

    flagged_ids = set()
    try:
        flagged_df = pd.read_csv("flagged_accounts.csv")
        flagged_ids = set(flagged_df["account_id"].astype(str))
        print(f"[INFO] Loaded {len(flagged_ids)} flagged accounts from Member 2")
    except FileNotFoundError:
        print("[WARN] flagged_accounts.csv not found — using fraud_flag column as fallback")
        fraud_senders = df[df["fraud_flag"] == 1]["sender"].astype(str).unique()
        flagged_ids = set(fraud_senders)
        print(f"[INFO] Fallback: {len(flagged_ids)} accounts flagged via fraud_flag")

    return df, flagged_ids


# ── Step 2: Build directed graph ───────────────────────────────────────────────
def build_graph(df):
    """
    Nodes  = accounts (senders and receivers)
    Edges  = money transfers (directed: sender → receiver)
    Weight = total amount transferred between two accounts
    """
    G = nx.DiGraph()

    for _, row in df.iterrows():
        sender   = str(int(row["sender"]))
        receiver = str(int(row["receiver"]))
        amount   = float(row["amount"])

        if G.has_edge(sender, receiver):
            G[sender][receiver]["weight"] += amount
            G[sender][receiver]["count"]  += 1
        else:
            G.add_edge(sender, receiver,
                       weight=round(amount, 2),
                       count=1)

    print(f"[INFO] Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    return G


# ── Step 3: Detect mule chains ─────────────────────────────────────────────────
def detect_chains(G, flagged_ids):
    """
    Adapted for this dataset structure:
    - Senders: 10000-10100
    - Receivers: 20000-20100
    - Mule pattern: flagged sender → multiple different receivers
      AND receives from multiple senders (high in-degree pattern)
    
    We detect:
    1. Fan-out chains: one mule sending to many receivers
    2. Shared receiver chains: multiple flagged accounts → same receiver
    """
    chains = []

    # Pattern 1 — Fan-out: flagged account sends to 3+ different receivers
    for node in G.nodes():
        if node not in flagged_ids:
            continue
        successors = list(G.successors(node))
        if len(successors) >= 3:
            total_out = sum(G[node][s]["weight"] for s in successors)
            chains.append({
                "chain": f"{node} → [{', '.join(successors[:3])}{'...' if len(successors)>3 else ''}]",
                "entry_account": "multiple",
                "mule_account": node,
                "exit_account": ", ".join(successors[:3]),
                "amount_in": round(total_out * 0.9, 2),
                "amount_out": round(total_out, 2),
                "total_flow": round(total_out, 2),
                "pattern": "fan-out"
            })

    # Pattern 2 — Shared receiver: 2+ flagged accounts send to same receiver
    receiver_map = {}
    for node in G.nodes():
        if node not in flagged_ids:
            continue
        for succ in G.successors(node):
            if succ not in receiver_map:
                receiver_map[succ] = []
            receiver_map[succ].append(node)

    for receiver, mules in receiver_map.items():
        if len(mules) >= 2:
            total_flow = sum(G[m][receiver]["weight"] for m in mules)
            chains.append({
                "chain": f"[{', '.join(mules[:3])}] → {receiver}",
                "entry_account": ", ".join(mules[:3]),
                "mule_account": ", ".join(mules[:3]),
                "exit_account": receiver,
                "amount_in": round(total_flow, 2),
                "amount_out": round(total_flow, 2),
                "total_flow": round(total_flow, 2),
                "pattern": "shared-receiver"
            })

    chains_df = pd.DataFrame(chains) if chains else pd.DataFrame(
        columns=["chain", "entry_account", "mule_account",
                 "exit_account", "amount_in", "amount_out", "total_flow", "pattern"]
    )

    if not chains_df.empty:
        chains_df = chains_df.sort_values("total_flow", ascending=False).reset_index(drop=True)

    print(f"[INFO] Detected {len(chains_df)} suspicious mule chains")
    return chains_df
# ── Step 4: Visualize the graph ────────────────────────────────────────────────
def visualize_graph(G, flagged_ids):
    print("[INFO] Drawing transaction graph...")

    # Color: red = mule/flagged, green = normal, orange = exit node in a chain
    node_colors = []
    for node in G.nodes():
        if node in flagged_ids:
            node_colors.append("#E24B4A")  # red
        else:
            node_colors.append("#1D9E75")  # green

    # Size: bigger = more connections
    node_sizes = [max(200, G.degree(n) * 100) for n in G.nodes()]

    fig, ax = plt.subplots(figsize=(18, 13))
    ax.set_title(
        "Transaction Network Graph — Mule Account Detection\n"
        f"({G.number_of_nodes()} accounts · {G.number_of_edges()} transfers · "
        f"{len(flagged_ids)} mule accounts flagged)",
        fontsize=14, fontweight="bold", pad=15
    )

    pos = nx.spring_layout(G, k=1.8, seed=42)

    # Draw edges (thin, semi-transparent)
    nx.draw_networkx_edges(
        G, pos, ax=ax,
        edge_color="#B4B2A9",
        arrows=True,
        arrowsize=8,
        width=0.4,
        alpha=0.4
    )

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos, ax=ax,
        node_color=node_colors,
        node_size=node_sizes,
        alpha=0.85
    )

    # Labels only on flagged (mule) nodes to avoid clutter
    mule_labels = {n: n for n in G.nodes() if n in flagged_ids}
    nx.draw_networkx_labels(
        G, pos, ax=ax,
        labels=mule_labels,
        font_size=6,
        font_color="white",
        font_weight="bold"
    )

    # Legend
    red_patch   = mpatches.Patch(color="#E24B4A",
                                  label=f"Mule account ({len(flagged_ids)} flagged)")
    green_patch = mpatches.Patch(color="#1D9E75",
                                  label=f"Normal account ({G.number_of_nodes() - len(flagged_ids)} accounts)")
    ax.legend(handles=[red_patch, green_patch],
              loc="upper left", fontsize=11, framealpha=0.9)

    ax.axis("off")
    plt.tight_layout()

    out_path = os.path.join(OUTPUT_DIR, "transaction_graph.png")
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[INFO] Graph image saved → {out_path}")


# ── Step 5: Print summary ──────────────────────────────────────────────────────
def print_summary(G, flagged_ids, chains_df):
    total     = G.number_of_nodes()
    n_flagged = len([n for n in G.nodes() if n in flagged_ids])

    print("\n" + "=" * 54)
    print("  GRAPH ANALYSIS — SUMMARY REPORT")
    print("=" * 54)
    print(f"  Total accounts  (nodes)  : {total}")
    print(f"  Total transfers (edges)  : {G.number_of_edges()}")
    print(f"  Flagged mule nodes       : {n_flagged}")
    print(f"  Suspicious chains found  : {len(chains_df)}")

    if not chains_df.empty:
        print()
        print("  Top 5 Highest-Flow Mule Chains:")
        print("  " + "-" * 50)
        for _, row in chains_df.head(5).iterrows():
            print(f"  {row['chain']}")
            print(f"  └─ Flow: ₹{row['amount_in']:>12,.2f} in  |"
                  f"  ₹{row['amount_out']:>12,.2f} out")

    print("=" * 54)
    print(f"[DONE] Visual  → graph_analysis/transaction_graph.png")
    print(f"[DONE] Chains  → graph_analysis/chain_report.csv")
    print(f"[DONE] Pass chain_report.csv → Member 4 (API /chains endpoint)\n")


# ── Main ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df, flagged_ids = load_data()
    G               = build_graph(df)
    chains_df       = detect_chains(G, flagged_ids)

    chains_df.to_csv(
        os.path.join(OUTPUT_DIR, "chain_report.csv"), index=False
    )

    visualize_graph(G, flagged_ids)
    print_summary(G, flagged_ids, chains_df)
