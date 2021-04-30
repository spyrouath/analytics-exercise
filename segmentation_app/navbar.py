# Import Bootstrap from Dash
import os

import dash_bootstrap_components as dbc


app_name = os.getenv("DASH_APP_PATH", "/segmentation_app")

# Navigation Bar fucntion
def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Segments Analysis", href=f"{app_name}/segments")),
        ],
        brand="Home",
        brand_href=f"{app_name}",
        sticky="top",
        color="#FC462A",
        dark=False,
        expand="lg",
    )
    return navbar
