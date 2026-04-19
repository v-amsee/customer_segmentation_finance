def calculate_clv(rfm):
    # Simple CLV proxy
    rfm['CLV'] = rfm['Monetary'] * rfm['Frequency']
    return rfm