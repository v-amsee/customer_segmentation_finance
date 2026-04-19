import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Load dataset
df = pd.read_csv('../data/final_data.csv')

# Remove extreme outliers for better visualization
df = df[df['CLV'] < df['CLV'].quantile(0.99)]
df = df[df['Monetary'] < df['Monetary'].quantile(0.99)]

app = dash.Dash(__name__)

app.layout = html.Div(style={
    'backgroundColor': '#111111',
    'color': 'white',
    'padding': '20px'
}, children=[

    html.H1("Customer Segmentation Dashboard", style={'textAlign': 'center'}),

    # Segment filter
    dcc.Dropdown(
        id='segment-filter',
        options=[{'label': s, 'value': s} for s in df['Segment'].unique()],
        placeholder="Filter by Segment",
        style={'width': '300px', 'color': 'black'}
    ),

    # KPI section
    html.Div(id='kpis', style={
        'display': 'flex',
        'justifyContent': 'space-between',
        'marginTop': '20px',
        'marginBottom': '30px'
    }),

    # Charts
    dcc.Graph(id='segment-chart'),
    dcc.Graph(id='clv-churn-chart'),
    dcc.Graph(id='revenue-chart'),
    dcc.Graph(id='behavior-chart')
])


@app.callback(
    [
        Output('kpis', 'children'),
        Output('segment-chart', 'figure'),
        Output('clv-churn-chart', 'figure'),
        Output('revenue-chart', 'figure'),
        Output('behavior-chart', 'figure')
    ],
    Input('segment-filter', 'value')
)
def update_dashboard(segment):

    dff = df[df['Segment'] == segment] if segment else df

    # Optional sampling for performance
    if len(dff) > 5000:
        dff = dff.sample(5000, random_state=42)

    # KPI cards
    kpis = [
        card("Customers", len(dff)),
        card("Avg CLV", round(dff['CLV'].mean(), 2)),
        card("Churn %", round(dff['Churn'].mean() * 100, 2)),
        card("Revenue", round(dff['Monetary'].sum(), 2))
    ]

    # Segment distribution
    fig1 = px.histogram(dff, x='Segment', color='Segment')

    # CLV vs churn (log scale handles skew)
    fig2 = px.scatter(
        dff,
        x='CLV',
        y='Churn_Prob',
        color='Segment',
        log_x=True,
        render_mode='svg'
    )

    # Revenue distribution
    fig3 = px.box(dff, x='Segment', y='Monetary')

    # Behavior plot (log scale for skewed spend)
    fig4 = px.scatter(
        dff,
        x='Frequency',
        y='Monetary',
        color='Segment',
        log_y=True,
        render_mode='svg'
    )

    return kpis, fig1, fig2, fig3, fig4


def card(title, value):
    return html.Div([
        html.H4(title),
        html.H2(value)
    ], style={
        'backgroundColor': '#1e1e1e',
        'padding': '20px',
        'borderRadius': '10px',
        'textAlign': 'center',
        'width': '23%'
    })


if __name__ == '__main__':
    app.run(debug=True)