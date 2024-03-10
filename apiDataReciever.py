# IMPORTING LIBRARY
import time

import folium
import requests
import json
import pandas as pd
from datetime import datetime

from PlaneData import PlaneData

kw = {"prefix": "fa", "color": "green", "icon": "plane"}
iconsList = [] # have each icon for a plane. plane_data and this correspond to the same index i.iconsList = [] # have each icon for a plane. plane_data and this correspond to the same index i.
plane_data = {}
isPlaneNew=False
location=[41,-71]
plane_instance=None
m = folium.Map(location=location, zoom_start=2) # update later
while( True ):
    # REST API QUERY
    url_data = "https://betulls:481projesi@opensky-network.org/api/states/all?lamin=35.902&lomin=25.909&lamax=42.026&lomax=44.574"
    response = requests.get(url_data).json()

    # LOAD TO PANDAS DATAFRAME
    col_name = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'long', 'lat', 'baro_altitude',
                'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi',
                'position_source']

    data = response['states']

    for i in range(len(data)):

        if data[i][0] not in plane_data:
            plane_instance = PlaneData(data[i][0],data[i][1],data[i][3],data[i][4],data[i][5],
                                   data[i][6],data[i][7],data[i][8],data[i][9],data[i][10],data[i][11],data[i][12])

            plane_data[data[i][0]] = plane_instance

        else:
            if data[i][8]:
                plane_data.pop(data[i][0]) # on_ground true olunca silinir
            else:
                plane_data[data[i][0]].update_data(data[i][6], data[i][5], data[i][7], data[i][8], data[i][9], data[i][10])


        if plane_instance.true_track==None:
            plane_instance.true_track=180 # default
        angle=int(plane_instance.true_track)
        icon = folium.Icon(angle=angle, **kw)

        folium.Marker(location=[float(data[i][6]),float(data[i][5])], icon=icon,
                          tooltip="Sign:" + plane_instance.callsign + " Icao24: " + plane_instance.icao24 +" angle: " +str(plane_instance.true_track)).add_to(m)



    flight_df = pd.DataFrame(data)
    flight_df = flight_df.loc[:, 0:16]
    flight_df.columns = col_name
    flight_df = flight_df.fillna('No Data')  # replace NAN with No Data

    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # flight_df = flight_df.sort_values(by='time_position')
    # print(flight_df)
    print(flight_df[['icao24', 'callsign', 'time_position', 'true_track']])
    m.save("mapimiz.html")
    print("***")
    time.sleep(5)

    """
            date = datetime.utcfromtimestamp(data[i][3])
            data[i][3] = date.strftime("%Y-%m-%d %H:%M:%S UTC")
            date = datetime.utcfromtimestamp(data[i][4])
            data[i][4] = date.strftime("%Y-%m-%d %H:%M:%S UTC")
    """