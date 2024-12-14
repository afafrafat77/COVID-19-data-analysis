import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import numpy as np

# Load the dataset
df = pd.read_csv('full_grouped_df.csv')  # Adjust the path accordingly

# Clean data: Replace zero or negative values with a small positive value (1) and drop NaN values
df['Confirmed'] = df['Confirmed'].apply(lambda x: x if x > 0 else 1)
df['Deaths'] = df['Deaths'].apply(lambda x: x if x > 0 else 1)
df['Recovered'] = df['Recovered'].apply(lambda x: x if x > 0 else 1)
df = df.dropna(subset=['Confirmed', 'Deaths', 'Recovered'])

# Convert 'Date' column to datetime if it's not already
df['Date'] = pd.to_datetime(df['Date'])

# Group the data by Date and WHO Region and calculate the mean Fatality and Recovery Rates
df_grouped = df.groupby(['Date', 'WHO Region']).agg({
    'Fatality Rate': 'mean',
    'Recovery Rate': 'mean'
}).reset_index()

# Layout for the page
layout = html.Div([
    html.H1("COVID-19 - Recovery and Fatality Rate Over Time by WHO Region",
            style={'textAlign': 'center', 'color': 'white', 'margin-top': '30px', 'marginBottom': '40px'}),

    # RadioItems component for selecting between Fatality Rate and Recovery Rate
    dbc.Row(
        dbc.Col(
            dcc.RadioItems(
                id='rate-selector',
                options=[
                    {'label': 'Recovery Rate', 'value': 'Recovery Rate'},
                    {'label': 'Fatality Rate', 'value': 'Fatality Rate'}
                ],
                value='Recovery Rate',  # Default value
                labelStyle={'display': 'inline-block', 'color': 'white'},
                style={'textAlign': 'center', 'marginBottom': '20px'}
            ),
            width=12
        )
    ),

    # Graph to display the selected rate
    dbc.Row(
        dbc.Col(
            dcc.Graph(id='line-plot'),
            width=12
        )
    ),
])

# Callback to update the plot based on selected rate
def register_callbacks(app):
    @app.callback(
        Output('line-plot', 'figure'),
        [Input('rate-selector', 'value')]
    )
    def update_plot(selected_rate):
        # Create a new line plot based on the selected rate
        fig = px.line(
            df_grouped,
            x="Date",
            y=selected_rate,
            color="WHO Region",
            title=f"{selected_rate} Over Time by WHO Region",
            labels={selected_rate: f"{selected_rate} (%)", "Date": "Date"},
        )

        fig.update_layout(
            plot_bgcolor='#3a3b47',
            paper_bgcolor='#3a3b47',
            font=dict(color='white'),
            hovermode='closest'
        )
        return fig
