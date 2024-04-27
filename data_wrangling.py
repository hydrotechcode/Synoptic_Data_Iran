# %% Import Libraries ---------------------------------------------------------
import zipfile
import pandas as pd

from utiles import add_remove_characters


# %% Constants ----------------------------------------------------------------
DATAFILE_PATH = ".\\data\\SynopticData_Iran_2000_2022.zip"


# %% Load Data ----------------------------------------------------------------
with zipfile.ZipFile(DATAFILE_PATH, mode="r") as zf:
    data = pd.read_csv(zf.open("SynopticData_Iran_2000_2022.csv"), sep=";")


# %% Data Cleansing -----------------------------------------------------------
# Rename Columns
df = data.rename(
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
    }
)

# Clean station_name Column
df['station_name'] = df['station_name']\
    .apply(add_remove_characters).str.upper()


# %%
st = df.drop_duplicates(
    subset=["station_name", "station_id", "station_latitude", "station_longitude", "station_altitude"]
).drop(columns=["date", "temperature_max", "temperature_min", "temperature_mean", "precipitation"])\
    .reset_index(drop=True)


# %%
# ab = df[df["station_name"] == "ABBAR"]

s_id = ab["station_id"].unique()

ab.loc[ab["station_id"] == s_id[0], "station_id"] = s_id[1]

# df.drop(ab.index, inplace=True)
