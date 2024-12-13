from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc  # Import Bootstrap components

# Load your dataset
df = pd.read_csv('C:/Users/ELFAJR/Downloads/covid_complete_df.csv')  # Adjust file path accordingly

# Clean data: Replace zero or negative values with a small positive value (1) and drop NaN values
df['Confirmed'] = df['Confirmed'].apply(lambda x: x if x > 0 else 1)
df['Deaths'] = df['Deaths'].apply(lambda x: x if x > 0 else 1)

# Drop rows where 'Confirmed' or 'Deaths' have NaN values
df = df.dropna(subset=['Confirmed', 'Deaths'])

# Initialize the Dash app with a dark theme
app = Dash(__name__,  external_stylesheets=[dbc.themes.SLATE, 'C:/Users/ELFAJR/Downloads/custom.css'])


# Layout for the app
app.layout = dbc.Container(  # Use Bootstrap Container for consistent layout
    [
        html.H1('COVID-19 Dashboard', style={'textAlign': 'center', 'color': 'white'}),
        html.H4("Animated Confirmed Cases and Population Over Time", style={'color': 'white'}),
        html.Label("Select an animation:", htmlFor="selection", style={'color': 'white'}),
        dcc.RadioItems(
            id="selection",
            options=[
                {'label': 'Confirmed Cases vs Deaths - Scatter', 'value': 'Confirmed Cases - Scatter'},
                {'label': 'Population - Bar', 'value': 'Population - Bar'},
            ],
            value='Confirmed Cases - Scatter',
            style={'color': 'white'},
        ),
        dcc.Loading(dcc.Graph(id="graph"), type="cube"),
    ],
    fluid=True,  # Ensure the layout is responsive
)

# Callback to update the graph based on the selected animation type
@app.callback(
    Output("graph", "figure"),
    [Input("selection", "value")]
)
def display_animated_graph(selection):
    # Define animations
    animations = {
        "Confirmed Cases - Scatter": px.scatter(
            df,
            x="Confirmed",  # Plot confirmed cases on the x-axis
            y="Deaths",  # Plot deaths on the y-axis
            animation_frame="Date",  # Change this to an existing column if "Date" doesn't exist
            animation_group="Country",  # Group by country for animation
            color="WHO Region",  # Color by WHO Region
            hover_name="Country",  # Hover information
            size_max=55,
            size="Deaths",
            log_x=True,  # Logarithmic scaling on x-axis
            range_x=[df["Confirmed"].min(), df["Confirmed"].max()],  # Set range for confirmed cases (log scale)
            range_y=[df["Deaths"].min(), df["Deaths"].max()],  # Set range for deaths
        ),
        "Population - Bar": px.bar(
            df,
            x="WHO Region",  # Plot WHO Region on the x-axis
            y="Confirmed",  # Use Confirmed cases on the y-axis
            color="WHO Region",  # Color by WHO Region
            animation_frame="Date",  # Change this to an existing column if "Date" doesn't exist
            animation_group="Country",  # Group by country for animation
            range_y=[0, df["Confirmed"].max()],  # Set range for deaths
        ),
    }

    # Apply custom background color to the plot and paper (whole figure)
    figure = animations.get(selection, {})
    figure.update_layout(
        plot_bgcolor='#2C3E50',  # Dark Navy Blue background for the plot area
        paper_bgcolor='#34495E',  # Slightly lighter dark blue for the whole paper
        font=dict(color='white'),  # Ensure the font color is white for visibility
    )

    return figure

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)