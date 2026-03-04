import pandas as pd


def create_features(input_file="transactions.csv",
                    output_file="featured_transactions.csv"):

    df = pd.read_csv(input_file)

    # 1️⃣ High Amount Flag
    df["high_amount_flag"] = df["amount"].apply(lambda x: 1 if x > 30000 else 0)

    # 2️⃣ New Account Flag
    df["new_account_flag"] = df["account_age_days"].apply(lambda x: 1 if x < 30 else 0)

    # 3️⃣ Amount per Day Ratio
    df["amount_account_age_ratio"] = df["amount"] / (df["account_age_days"] + 1)

    # 4️⃣ Transaction Type Encoding
    df["transaction_type_encoded"] = df["transaction_type"].astype("category").cat.codes

    df.to_csv(output_file, index=False)

    print("Feature engineering completed!")


if __name__ == "__main__":
    create_features()