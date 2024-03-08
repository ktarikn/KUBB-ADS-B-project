# IMPORTING LIBRARY
import time

import requests
import json
import pandas as pd
from datetime import datetime

from PlaneData import PlaneData

plane_data = []
plane_icao4_data = []
while( True ):
    # REST API QUERY
    url_data = "https://betulls:481projesi@opensky-network.org/api/states/all?lamin=35.902&lomin=25.909&lamax=42.026&lomax=44.574"
    response = requests.get(url_data).json()

    # LOAD TO PANDAS DATAFRAME
    col_name = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'long', 'lat', 'baro_altitude',
                'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi',
                'position_source']

    data = response['states']  # time ve states

    # Convert unix timestamps to a human-readable format
    for i in range(len(data)):

        plane_instance = PlaneData(data[i][0],data[i][1],data[i][3],data[i][4],data[i][5],
                                   data[i][6],data[i][7],data[i][8],data[i][9],data[i][11],data[i][12])

        if plane_instance.icao24 not in plane_icao4_data:
            plane_data.append(plane_instance)
            plane_icao4_data.append(plane_instance.icao24)


    flight_df = pd.DataFrame(data)
    flight_df = flight_df.loc[:, 0:16]
    flight_df.columns = col_name
    flight_df = flight_df.fillna('No Data')  # replace NAN with No Data

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # flight_df = flight_df.sort_values(by='time_position')
    # print(flight_df)
    print(flight_df[['icao24', 'callsign', 'time_position']])
    print("***")
    time.sleep(5)

    """
            date = datetime.utcfromtimestamp(data[i][3])
            data[i][3] = date.strftime("%Y-%m-%d %H:%M:%S UTC")
            date = datetime.utcfromtimestamp(data[i][4])
            data[i][4] = date.strftime("%Y-%m-%d %H:%M:%S UTC")
    """