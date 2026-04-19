import pandas as pd

def rfm_scoring(rfm):

    rfm['R_score'] = pd.qcut(rfm['Recency'], 5, labels=[5,4,3,2,1], duplicates='drop')
    rfm['F_score'] = pd.qcut(rfm['Frequency'], 5, labels=False, duplicates='drop') + 1
    rfm['M_score'] = pd.qcut(rfm['Monetary'], 5, labels=False, duplicates='drop') + 1

    rfm['RFM_Score'] = (
        rfm['R_score'].astype(int).astype(str) +
        rfm['F_score'].astype(int).astype(str) +
        rfm['M_score'].astype(int).astype(str)
    )

    return rfm

def segment_customers(rfm):
    def segment(row):
        score = row['RFM_Score']

        if score == '555':
            return 'Champions'
        elif row['R_score'] >= 4 and row['F_score'] >= 4:
            return 'Loyal'
        elif row['R_score'] <= 2:
            return 'At Risk'
        else:
            return 'Others'

    rfm['Segment'] = rfm.apply(segment, axis=1)
    return rfm