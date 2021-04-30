import pandasql as psql
from datetime import datetime
import pandas as pd
from sklearn.cluster import KMeans

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 40)
pd.set_option('display.width', 1500)

dt = pd.read_csv("data/raw_data.csv")

dt['week'] = dt['submit_dt'].apply(lambda x: pd.Timestamp(datetime.strptime(x, '%Y-%m-%d %H:%M:%S UTC')).weekofyear)
dt['day'] = dt['submit_dt'].apply(lambda x: pd.Timestamp(datetime.strptime(x, '%Y-%m-%d %H:%M:%S UTC')).dayofyear)
dt['weekday'] = dt['submit_dt'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S UTC').weekday())
dt['weekday_name'] = dt['weekday'].apply(lambda x: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday",
                                                    "Sunday"][x])

def part_of_the_day(x):
    if (x >= 5) and (x <= 12):
        return 'morning'
    elif (x > 12) and (x <= 16):
        return 'miday'
    elif (x > 16) and (x <= 22):
        return 'night'
    elif (x > 22) or (x < 5):
        return'late_night'


dt['part_of_the_day'] = dt['submit_dt'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S UTC').hour)\
    .apply(part_of_the_day)

dt = dt.sort_values(by=['user_id', 'day'], ascending=True)

# calculate recency features
dt['last_odr_lag'] = dt.groupby("user_id")['day'].transform(lambda x: x.shift(1)).fillna(0).astype(int)
dt['recency'] = abs(dt['last_odr_lag'] - dt['day'])

tx_frequency = dt.groupby('user_id').day.count().reset_index()
tx_frequency.columns = ['user_id', 'frequency']

dt = pd.merge(dt, tx_frequency, on='user_id')

dt['revenue'] = dt['basket']
tx_revenue = dt.groupby('user_id')['basket'].sum().reset_index()

dt = pd.merge(dt, tx_revenue, on='user_id')

dt['cuisine_parent'] = dt['cuisine_parent'].replace(['Healthy / Other'], 'Healthy_Other')
dt['cuisine_parent'] = dt['cuisine_parent'].replace(['Street food'], 'Street_food')

# behavioral features
dt = pd.concat([dt, pd.get_dummies(dt['part_of_the_day'])], 1)
dt = pd.concat([dt, pd.get_dummies(dt['weekday_name'])], 1)
dt = pd.concat([dt, pd.get_dummies(dt['cuisine_parent'])], 1)


def is_weekend(row):
    if ((row['Monday'] == 0) & (row['Tuesday'] == 0) & (row['Wednesday'] == 0) & (row['Tuesday'] == 0)
& (row['Friday'] == 0)) & ((row['Saturday'] == 1) | (row['Sunday'] == 1)):
        return 1
    else:
        return 0

dt['wkend'] = dt.apply(is_weekend, axis=1)

segmentation_table = psql.sqldf("select user_id, count(distinct day) as num_ords, "
                 "max(week) as week, "
                 "count(distinct week) as num_weeks, "
                 "min(recency) as min_recency, "
                 "max(recency) as max_recency, "
                 "avg(recency) as avg_recency, "
                 "min(frequency) as min_frequency, "
                 "max(frequency) as max_frequency, "
                 "avg(frequency) as avg_frequency, "
                 "min(revenue) as min_revenue, "
                 "max(revenue) as max_revenue, "
                 "avg(revenue) as avg_revenue, "
                 "sum(morning) as morning, "
                 "sum(miday) as miday, "
                 "sum(night) as night, "
                 "sum(late_night) as late_night, "
                 "sum(Monday) as mondays, "
                 "sum(Tuesday) as tuesdays, "
                 "sum(Wednesday) as wednesdays, "
                 "sum(Thursday) as thursdays, "
                 "sum(Friday) as fridays, "
                 "sum(wkend) as weekends, "
                 "sum(Breakfast) as breakfasts, "
                 "sum(Creperie) as creperies, "
                 "sum(Ethnic) as ethincs, "
                 "sum(Healthy_Other) as healthys, "
                 "sum(Italian) as italians, "
                 "sum(Meat) as meats, "
                 "sum(Street_food) as street_foods, "
                 "sum(Sweets) as sweets, "
                 "sum(Traditional) as traditionals "
                 "from dt group by user_id")

sse={}
for k in range(1, 10):
    kmeans = KMeans(n_clusters=k, max_iter=1000).fit(segmentation_table['avg_recency'].to_numpy().reshape(-1, 1))
    segmentation_table["clusters"] = kmeans.labels_
    sse[k] = kmeans.inertia_

kmeans = KMeans(n_clusters=4)
kmeans.fit(segmentation_table[['avg_recency']])
segmentation_table['RecencyCluster'] = kmeans.predict(segmentation_table[['avg_recency']])


def order_cluster(cluster_field_name, target_field_name, df, ascending):
    df_new = df.groupby(cluster_field_name)[target_field_name].mean().reset_index()
    df_new = df_new.sort_values(by=target_field_name,ascending=ascending).reset_index(drop=True)
    df_new['index'] = df_new.index
    df_final = pd.merge(df, df_new[[cluster_field_name,'index']], on=cluster_field_name)
    df_final = df_final.drop([cluster_field_name],axis=1)
    df_final = df_final.rename(columns={"index":cluster_field_name})
    return df_final


segmentation_table = order_cluster('RecencyCluster', 'avg_recency', segmentation_table, False)

kmeans = KMeans(n_clusters=4)
kmeans.fit(segmentation_table[['avg_frequency']])
segmentation_table['FrequencyCluster'] = kmeans.predict(segmentation_table[['avg_frequency']])

segmentation_table = order_cluster('FrequencyCluster', 'avg_frequency', segmentation_table, True)

kmeans = KMeans(n_clusters=4)
kmeans.fit(segmentation_table[['avg_revenue']])
segmentation_table['RevenueCluster'] = kmeans.predict(segmentation_table[['avg_revenue']])

segmentation_table = order_cluster('RevenueCluster', 'avg_revenue', segmentation_table, True)

segmentation_table['segment_id'] = segmentation_table['RecencyCluster'] + segmentation_table['FrequencyCluster'] + \
                                   segmentation_table['RevenueCluster']
# segmentation_table.groupby('segment_id')['avg_recency', 'avg_frequency', 'avg_revenue'].mean()

segmentation_table.to_csv("data/segments.csv", index=False)

customer_table = psql.sqldf("select user_id, week, count(distinct day) as num_ords, "
                 "count(distinct week) as num_weeks, "
                 "min(recency) as min_recency, "
                 "max(recency) as max_recency, "
                 "avg(recency) as avg_recency, "
                 "min(frequency) as min_frequency, "
                 "max(frequency) as max_frequency, "
                 "avg(frequency) as avg_frequency, "
                 "min(revenue) as min_revenue, "
                 "max(revenue) as max_revenue, "
                 "avg(revenue) as avg_revenue, "
                 "sum(morning) as morning, "
                 "sum(miday) as miday, "
                 "sum(night) as night, "
                 "sum(late_night) as late_night, "
                 "sum(Monday) as mondays, "
                 "sum(Tuesday) as tuesdays, "
                 "sum(Wednesday) as wednesdays, "
                 "sum(Thursday) as thursdays, "
                 "sum(Friday) as fridays, "
                 "sum(wkend) as weekends, "
                 "sum(Breakfast) as breakfasts, "
                 "sum(Creperie) as creperies, "
                 "sum(Ethnic) as ethincs, "
                 "sum(Healthy_Other) as healthys, "
                 "sum(Italian) as italians, "
                 "sum(Meat) as meats, "
                 "sum(Street_food) as street_foods, "
                 "sum(Sweets) as sweets, "
                 "sum(Traditional) as traditionals "
                 "from dt group by user_id, week order by user_id, week")

customer_table.to_csv("data/customers.csv", index=False)