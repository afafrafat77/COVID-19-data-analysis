import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import Input, Output
from Second_page import layout as second_layout, register_callbacks

import dash_core_components as dcc

# Create the dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE, '/custom.css'])

# Assign the layout
app.layout = second_layout

# Register the callbacks
register_callbacks(app)

# Define the navigation bar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Covid", href="/Covid")),
        dbc.NavItem(dbc.NavLink("Daily", href="/Daily")),
        dbc.NavItem(dbc.NavLink("Top Movers", href="/growth")),
        dbc.NavItem(dbc.NavLink("Volume", href="/volume")),
    ],
    brand="COVID-19 Dashboard",
    brand_href="/",
    color="dark",
    dark=True,
)

footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(html.A("Afaf Rafat| GitHub", href="https://github.com/afafrafat77"), align='left'),
        ],
    ),
    className="footer",
    fluid=True,
)

# Layout for the page container
app.layout = html.Div([
    navbar,  # Include the navigation bar
    dcc.Location(id='url', refresh=False),  # Location component to manage URLs
    html.Div(id='page-content'),  # This is where the content will be updated based on the URL
    footer,  # Include the footer
])

# Callback to update the page content based on the URL
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/Covid' or pathname == '/':
        from First_page import layout  # Import the overview page layout
        return layout
    elif pathname == '/Daily':
        from Second_page import layout  # Import the sector-avg page layout
        return layout
    elif pathname == '/growth':
        from pages.growth import layout  # Import the growth page layout
        return layout
    elif pathname == '/volume':
        from pages.volume import layout  # Import the volume page layout
        return layout
    else:
        return html.Div([html.H1('Covid_19 Dashboard')])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
