Mule Detection Framework
A machine learning based framework designed to detect fraudulent financial transactions by analyzing behavioral patterns in transaction data.
Problem
Financial systems face fraud through mule accounts that transfer illegal funds across multiple transactions. Traditional rule-based systems fail because fraudsters constantly change behavior. This project uses machine learning to automatically detect suspicious patterns at scale.
How It Works
Data Generation → Feature Engineering → Model Training → Prediction Interface
Project Structure
mule-detection-framework/
├── data_generator.py          # Generates synthetic transaction data
├── feature_engineering.py     # Processes and prepares features
├── model_building.py          # Trains the fraud detection model
├── analysis.py                # Analyzes fraud patterns
├── app.py                     # Streamlit prediction interface
├── transactions.csv           # Raw transaction data
├── featured_transactions.csv  # Processed dataset
└── fraud_model.pkl            # Trained ML model
Getting Started
# Clone the repo
git clone https://github.com/your-username/mule-detection-framework.git
cd mule-detection-framework

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python data_generator.py
python feature_engineering.py
python model_building.py

# Launch the app
streamlit run app.py
Tech Stack
Python — Core language
Pandas — Data processing
Scikit-learn — Model training
Matplotlib — Visualization
Streamlit — Prediction interface
Model Performance
Metric
Score
Accuracy
92%
Team
Member
Work Done
Member 1 ⭐
Data generation, feature engineering, model training
Member 2
Documentation, architecture design, problem analysis
Member 3
Data analysis and visualization
Member 4
Prediction interface (Streamlit app)
This project was built by Member 1, who developed the core pipeline — data generation, feature engineering, and model training.