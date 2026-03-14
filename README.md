Member 1 Contribution – Data Pipeline and Model Development

Data Generation

The first stage of the project involved generating a synthetic financial transaction dataset.
A Python module was developed to simulate realistic transaction behaviour including transaction amounts, sender balance, receiver balance, and fraud labels.

The generated dataset was stored in the file:

"transactions.csv"

This dataset acts as the raw input for further processing and machine learning model training.

---

Feature Engineering

The raw dataset was processed using a feature engineering pipeline.
This step prepares the dataset by selecting relevant attributes and transforming them into a format suitable for machine learning algorithms.

The processed dataset was saved as:

"featured_transactions.csv"

This file contains the final set of features used for model training and evaluation.

---

Model Development

A machine learning model was implemented using the Python Scikit-learn library to classify financial transactions as either fraudulent or legitimate.

The model was trained using the processed dataset generated during the feature engineering stage.

The training pipeline includes:

- Loading the dataset
- Splitting the data into training and testing sets
- Training the classification model
- Generating predictions for evaluation

---

Model Evaluation

After training, the model was evaluated on the test dataset to measure its performance.

The fraud detection model achieved an accuracy score of 0.92, demonstrating effective detection capability for fraudulent transaction patterns.

---

Implemented Modules

The following files were implemented as part of the data pipeline and model training system:

"data_generator.py" – Generates synthetic financial transaction data

"feature_engineering.py" – Processes raw transaction data and extracts relevant features

"model_building.py" – Trains the fraud detection machine learning model

"transactions.csv" – Raw generated transaction dataset

"featured_transactions.csv" – Processed dataset used for training the model

---

These components together form the core machine learning pipeline of the Mule Detection Framework.