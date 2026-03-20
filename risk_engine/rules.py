# rules.py
import json

with open("risk_engine/config.json") as f:
    CONFIG = json.load(f)

T = CONFIG["thresholds"]
S = CONFIG["scores"]


RULES = [
    {
        "name": "new_account",
        "check": lambda row: row["min_account_age_days"] < T["account_age_days"],
        "score": S["new_account"],
        "reason": "New account (<30 days)"
    },
    {
        "name": "high_tx_rate",
        "check": lambda row: row["tx_per_hour"] > T["tx_per_hour"],
        "score": S["high_tx_rate"],
        "reason": "High transaction rate"
    },
    {
        "name": "quick_forward",
        "check": lambda row: row["quick_forward_flag"] == 1,
        "score": S["quick_forward"],
        "reason": "Quick forward after receiving"
    },
    {
        "name": "many_senders",
        "check": lambda row: row["unique_senders_recv"] > T["unique_senders"],
        "score": S["many_senders"],
        "reason": "Many unique senders"
    },
    {
        "name": "high_amount_ratio",
        "check": lambda row: row["high_amount_ratio"] > T["high_amount_ratio"],
        "score": S["high_amount_ratio"],
        "reason": "Majority high-value transactions"
    },
    {
        "name": "fraud_ratio",
        "check": lambda row: row.get("fraud_ratio", 0) > T["fraud_ratio"],
        "score": S["fraud_ratio"],
        "reason": "High fraud transaction ratio"
    },
]
