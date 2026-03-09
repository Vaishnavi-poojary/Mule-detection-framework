def amount_risk(amount):
    if amount > 50000:
        return 25
    elif amount > 30000:
        return 15
    return 0


def channel_risk(txn_type):
    if txn_type in ["UPI", "IMPS"]:
        return 10
    return 0


def rapid_activity(time_diff):
    if time_diff < 600:  # 10 minutes
        return 20
    return 0
