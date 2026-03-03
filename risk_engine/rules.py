def check_account_age(account_age_days, threshold, score):
    return score if account_age_days < threshold else 0

def check_transaction_frequency(txn_count_per_hour, threshold, score):
    return score if txn_count_per_hour > threshold else 0

def check_quick_forward(time_diff_minutes, threshold, score):
    return score if time_diff_minutes < threshold else 0

def check_unique_senders(unique_sender_count, threshold, score):
    return score if unique_sender_count >= threshold else 0
