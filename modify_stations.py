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
iran_polygons = gpd.read_file("P:\\Supervisor\\Fatemeh Babaei\\Data\\Map\\Iran\\Iran.shp")

# %%
gdf = gpd.sjoin(gdf, iran_polygons, how="left", predicate="within")
# %%

gdf = gdf.drop(columns=["index_right", "source"])

gdf.rename(
    columns={
        "id": "state_id",
        "name": "state_name"},
    inplace=True
)


# %%
gdf.isna().sum()


# %%
gdf[gdf["state_id"].isna()]




# %%
gdf.loc[((gdf["station_name"] == "BABOLSAR") & (gdf["station_id"] == "40736")), "state_id"] = "IR21"
gdf.loc[((gdf["station_name"] == "BABOLSAR") & (gdf["station_id"] == "40736")), "state_name"] = "Mazandaran"

gdf.loc[((gdf["station_name"] == "ABUMUSA ISLAND") & (gdf["station_id"] == "40890")), "state_id"] = "IR23"
gdf.loc[((gdf["station_name"] == "ABUMUSA ISLAND") & (gdf["station_id"] == "40890")), "state_name"] = "Hormozgan"

gdf.loc[((gdf["station_name"] == "BANDAR-E-DAYYER") & (gdf["station_id"] == "40872")), "state_id"] = "IR06"
gdf.loc[((gdf["station_name"] == "BANDAR-E-DAYYER") & (gdf["station_id"] == "40872")), "state_name"] = "Bushehr"

gdf.loc[((gdf["station_name"] == "BUSHEHR (COASTAL)") & (gdf["station_id"] == "40857")), "state_id"] = "IR06"
gdf.loc[((gdf["station_name"] == "BUSHEHR (COASTAL)") & (gdf["station_id"] == "40857")), "state_name"] = "Bushehr"

gdf.loc[((gdf["station_name"] == "BANDAR-E-GENAVEH") & (gdf["station_id"] == "99594")), "state_id"] = "IR06"
gdf.loc[((gdf["station_name"] == "BANDAR-E-GENAVEH") & (gdf["station_id"] == "99594")), "state_name"] = "Bushehr"

gdf.loc[((gdf["station_name"] == "BANDAR-E-SIRIK") & (gdf["station_id"] == "99686")), "state_id"] = "IR23"
gdf.loc[((gdf["station_name"] == "BANDAR-E-SIRIK") & (gdf["station_id"] == "99686")), "state_name"] = "Hormozgan"

gdf.loc[((gdf["station_name"] == "JASK") & (gdf["station_id"] == "40893")), "state_id"] = "IR23"
gdf.loc[((gdf["station_name"] == "JASK") & (gdf["station_id"] == "40893")), "state_name"] = "Hormozgan"

gdf.loc[((gdf["station_name"] == "BILEHSOWAR") & (gdf["station_id"] == "99202")), "state_id"] = "IR03"
gdf.loc[((gdf["station_name"] == "BILEHSOWAR") & (gdf["station_id"] == "99202")), "state_name"] = "Ardebil"

gdf.loc[((gdf["station_name"] == "DARYACHE NAMAK") & (gdf["station_id"] == "19607")), "state_id"] = "IR10"
gdf.loc[((gdf["station_name"] == "DARYACHE NAMAK") & (gdf["station_id"] == "19607")), "state_name"] = "Khuzestan"

gdf.loc[((gdf["station_name"] == "TONB-E-BOZORG ISLAND") & (gdf["station_id"] == "40884")), "state_id"] = "IR23"
gdf.loc[((gdf["station_name"] == "TONB-E-BOZORG ISLAND") & (gdf["station_id"] == "40884")), "state_name"] = "Hormozgan"

gdf.loc[((gdf["station_name"] == "SIRI ISLAND") & (gdf["station_id"] == "40889")), "state_id"] = "IR23"
gdf.loc[((gdf["station_name"] == "SIRI ISLAND") & (gdf["station_id"] == "40889")), "state_name"] = "Hormozgan"

gdf.loc[((gdf["station_name"] == "DEHKHODA") & (gdf["station_id"] == "-999")), "state_id"] = "IR06"
gdf.loc[((gdf["station_name"] == "DEHKHODA") & (gdf["station_id"] == "-999")), "state_name"] = "Bushehr"

gdf.loc[((gdf["station_name"] == "QESHM (COASTAL)") & (gdf["station_id"] == "99675")), "state_id"] = "IR23"
gdf.loc[((gdf["station_name"] == "QESHM (COASTAL)") & (gdf["station_id"] == "99675")), "state_name"] = "Hormozgan"

gdf.loc[((gdf["station_name"] == "SOLTANABAD") & (gdf["station_id"] == "18465")), "state_id"] = "IR02"
gdf.loc[((gdf["station_name"] == "SOLTANABAD") & (gdf["station_id"] == "18465")), "state_name"] = "West Azarbaijan"

gdf.loc[((gdf["station_name"] == "HEYRAN") & (gdf["station_id"] == "18052")), "state_id"] = "IR03"
gdf.loc[((gdf["station_name"] == "HEYRAN") & (gdf["station_id"] == "18052")), "state_name"] = "Ardebil"

gdf.loc[((gdf["station_name"] == "FARID PAK") & (gdf["station_id"] == "99238")), "state_id"] = "IR27"
gdf.loc[((gdf["station_name"] == "FARID PAK") & (gdf["station_id"] == "99238")), "state_name"] = "Golestan"


# %%

gdf.to_file("stations_info.geojson", driver="GeoJSON")
# %%
