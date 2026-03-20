import pandas as pd

df = pd.read_csv("transactions.csv")

total = len(df)
fraud_count = df["fraud_flag"].sum()

print("Total rows:", total)
print("Fraud count:", fraud_count)
print("Fraud percentage:", (fraud_count / total) * 100)