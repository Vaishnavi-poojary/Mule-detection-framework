# rules.py

def account_age_rule(account_age, weight):
    """
    Adds risk if account age is less than threshold.
    """
    if account_age < 30:
        return weight
    return 0


def transaction_velocity_rule(tx_per_hour, weight):
    """
    Adds risk if transactions per hour exceed limit.
    """
    if tx_per_hour > 10:
        return weight
    return 0


def quick_forward_rule(time_diff_minutes, weight):
    """
    Adds risk if money is forwarded very quickly.
    """
    if time_diff_minutes < 5:
        return weight
    return 0


def unique_sender_rule(unique_senders, weight):
    """
    Adds risk if account receives money from many unique senders.
    """
    if unique_senders > 10:
        return weight
    return 0
