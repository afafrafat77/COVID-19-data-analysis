import dash
from dash import html, dcc
import pandas as pd
import numpy as np
import plotly.express as px
import dash_bootstrap_components as dbc

# Load the data for the overview page
df = pd.read_csv('covid_complete_df2.csv')  # Adjust path as needed

# Clean data
df['Confirmed'] = df['Confirmed'].apply(lambda x: x if x > 0 else 1)
df['Deaths'] = df['Deaths'].apply(lambda x: x if x > 0 else 1)
df['Recovered'] = df['Recovered'].apply(lambda x: x if x > 0 else 1)
df = df.dropna(subset=['Confirmed', 'Deaths', 'Recovered'])

df['Sqrt_Recovered'] = np.sqrt(df['Recovered'])
# Scatter Plot
scatter_fig = px.scatter(
    df,
    x="Confirmed",
    y="Deaths",
    animation_frame="Date",
    animation_group="Country",
    color="WHO Region",
    hover_name="Country",
    size="Sqrt_Recovered",
    size_max=55,
    log_x=True,
    log_y=True,
    range_x=[df["Confirmed"].min(), df["Confirmed"].max()],
    range_y=[df["Deaths"].min(), df["Deaths"].max()],
    hover_data={
        "Recovered": True,  # Show the original 'Recovered' value in the hover
        "Confirmed": True,  # Do not repeat confirmed in hover (optional)
        "Deaths": True,  # Do not repeat deaths in hover (optional)
        "Sqrt_Recovered": False  # Do not show sqrt-transformed 'Recovered' in hover
    }

)
scatter_fig.update_layout(
    plot_bgcolor='#3a3b47',  # Set dark grey color for the graph's plot area
    paper_bgcolor='#3a3b47',  # Set dark grey for the entire paper (outside the plot)
    font=dict(color='white'),  # Set text color to white for contrast
)


# Bar Plot
bar_fig = px.bar(
    df,
    x="WHO Region",
    y="Confirmed",
    color="WHO Region",
    animation_frame="Date",
    animation_group="Country",
    range_y=[df["Confirmed"].min(), df["Confirmed"].max()],
)
bar_fig.update_layout(
    plot_bgcolor='#2C3E50',
    paper_bgcolor='#34495E',
    font=dict(color='white'),
)

# Layout for the overview page
layout = html.Div([
    html.H1('COVID-19 Dashboard Overview', style={'textAlign': 'center', 'color': 'white','marginBottom': '40px'}),

    dbc.Row([  # Use a row to arrange the plots side by side
        dbc.Col(dcc.Graph(figure=scatter_fig), width=6),  # Left column for the scatter plot
        dbc.Col(dcc.Graph(figure=bar_fig), width=6),  # Right column for the bar plot
    ], justify="center"),  # This centers the row content
])
