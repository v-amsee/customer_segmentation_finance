from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report


def define_churn(rfm):
    # If no purchase in last 90 days → churn
    rfm['Churn'] = (rfm['Recency'] > 90).astype(int)
    return rfm


def train_model(rfm):
    features = ['Recency', 'Frequency', 'Monetary', 'AvgSpend', 'TotalQuantity']

    X = rfm[features]
    y = rfm['Churn']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    print(classification_report(y_test, preds))

    rfm['Churn_Prob'] = model.predict_proba(X)[:, 1]

    return model, rfm