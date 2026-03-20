"""
risk_engine/scoring.py
Member 2 – Risk Scoring Engine (Main Entry Point)

How to run:
    python -m risk_engine.scoring
    (from the root of the project, not inside risk_engine/)

Reads  : transactions.csv  (Member 1's output)
Writes : flagged_accounts.csv  (for Member 4 API)
         all_accounts.csv      (for Member 3 graph)
"""

import pandas as pd
import json
import sys
import os

# ── Load config ────────────────────────────────────────────────────────────────
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH) as f:
    CONFIG = json.load(f)

T = CONFIG["thresholds"]   # threshold values
S = CONFIG["scores"]       # score points per rule

# ── Rules (imported from rules.py in same folder) ─────────────────────────────
from risk_engine.rules import RULES


# ── Step 1: Load transactions ─────────────────────────────────────────────────
def load_transactions(path="transactions.csv"):
    df = pd.read_csv(path, parse_dates=["timestamp"])
    print(f"[INFO] Loaded {len(df)} transactions.")
    return df


# ── Step 2: Build per-account features ───────────────────────────────────────
def build_account_features(df):
    features = []
    all_senders = df["sender"].unique()

    for account in all_senders:
        sent = df[df["sender"] == account]
        received = df[df["receiver"] == account]

        tx_count = len(sent)
        if tx_count == 0:
            continue

        min_age = int(sent["account_age_days"].min())

        if tx_count > 1:
            span_hours = (
                sent["timestamp"].max() - sent["timestamp"].min()
            ).total_seconds() / 3600
            tx_per_hour = round(tx_count / max(span_hours, 1), 2)
        else:
            tx_per_hour = 1.0

        high_ratio = round((sent["amount"] > T["high_amount"]).mean(), 2)
        unique_recv = int(received["sender"].nunique())

        quick_fwd = 0
        window = pd.Timedelta(minutes=T["quick_forward_minutes"])
        for recv_time in received["timestamp"]:
            if not sent[
                (sent["timestamp"] >= recv_time) &
                (sent["timestamp"] <= recv_time + window)
            ].empty:
                quick_fwd = 1
                break

        avg_amount = round(float(sent["amount"].mean()), 2)

        # ── NEW: fraud_ratio from Member 1's own fraud_flag column ──
        fraud_ratio = round(float(sent["fraud_flag"].mean()), 2) \
                      if "fraud_flag" in sent.columns else 0.0

        features.append({
            "account_id": account,
            "min_account_age_days": min_age,
            "tx_count": tx_count,
            "tx_per_hour": tx_per_hour,
            "high_amount_ratio": high_ratio,
            "unique_senders_recv": unique_recv,
            "quick_forward_flag": quick_fwd,
            "avg_amount": avg_amount,
            "fraud_ratio": fraud_ratio,       # NEW
        })

    feature_df = pd.DataFrame(features)
    print(f"[INFO] Built features for {len(feature_df)} accounts.")
    return feature_df

# ── Step 3: Apply risk rules and compute score ────────────────────────────────
def score_account(row):
    """Returns (total_score, reasons_string) for one account row."""
    total = 0
    reasons = []
    for rule in RULES:
        if rule["check"](row):
            total += rule["score"]
            reasons.append(rule["reason"])
    return min(total, 100), "; ".join(reasons) if reasons else "Clean"


def apply_scoring(feature_df):
    scored = feature_df.copy()
    results = scored.apply(
        lambda r: pd.Series(score_account(r), index=["risk_score", "risk_reasons"]),
        axis=1
    )
    scored = pd.concat([scored, results], axis=1)
    scored["is_mule"] = (scored["risk_score"] > T["mule_flag_score"]).astype(int)
    return scored


# ── Step 4: Save outputs ──────────────────────────────────────────────────────
def save_outputs(scored_df, output_dir="."):
    all_path = os.path.join(output_dir, "all_accounts.csv")
    flagged_path = os.path.join(output_dir, "flagged_accounts.csv")

    scored_df.to_csv(all_path, index=False)
    print(f"[INFO] Saved {all_path} ({len(scored_df)} accounts)")

    flagged = scored_df[scored_df["is_mule"] == 1].sort_values(
        "risk_score", ascending=False
    )
    flagged.to_csv(flagged_path, index=False)
    print(f"[INFO] Saved {flagged_path} ({len(flagged)} flagged accounts)")
    return flagged


# ── Step 5: Print summary ─────────────────────────────────────────────────────
def print_report(scored_df, flagged):
    total = len(scored_df)
    n_flagged = len(flagged)
    print("\n" + "=" * 52)
    print("  MULE ACCOUNT RISK SCORING — SUMMARY")
    print("=" * 52)
    print(f"  Total accounts analysed : {total}")
    print(f"  Flagged as mule (>{T['mule_flag_score']}) : {n_flagged}")
    print(f"  Detection rate          : {round(n_flagged/total*100, 1)}%")
    print()

    bins   = [0, 20, 40, 60, 70, 80, 100]
    labels = ["0-20", "21-40", "41-60", "61-70", "71-80", "81-100"]
    scored_df = scored_df.copy()
    scored_df["band"] = pd.cut(scored_df["risk_score"], bins=bins, labels=labels)
    print("  Score Distribution:")
    for band, count in scored_df["band"].value_counts().sort_index().items():
        bar = "█" * max(1, count // max(1, total // 30))
        print(f"    {band:8s} | {bar} {count}")

    print()
    print("  Top 10 Riskiest Accounts:")
    print("  " + "-" * 48)
    for _, r in flagged.head(10).iterrows():
        print(f"  Acc {r['account_id']:>6} | Score {r['risk_score']:>3} | {r['risk_reasons']}")
    print("=" * 52)
    print("[DONE] Pass flagged_accounts.csv → Member 3 (graph) & Member 4 (API)\n")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tx_path = sys.argv[1] if len(sys.argv) > 1 else "transactions.csv"
    df        = load_transactions(tx_path)
    features  = build_account_features(df)
    scored    = apply_scoring(features)
    flagged   = save_outputs(scored)
    print_report(scored, flagged)
