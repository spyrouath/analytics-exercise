# import dash-core, dash-html, dash io, bootstrap
import os

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Dash Bootstrap components
import dash_bootstrap_components as dbc

# Navbar, layouts, custom callbacks

from navbar import Navbar
from layouts import (
    appMenu,
    menuSlider,
    segmentLayout,
)
import callbacks

# Import app
from app import app

# Import server for deployment
from app import srv as server


app_name = os.getenv("DASH_APP_PATH", "/segmentation_app")

# Layout variables, navbar, header, content, and container
nav = Navbar()

header = dbc.Row(
    dbc.Col(
        html.Div(
            [
                html.H2(children="Customer History"),
                html.H3(children="A Visualization of Customer Historical Data"),
            ]
        )
    ),
    className="banner",
)

content = html.Div([dcc.Location(id="url"), html.Div(id="page-content")])

container = dbc.Container([header, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def display_page(pathname):
    if pathname in [app_name, app_name + "/"]:
        return html.Div(
            [
                dcc.Markdown(
                    """
            ### The Application
            Something about the app

            ### The Analysis
            Something about the analysis

            ### The Data
            Something about the data
        """
                )
            ],
            className="home",
        )
    elif pathname.endswith("/segments"):
        return appMenu, menuSlider, segmentLayout
    # elif pathname.endswith("/customer"):
    #     return appMenu, menuSlider, playerMenu, battingLayout
    # elif pathname.endswith("/likes"):
    #     return appMenu, menuSlider, playerMenu, fieldingLayout
    else:
        return "ERROR 404: Page not found!"


# Main index function that will call and return all layout variables
def index():
    layout = html.Div([nav, container])
    return layout


# Set layout to index function
app.layout = index()

# Call app server
if __name__ == "__main__":
    # set debug to false when deploying app
    app.run_server(host="0.0.0.0", debug=True)
