# %% Import Libraries ---------------------------------------------------------
import pickle
import zipfile
import pandas as pd

from utiles import add_remove_characters


# %% Constants ----------------------------------------------------------------
DATAFILE_PATH = ".\\data\\SynopticData_Iran_2000_2022.zip"


# %% Load Data ----------------------------------------------------------------
with zipfile.ZipFile(DATAFILE_PATH, mode="r") as zf:
    df = pd.read_csv(zf.open("SynopticData_Iran_2000_2022.csv"), sep=";")


# %% Data Cleansing: Rename Columns -------------------------------------------
df.rename(
    columns={
        "name": "station_name",
        "station_id": "station_id",
        "lon": "station_longitude",
        "lat": "station_latitude",
        "ground_elevation": "station_altitude",
        "data": "date",
        "tmax": "temperature_max",
        "tmin": "temperature_min",
        "tm": "temperature_mean",
        "rrr24_70000": "precipitation",
    },
    inplace = True
)


# %% Data Cleansing: Convert _date_ to Date
df['date'] = pd.to_datetime(df['date'])


# %% Data Cleansing: Clean _station_name_ Column
df['station_name'] = df['station_name']\
    .apply(add_remove_characters).str.upper()


# %% Data Cleansing: Show Number of na
df.isna().sum()


# %% Data Cleansing: Replace na Value with -999 in _station_id_ and _station_altitude_ Columns
df.loc[df["station_id"].isna(), "station_id"] = -999
df.loc[df["station_altitude"].isna(), "station_altitude"] = -999


# %% Data Cleansing: Extract Station Info
gb = ["station_name", "station_id", "station_latitude", "station_longitude", "station_altitude"]

station_info = df.groupby(by = gb)\
    .agg(
        date_min = ('date', 'min'),
        date_max = ('date', 'max'),
    )\
    .sort_values(by = ["station_name", "station_id"])\
    .reset_index()


data = pd.DataFrame()

for _, st in station_info.iterrows():

    df_tmp = df[
        (df["station_name"] == st["station_name"]) &
        (df["station_id"] == st["station_id"]) &
        (df["station_latitude"] == st["station_latitude"]) &
        (df["station_longitude"] == st["station_longitude"]) &
        (df["station_altitude"] == st["station_altitude"])
    ]

    df_date = pd.DataFrame(
        {
            "station_name": st["station_name"],
            "station_id": st["station_id"],
            "station_latitude": st["station_latitude"],
            "station_longitude": st["station_longitude"],
            "station_altitude": st["station_altitude"],
            "date": pd.date_range(
                start = st["date_min"].strftime('%Y-%m-%d'),
                end = st["date_max"].strftime('%Y-%m-%d')
            ).strftime('%Y-%m-%d')
        }
    )

    df_tmp["date"] = df_tmp["date"].astype(str)
    df_date["date"] = df_date["date"].astype(str)
    df_tmp = df_tmp.merge(right = df_date, on = gb + ["date"])\
        .sort_values(by = ["date"])\
        .reset_index()
    df_tmp['date'] = pd.to_datetime(df_tmp['date'])

    data = pd.concat([data, df_tmp])


# %%
station_info.to_csv("stations_info.csv", index = False)

# %% Data Cleansing: Save data as pickle
data.to_pickle("data.pkl")


# %% Data Cleansing: Load Pickle Data
data = pd.read_pickle("data.pkl")

# %% Data Cleansing: Select Stations
day = 1

gb = ["station_name", "station_id", "station_latitude", "station_longitude", "station_altitude"]

station_info = data.groupby(by = gb)\
    .agg(
        date_min = ('date', 'min'),
        date_max = ('date', 'max'),
        temperature_max_count = ('temperature_max', 'count'),
        temperature_max_na = ('temperature_max', lambda x: sum(x.isna())),
        temperature_min_count = ('temperature_min', 'count'),
        temperature_min_na = ('temperature_min', lambda x: sum(x.isna())),
        temperature_mean_count = ('temperature_mean', 'count'),
        temperature_mean_na = ('temperature_mean', lambda x: sum(x.isna())),
        precipitation_count = ('precipitation', 'count'),
        precipitation_na = ('precipitation', lambda x: sum(x.isna())),
    )\
    .sort_values(by = ["station_name", "station_id"])\
    .reset_index()#.to_csv("station_info.csv", index = False)

station_info['number_days'] = (station_info['date_max'] - station_info['date_min']).dt.days + 1

station_info['temperature_max_percent'] = (station_info['temperature_max_count'] / station_info['number_days']) * 100

station_info['temperature_min_percent'] = (station_info['temperature_min_count'] / station_info['number_days']) * 100

station_info['temperature_mean_percent'] = (station_info['temperature_mean_count'] / station_info['number_days']) * 100

station_info['precipitation_percent'] = (station_info['precipitation_count'] / station_info['number_days']) * 100

station_info['average_percent'] = (station_info['temperature_max_percent'] + station_info['temperature_min_percent'] + station_info['temperature_mean_percent'] + station_info['precipitation_percent']) / 4

station_info = station_info[station_info["average_percent"] > 1]
station_info = station_info[station_info["number_days"] > 365]

# station_tmp = station_info[
#         (station_info["temperature_max_count"] >= day) &
#         (station_info["temperature_min_count"] >= day) &
#         (station_info["temperature_mean_count"] >= day) &
#         (station_info["precipitation_count"] >= day)
#     ].reset_index(drop = True)

station_info.to_csv("stations_info.csv", index = False)

# %% Data Cleansing: Save Data
data.loc[data["station_name"].isin(list(station_info["station_name"])), :]\
    .sort_values(by=["station_name", "date"])\
    .reset_index(drop=True)\
    .to_csv("data.csv", index = False)

# %% 
a = station_info[station_info.duplicated(subset="station_name", keep=False)]
