import pandas as pd
from risk_engine.scoring import calculate_risk_score

# Load the dataset

data = pd.read_csv("transactions.csv")

# Test first 5 transactions

for index, row in data.head(5).iterrows():
transaction = row.to_dict()

```
score = calculate_risk_score(transaction)

print("Transaction ID:", transaction.get("transaction_id"))
print("Risk Score:", score)
print("----------------------")
```

