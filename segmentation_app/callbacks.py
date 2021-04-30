from dash.dependencies import Input, Output
import plotly.graph_objects as go
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from app import app
import data as data

segments_df = data.segments
customers_df = data.customers
period_list = data.period_list

for col in segments_df.columns:
    segments_df[col] = segments_df[col].astype(int)

for col in customers_df.columns:
    customers_df[col] = customers_df[col].astype(int)

@app.callback(
    [
        Output("segment-dropdown", "options"),
        Output("segment-dropdown", "value"),
        Output("period-slider", "value"),
    ],
    [Input("period-dropdown", "value")],
)
def select_period(selected_period):
    if selected_period == period_list[1]["value"]:
        segments = data.dynamicsegments(1)
        range = data.dynamicrange(1)
    elif selected_period == period_list[2]["value"]:
        segments = data.dynamicsegments(2)
        range = data.dynamicrange(2)
    else:
        segments = data.dynamicsegments(0)
        range = data.dynamicrange(0)
    return segments, segments[0]["value"], range

@app.callback(
    [Output("segment-data", "children")],
    [Input("segment-dropdown", "value"), Input("period-slider", "value")],
)
def update_win_table(selected_segment, week_range):
    filter_segments = segments_df[segments_df.segment_id == selected_segment].head(30)
    if week_range:
        filter_week = filter_segments[
            (filter_segments.week >= week_range[0]) & (filter_segments.week <= week_range[1])
        ]
    else:
        filter_week = filter_segments[
            (filter_segments.week >= 1) & (filter_segments.week <= 4)
        ]

    Data = filter_week

    data_note = []

    if Data.empty:
        data_note.append(
            html.Div(
                dbc.Alert(
                    "The selected segment did not have any data.", color="warning"
                )
            )
        )
        return data_note
    else:
        data_note.append(
            html.Div(
                dash_table.DataTable(
                    data=Data.to_dict("records"),
                    columns=[{"name": x, "id": x}for x in Data],
                    style_as_list_view=True,
                    editable=False,
                    style_table={
                        "overflowY": "scroll",
                        "width": "100%",
                        "minWidth": "100%",
                    },
                    style_header={"backgroundColor": "#f8f5f0", "fontWeight": "bold"},
                    style_cell={"textAlign": "center", "padding": "8px"},
                )
            )
        )
        return data_note

@app.callback(
    Output("wl-bar", "figure"),
    [Input("segment-dropdown", "value"), Input("period-slider", "value")],
)
def update_figure1(selected_segment, week_range):
    filter_segments = segments_df[segments_df.segment_id == selected_segment]
    filter_segments = filter_segments\
    .groupby(['week', 'avg_recency', 'avg_frequency'])['avg_revenue'].sum().reset_index()
    if week_range:
        filter_week = filter_segments[
            (filter_segments.week >= week_range[0]) & (filter_segments.week <= week_range[1])
        ]
    else:
        filter_week = filter_segments[
            (filter_segments.week >= 1) & (filter_segments.week <= 4)
        ]

    fig1 = go.Figure(
        data=[
            go.Bar(
                name="Recency",
                x=filter_week.week,
                y=filter_week.avg_recency.astype(int),
                marker_color="#004687",
                opacity=0.8,
            ),
            go.Bar(
                name="Frequency",
                x=filter_week.week,
                y=filter_week.avg_frequency.astype(int),
                marker_color="#AE8F6F",
                opacity=0.8,
            ),
        ]
    )
    fig1.update_xaxes(title="Week", tickformat="d")
    fig1.update_yaxes(fixedrange=True)
    fig1.update_layout(
        hovermode="x",
        barmode="group",
        title="Recency/Frequency Metrics",
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
    )
    return fig1

@app.callback(
    Output("revenue-line", "figure"),
    [Input("segment-dropdown", "value"), Input("period-slider", "value")],
)
def update_figure2(selected_team, week_range):
    filter_segment = segments_df[segments_df.segment_id == selected_team]
    filter_segment = filter_segment \
        .groupby(['week'])['avg_revenue', 'max_revenue'].sum().reset_index()
    if week_range:
        filter_week = filter_segment[
            (filter_segment.week >= week_range[0]) & (filter_segment.week <= week_range[1])
        ]
    else:
        filter_week = filter_segment[
            (filter_segment.week >= 1) & (filter_segment.week <= 4)
        ]

    fig2 = go.Figure(
        data=[
            go.Scatter(
                name="Total Avg Revenue",
                x=filter_week.week,
                y=filter_week.avg_revenue,
                mode="lines+markers",
                marker_color="Orange",
                opacity=0.9,
            ),
            go.Scatter(
                name="Total Max Revenue",
                x=filter_week.week,
                y=filter_week.max_revenue,
                mode="lines+markers",
                marker_color="#005C5C",
                opacity=0.8,
            ),
        ]
    )

    fig2.update_xaxes(title="Week", tickformat="d")
    fig2.update_yaxes(fixedrange=True)
    fig2.update_layout(
        hovermode="x",
        title="Monetization",
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
    )
    return fig2

