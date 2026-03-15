import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# load data
df = pd.read_csv("transactions.csv")

# create directed graph
G = nx.DiGraph()

for _, row in df.iterrows():
    sender = row["sender"]
    receiver = row["receiver"]
    fraud = row["fraud_flag"]

    color = "red" if fraud == 1 else "blue"

    G.add_edge(sender, receiver, color=color)

# edge colors
edge_colors = [G[u][v]['color'] for u,v in G.edges()]

plt.figure(figsize=(12,8))
pos = nx.spring_layout(G)

nx.draw(
    G, pos,
    with_labels=True,
    node_size=700,
    node_color="lightblue",
    edge_color=edge_colors,
    arrows=True
)

plt.title("Transaction Network Graph")
plt.show()
