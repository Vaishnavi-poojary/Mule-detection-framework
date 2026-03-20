

## Member 1 Contribution – Data Pipeline and Model Development

### Data Generation
The first stage of the project involved generating a synthetic financial transaction dataset.
A Python module was developed to simulate realistic transaction behaviour including transaction amounts, sender balance, receiver balance, and fraud labels.

The generated dataset was stored in the file:

transactions.csv

---

### Feature Engineering
The raw dataset was processed using a feature engineering pipeline.  
This step prepares the dataset by selecting relevant attributes and transforming them into a format suitable for machine learning algorithms.

The processed dataset was saved as:

featured_transactions.csv

---

### Model Development
A machine learning model was implemented using the Python Scikit-learn library to classify financial transactions as either fraudulent or legitimate.

The model was trained using the processed dataset generated during the feature engineering stage.

---

### Model Evaluation
After training, the model was evaluated on the test dataset to measure its performance.

The fraud detection model achieved an accuracy score of **0.92**.

---

### Implemented Modules

data_generator.py – Generates synthetic financial transaction data  

feature_engineering.py – Processes raw transaction data  

model_building.py – Trains the fraud detection machine learning model  

transactions.csv – Raw generated transaction dataset  

featured_transactions.csv – Processed dataset used for training