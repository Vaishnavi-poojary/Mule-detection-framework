import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def load_data(file_name="featured_transactions.csv"):
    df = pd.read_csv(file_name)
    return df


def build_graph(df):

    G = nx.DiGraph()

    for _, row in df.iterrows():
        sender = row["sender"]
        receiver = row["receiver"]
        amount = row["amount"]

        G.add_edge(sender, receiver, amount=amount)

    return G


def detect_suspicious_accounts(G, threshold=10):

    suspicious = []

    degree_dict = dict(G.degree())

    for node, degree in degree_dict.items():
        if degree > threshold:
            suspicious.append(node)

    return suspicious


def visualize_graph(G, suspicious_nodes):

    plt.figure(figsize=(12, 8))

    pos = nx.spring_layout(G, seed=42)

    node_colors = []

    for node in G.nodes():
        if node in suspicious_nodes:
            node_colors.append("red")
        else:
            node_colors.append("skyblue")

    nx.draw(
        G,
        pos,
        node_color=node_colors,
        node_size=60,
        edge_color="gray",
        with_labels=False
    )

    plt.title("Transaction Network Graph")
    plt.show()


def main():

    print("Loading dataset...")
    df = load_data()

    print("Building graph...")
    G = build_graph(df)

    print("Detecting suspicious accounts...")
    suspicious_nodes = detect_suspicious_accounts(G)

    print("\nSuspicious Accounts:")
    print(suspicious_nodes)

    print("\nDrawing graph...")
    visualize_graph(G, suspicious_nodes)


if __name__ == "__main__":
    main()
