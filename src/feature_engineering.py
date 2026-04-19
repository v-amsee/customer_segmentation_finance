import pandas as pd

def create_rfm(df):
    snapshot_date = df['InvoiceDate'].max()

    rfm = df.groupby('CustomerID').agg({
        'InvoiceDate': lambda x: (snapshot_date - x.max()).days,
        'InvoiceNo': 'nunique',
        'TotalPrice': 'sum'
    })

    rfm.columns = ['Recency', 'Frequency', 'Monetary']
    return rfm


def add_behavior_features(df):
    behavior = df.groupby('CustomerID').agg({
        'TotalPrice': ['mean', 'std'],
        'Quantity': 'sum',
        'StockCode': 'nunique'
    })

    behavior.columns = ['AvgSpend', 'SpendStd', 'TotalQuantity', 'UniqueProducts']

    behavior = behavior.fillna(0)
    return behavior