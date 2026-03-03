# scoring.py

import json
from rules import (
    account_age_rule,
    transaction_velocity_rule,
    quick_forward_rule,
    unique_sender_rule
)

# Load configuration
with open("risk_engine/config.json") as f:
    config = json.load(f)


def calculate_risk(account_data):
    """
    Calculate total risk score for an account.
    account_data should contain:
    - account_age
    - tx_per_hour
    - time_diff_minutes
    - unique_senders
    """

    score = 0

    score += account_age_rule(
        account_data["account_age"],
        config["account_age_weight"]
    )

    score += transaction_velocity_rule(
        account_data["tx_per_hour"],
        config["velocity_weight"]
    )

    score += quick_forward_rule(
        account_data["time_diff_minutes"],
        config["quick_forward_weight"]
    )

    score += unique_sender_rule(
        account_data["unique_senders"],
        config["unique_sender_weight"]
    )

    return score


def is_suspicious(account_data):
    risk_score = calculate_risk(account_data)
    return risk_score > config["risk_threshold"]
