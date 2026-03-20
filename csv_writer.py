import csv
from data_generator import generate_transactions


def write_to_csv(filename="transactions.csv", n=3000):

    data = generate_transactions(n)

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)

        # Header
        writer.writerow([
            "transaction_id",
            "sender",
            "receiver",
            "amount",
            "timestamp",
            "account_age_days",
            "transaction_type",
            "fraud_flag"
        ])

        writer.writerows(data)

    print("CSV file created successfully!")


# Run this file directly
if __name__ == "__main__":
    write_to_csv()