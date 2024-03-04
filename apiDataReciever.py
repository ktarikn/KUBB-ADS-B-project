# IMPORTING LIBRARY
import requests
import json
import pandas as pd
from datetime import datetime

# REST API QUERY
url_data = "https://betulls:481projesi@opensky-network.org/api/states/all?lamin=35.902&lomin=25.909&lamax=42.026&lomax=44.574"
response = requests.get(url_data).json()

# LOAD TO PANDAS DATAFRAME
col_name = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'long', 'lat', 'baro_altitude',
            'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi',
            'position_source']

data = response['states']

# Convert unix timestamps to a human-readable format
for i in range(len(data)):
    date = datetime.utcfromtimestamp(data[i][3])
    data[i][3] = date.strftime("%Y-%m-%d %H:%M:%S UTC")

flight_df = pd.DataFrame(data)
flight_df = flight_df.loc[:, 0:16]
flight_df.columns = col_name
flight_df = flight_df.fillna('No Data')  # replace NAN with No Data

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

flight_df = flight_df.sort_values(by='time_position')
print(flight_df)
