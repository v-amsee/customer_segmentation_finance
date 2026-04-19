from src.preprocessing import load_data, clean_data
from src.feature_engineering import create_rfm, add_behavior_features
from src.segmentation import rfm_scoring, segment_customers
from src.churn_model import define_churn, train_model
from src.clv import calculate_clv

# Load
df = load_data('data/Online Retail.xlsx')

# Clean
df = clean_data(df)

# Features
rfm = create_rfm(df)
behavior = add_behavior_features(df)

rfm = rfm.merge(behavior, on='CustomerID')

# Segmentation
rfm = rfm_scoring(rfm)
rfm = segment_customers(rfm)

# Churn
rfm = define_churn(rfm)
model, rfm = train_model(rfm)

# CLV
rfm = calculate_clv(rfm)

# Save
rfm.to_csv('data/final_data.csv')
print("✅ Pipeline completed. File saved: data/final_data.csv")