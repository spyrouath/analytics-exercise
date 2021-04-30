import pandas as pd

segments = pd.read_csv("data/segments.csv")
customers = pd.read_csv("data/customers.csv")

period_list = [
    {"label": "week1", "value": "week1"},
    {"label": "week2", "value": "week2"},
    {"label": "week3", "value": "week3"},
    {"label": "week4", "value": "week4"},
]

period_marks = {
    1: {"label": "1"},
    2: {"label": "2"},
    3: {"label": "3"},
    4: {"label": "4"},
}


def dynamicsegments(x):
    period_time = [
        (1, 2),
        (2, 3),
        (3, 4),
    ]
    filter_segment_wk = segments[['week', 'segment_id', 'user_id', "avg_frequency"]]
    filter_week = filter_segment_wk[
        (filter_segment_wk.week >= period_time[x][0])
        & (filter_segment_wk.week <= period_time[x][1])
    ]
    filter_segments = filter_week["segment_id"].unique()
    filter_segment_ids = filter_week["segment_id"].unique()
    return [{"label": k, "value": v} for k, v in zip(filter_segments, filter_segment_ids)]


def dynamicrange(x):
    period_time = [
        (1, 2),
        (2, 3),
        (3, 4),
    ]
    return [period_time[x][0], period_time[x][1]]
