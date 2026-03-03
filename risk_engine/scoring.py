import pandas as pd
import json
from rules import check_account_age, check_transaction_frequency, check_quick_forward, check_unique_senders

def load_config():
    with open("config.json") as f:
        return json.load(f)

def calculate_risk_score(account_data, config):
    rules = config["rules"]
    score = 0
    score += check_account_age(account_data["account_age"], rules["account_age_days"], rules["account_age_score"])
    score += check_transaction_frequency(account_data["txn_per_hour"], rules["transactions_per_hour"], rules["transactions_per_hour_score"])
    score += check_quick_forward(account_data["min_forward_time"], rules["quick_forward_minutes"], rules["quick_forward_score"])
    score += check_unique_senders(account_data["unique_senders"], rules["unique_senders_min"], rules["unique_senders_score"])
    return score

def run_engine(csv_path):
    config = load_config()
    df = pd.read_csv(csv_path)
    results = []
    for _, row in df.iterrows():
        score = calculate_risk_score(row, config)
        results.append({
            "account_id": row["account_id"],
            "risk_score": score,
            "flagged": score >= config["risk_threshold"]
        })
    return pd.DataFrame(results)
