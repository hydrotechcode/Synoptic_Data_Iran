# %% Create DataBase
from db_connect import create_db
create_db()



# %% Import Libraries
import os
import zipfile
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


# %% Initialize Environment Variables
load_dotenv()

# 'postgresql://username:password@host:port/database_name'
engine = create_engine(
    f'postgresql://{os.getenv("PostgreSQL_USERNAME")}:{os.getenv("PostgreSQL_PASSWORD")}@{os.getenv("PostgreSQL_HOST")}:{os.getenv("PostgreSQL_PORT")}/{os.getenv("PostgreSQL_DATABASE")}'
)


# %% Read Data
with zipfile.ZipFile('data.zip', 'r') as zf:
    df = pd.read_csv(zf.open('data.csv'), sep=';')


# %% Print Data
print(df.loc[0, :])
print(df.info())


# %% Data Cleaning and Preprocessing
df.columns = [
    'StationName',
    'StationID',
    'Longitude',
    'Latitude',
    'Altitude',
    'Date',
    'TemperatureMax',
    'TemperatureMin',
    'TemperatureMean',
    'Precipitation',
]

df['StationName'] = df['StationName'].str.strip().str.upper()

df['StationID'] = df['StationID'].fillna(999.0)\
    .astype(int).astype(str).replace('999', pd.NA)

df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d %H:%M:%S')

df.sort_values(by=['StationName', 'Date'], inplace=True)

df.reset_index(drop=True, inplace=True)


# %% Save Data to PostgreSQL Database
df.to_sql(
    name="synoptic_data",
    con=engine,
    if_exists="replace",
    index=False
)

# %%
