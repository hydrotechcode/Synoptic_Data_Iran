# %% Importing libraries
import pandas as pd
import geopandas as gpd
import plotly.express as px


# %% Load Data
df = pd.read_csv("stations_info.csv")
df["station_id"] = df["station_id"].astype(int).astype(str)
df["date_min"] = pd.to_datetime(df["date_min"])
df["date_max"] = pd.to_datetime(df["date_max"])
df.info()


# %% Convert to GeoDataFrame
gdf = gpd.GeoDataFrame(
    data = df,
    geometry = gpd.points_from_xy(
        x = df["station_longitude"],
        y = df["station_latitude"]
    ),
    crs = "EPSG:4326"
)

# %% Plot Stations
fig = px.scatter_mapbox(
    data_frame=gdf,
    lat="station_latitude",
    lon="station_longitude",
    hover_name="station_name",
    hover_data=["station_id", "station_altitude", "date_min", "date_max"],
    zoom=5
)

fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.show()







# %%
