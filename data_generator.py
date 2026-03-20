import random
from datetime import datetime, timedelta


def generate_transactions(n=3000):

    transactions = []
    base_time = datetime.now()

    for i in range(n):

        sender = random.randint(10000, 10100)
        receiver = random.randint(20000, 20100)

        amount = round(random.uniform(100, 50000), 2)

        timestamp = base_time - timedelta(minutes=random.randint(1, 100000))

        account_age_days = random.randint(1, 1000)

        transaction_type = random.choice(["NEFT", "IMPS", "UPI", "RTGS"])

        # 🔥 Fraud logic (Mule behaviour simulation)
        fraud = 0

        # Condition 1: Very new account + high amount
        if account_age_days < 30 and amount > 30000:
            fraud = 1

        # Condition 2: Random small percentage fraud (5%)
        elif random.random() < 0.05:
            fraud = 1

        transactions.append([
            i,
            sender,
            receiver,
            amount,
            timestamp,
            account_age_days,
            transaction_type,
            fraud
        ])

    return transactions