@app.callback(
    Output("feild-line", "figure"),
    [Input("segment-dropdown", "value"), Input("period-slider", "value")],
)
def update_figure3(selected_segment, week_range):
    filter_segments = segments_df[segments_df.segment_id == selected_segment]
    filter_segments = filter_segments.groupby(['week'])['morning', 'night'].sum().reset_index()
    if week_range:
        filter_week = filter_segments[
            (filter_segments.week >= week_range[0]) & (filter_segments.week <= week_range[1])
        ]
    else:
        filter_week = filter_segments[
            (filter_segments.week >= 1) & (filter_segments.week <= 4)
        ]
    fig3 = go.Figure(
        data=[
            go.Bar(
                name="Breakfasts",
                x=filter_week.week,
                y=filter_week.morning,
                marker=dict(color="#5F259F"),
                opacity=0.7,
            ),
            go.Bar(
                name="Dinners",
                x=filter_week.week,
                y=filter_week.night,
                marker=dict(color="#005F61"),
                opacity=0.7,
            ),
        ]
    )

    fig3.update_xaxes(title="Week", tickformat="d")
    fig3.update_yaxes(fixedrange=True)
    fig3.update_layout(
        barmode="stack",
        hovermode="x",
        title="Breakfasts/Dinners Ratio",
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1),
    )
    return fig3

@app.callback(
    Output("pitch-pie", "figure"),
    [Input("segment-dropdown", "value"), Input("period-slider", "value")],
)
def update_figure4(selected_segment, week_range):
    filter_segments = segments_df[segments_df.segment_id == selected_segment]
    if week_range:
        filter_week = filter_segments[
            (filter_segments.week >= week_range[0]) & (filter_segments.week <= week_range[1])
        ]
    else:
        filter_week = filter_segments[
            (filter_segments.week >= 1) & (filter_segments.week <= 4)
        ]

    filter_week = filter_week.agg(['sum', 'count'])
    breakfasts = filter_week['breakfasts']['sum']/filter_week['breakfasts']['count'] * 100
    creperies = filter_week['creperies']['sum']/filter_week['creperies']['count'] * 100
    healthys = filter_week['healthys']['sum']/filter_week['healthys']['count'] * 100
    ethincs = filter_week['ethincs']['sum'] / filter_week['ethincs']['count'] * 100
    italians = filter_week['italians']['sum'] / filter_week['italians']['count'] * 100
    meats = filter_week['meats']['sum'] / filter_week['meats']['count'] * 100
    street_foods = filter_week['street_foods']['sum'] / filter_week['street_foods']['count'] * 100
    sweets = filter_week['sweets']['sum'] / filter_week['sweets']['count'] * 100
    traditionals = filter_week['traditionals']['sum'] / filter_week['traditionals']['count'] * 100

    fig4 = go.Figure(
        go.Pie(values=[breakfasts, creperies, healthys, ethincs, italians, meats, street_foods, sweets, traditionals],
               labels=["breakfasts", "creperies", "healthys", "ethincs", "italians", "meats",
                       "street_foods", "sweets", "traditionals"], opacity=0.8)
    )
    fig4.update_layout(
        hovermode=False,
        title="% of Total orders",
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
        legend=dict(orientation="h", yanchor="bottom", y=1, xanchor="right", x=1.15),
    )
    fig4.update_traces(marker=dict(colors=["#462425", "#E35625", "#CEC6C0"]))
    return fig4

@app.callback(
    Output("pitch-bubble", "figure"),
    [Input("segment-dropdown", "value"), Input("period-slider", "value")],
)
def update_figure5(selected_segment, week_range):
    filter_segment = segments_df[segments_df.segment_id == selected_segment]
    if week_range:
        filter_week = filter_segment[
            (filter_segment.week >= week_range[0]) & (filter_segment.week <= week_range[1])
        ]
    else:
        filter_week = filter_segment[
            (filter_segment.week >= 1) & (filter_segment.week <= 1)
        ]

    fig5 = go.Figure(
        data=go.Scatter(
            x=filter_week.week,
            y=filter_week.segment_id,
            mode="markers",
            marker=dict(symbol="circle-open-dot", size=0.8 * filter_week.avg_revenue, color="#006BA6"),
            hovertemplate="Ratio: %{y:.2f}<extra></extra><br>" + "%{text}",
            text=["Period: {}".format(i) for i in filter_week.avg_revenue * 0.8],
        )
    )

    fig5.update_xaxes(title="Week", tickformat="d")
    fig5.update_yaxes(title="Revenue Dynamics")
    fig5.update_layout(
        hovermode="x",
        title="Revenue Dynamics Bubble",
        font={"color": "darkslategray"},
        paper_bgcolor="white",
        plot_bgcolor="#f8f5f0",
    )
    return fig5

@app.callback(
    [Output("player-dropdown", "options"), Output("player-dropdown", "value")],
    [Input("segment-dropdown", "value"), Input("period-slider", "value")],
)
def update_player_dropdown(selected_segment, week_range):
    filter_segments = segments_df[segments_df.segment_id == selected_segment]

    if week_range:
        filter_week = filter_segments[
            (filter_segments.week >= week_range[0]) & (filter_segments.week <= week_range[1])
        ]
    else:
        filter_week = filter_segments[
            (filter_segments.week >= 1) & (filter_segments.week <= 4)
        ]
    names = [
        {"label": k, "value": v}
        for k, v in zip(filter_week.user_id, filter_week.user_id)
    ]
    user_list = []
    [user_list.append(x) for x in names if x not in user_list]
    return user_list, user_list[0]["value"]