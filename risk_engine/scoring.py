import pandas as pd
from rules import amount_risk, channel_risk, rapid_activity

# Load dataset
data = pd.read_csv("transactions.csv")

# Convert timestamp to datetime
data["timestamp"] = pd.to_datetime(data["timestamp"])

# Sort transactions by sender and time
data = data.sort_values(["sender", "timestamp"])

# Calculate time difference between transactions for same sender
data["time_diff"] = data.groupby("sender")["timestamp"].diff().dt.total_seconds()

# Replace NaN values
data.fillna(0, inplace=True)

# Count transactions per sender
txn_count = data.groupby("sender").size()


# -------- Main Risk Calculation -------- #

def calculate_risk(row):

    score = 0

    # Rule 1: New account
    if row["account_age_days"] < 30:
        score += 20

    # Rule 2: Large amount transfer
    score += amount_risk(row["amount"])

    # Rule 3: Fast payment channel
    score += channel_risk(row["transaction_type"])

    # Rule 4: Rapid transactions
    score += rapid_activity(row["time_diff"])

    # Rule 5: Many transactions by same sender
    if txn_count[row["sender"]] > 5:
        score += 25

    return score


# Apply risk scoring
data["risk_score"] = data.apply(calculate_risk, axis=1)

# Flag suspicious transactions
data["flagged"] = data["risk_score"] > 40


# -------- Account Level Risk -------- #

account_risk = data.groupby("sender")["risk_score"].sum().reset_index()

account_risk.rename(columns={"risk_score": "total_risk"}, inplace=True)

# Flag mule accounts
account_risk["is_mule"] = account_risk["total_risk"] > 70

print("\nAccount Risk Scores:")
print(account_risk)

account_risk.to_csv("account_risk_scores.csv", index=False)


# Extract suspicious transactions
flagged_accounts = data[data["flagged"] == True]

print("\nSuspicious Transactions:")
print(flagged_accounts.head())

flagged_accounts.to_csv("flagged_accounts.csv", index=False)