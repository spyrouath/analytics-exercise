import dash_core_components as dcc
import dash_html_components as html
import dash_table

# Import Bootstrap components
import dash_bootstrap_components as dbc

# Import custom data.py
import data

segments_df = data.segments
period_list = data.period_list
period_marks = data.period_marks

appMenu = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.H4(style={"text-align": "center"}, children="Select Period:"),
                    xs={"size": "auto", "offset": 0},
                    sm={"size": "auto", "offset": 0},
                    md={"size": "auto", "offset": 3},
                    lg={"size": "auto", "offset": 0},
                    xl={"size": "auto", "offset": 0},
                ),
                dbc.Col(
                    dcc.Dropdown(
                        style={
                            "text-align": "center",
                            "font-size": "18px",
                            "width": "160px",
                        },
                        id="period-dropdown",
                        options=period_list,
                        value=period_list[0]["value"],
                        clearable=False,
                    ),
                    xs={"size": "auto", "offset": 0},
                    sm={"size": "auto", "offset": 0},
                    md={"size": "auto", "offset": 0},
                    lg={"size": "auto", "offset": 0},
                    xl={"size": "auto", "offset": 0},
                ),
                dbc.Col(
                    html.H4(
                        style={"text-align": "center", "justify-self": "right"},
                        children="Select Segment:",
                    ),
                    xs={"size": "auto", "offset": 0},
                    sm={"size": "auto", "offset": 0},
                    md={"size": "auto", "offset": 3},
                    lg={"size": "auto", "offset": 0},
                    xl={"size": "auto", "offset": 1},
                ),
                dbc.Col(
                    dcc.Dropdown(
                        style={
                            "text-align": "center",
                            "font-size": "18px",
                            "width": "160",
                        },
                        id="segment-dropdown",
                        clearable=False,
                    ),
                    xs={"size": "auto", "offset": 0},
                    sm={"size": "auto", "offset": 0},
                    md={"size": "auto", "offset": 0},
                    lg={"size": "auto", "offset": 0},
                    xl={"size": "auto", "offset": 0},
                ),
            ],
            form=True,
        ),
        dbc.Row(
            dbc.Col(
                html.P(
                    style={"font-size": "16px", "opacity": "70%"},
                    children="",
                )
            )
        ),
    ],
    className="menu",
)


menuSlider = html.Div(
    [
        dbc.Row(
            dbc.Col(
                dcc.RangeSlider(
                    id="period-slider",
                    min=1,
                    max=segments_df["week"].max(),
                    marks=period_marks,
                    tooltip={"always_visible": False, "placement": "bottom"},
                )
            )
        ),
        dbc.Row(
            dbc.Col(
                html.P(
                    style={"font-size": "16px", "opacity": "70%"},
                    children="Adjust slider to desired range.",
                )
            )
        ),
    ],
    className="period-slider",
)

segmentLayout = html.Div(
    [
        dbc.Row(dbc.Col(html.H3(children="Segmentation Data"))),
        dbc.Row(
            dbc.Col(
                html.Div(id="segment-data"),
                xs={"size": "auto", "offset": 0},
                sm={"size": "auto", "offset": 0},
                md={"size": 7, "offset": 0},
                lg={"size": "auto", "offset": 0},
                xl={"size": "auto", "offset": 0},
            ),
            justify="center",
        ),
        dbc.Row(dbc.Col(html.H3(children="Recency/Frequency per Segment"))),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="wl-bar", config={"displayModeBar": False}),
                xs={"size": 12, "offset": 0},
                sm={"size": 12, "offset": 0},
                md={"size": 12, "offset": 0},
                lg={"size": 12, "offset": 0},
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="revenue-line", config={"displayModeBar": False}),
                xs={"size": 12, "offset": 0},
                sm={"size": 12, "offset": 0},
                md={"size": 12, "offset": 0},
                lg={"size": 12, "offset": 0},
            )
        ),
        # Bar Char of Errors and Double Plays
        dbc.Row(
            dbc.Col(
                dcc.Graph(id="feild-line", config={"displayModeBar": False}),
                xs={"size": 12, "offset": 0},
                sm={"size": 12, "offset": 0},
                md={"size": 12, "offset": 0},
                lg={"size": 12, "offset": 0},
            )
        ),
        dbc.Row(dbc.Col(html.H4(children="Revenue Performance"))),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(id="pitch-bubble", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 6, "offset": 0},
                ),
                # Pie Chart, % of Completed Games, Shutouts, and Saves of Total Games played
                dbc.Col(
                    dcc.Graph(id="pitch-pie", config={"displayModeBar": False}),
                    xs={"size": 12, "offset": 0},
                    sm={"size": 12, "offset": 0},
                    md={"size": 12, "offset": 0},
                    lg={"size": 6, "offset": 0},
                ),
            ],
            no_gutters=True,
        ),
    ],
    className="app-page",
)