import pandas as pd

def load_data(path):
    df = pd.read_excel(path, engine='openpyxl')
    df.columns = df.columns.str.strip()
    return df

def clean_data(df):
    # Remove missing customers
    df = df.dropna(subset=['CustomerID'])

    # Remove negative / return transactions
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]

    # Convert types
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    df['CustomerID'] = df['CustomerID'].astype(int)

    # Create total price
    df['TotalPrice'] = df['Quantity'] * df['UnitPrice']

    # Remove duplicates
    df = df.drop_duplicates()

    return df