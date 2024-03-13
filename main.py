import time
import sys
import io
import folium  # pip install folium
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView  # pip install PyQtWebEngine
import time

import folium
import requests
import json
import pandas as pd
from datetime import datetime

from PlaneData import PlaneData
"""
Folium in PyQt5
"""
kw = {"prefix": "fa", "color": "green", "icon": "plane"}
iconsList = [] # have each icon for a plane. plane_data and this correspond to the same index i.iconsList = [] # have each icon for a plane. plane_data and this correspond to the same index i.
plane_data = {}
isPlaneNew=False
location = [40, 35]
plane_instance=None

m = folium.Map(location=location, zoom_start=6)
class MyApp(QWidget):
    webView = object()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600, 900
        self.setMinimumSize(self.window_width, self.window_height)

        timer = QTimer(self)
        timer.timeout.connect(self.update_map)
        timer.start(5000)  # Update map every 5 seconds (5000 milliseconds)

        layout = QVBoxLayout()
        self.setLayout(layout)



        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        layout.addWidget(self.webView)

    def setView(self, input):
        self.webView.setHtml(input)
    def update_map(self):
        # REST API QUERY
        url_data = "https://betulls:481projesi@opensky-network.org/api/states/all?lamin=35.902&lomin=25.909&lamax=42.026&lomax=44.574"
        response = requests.get(url_data).json()

        # LOAD TO PANDAS DATAFRAME
        col_name = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'long', 'lat',
                    'baro_altitude',
                    'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi',
                    'position_source']

        data = response['states']

        for i in range(len(data)):

            if data[i][0] not in plane_data:
                plane_instance = PlaneData(data[i][0], data[i][1], data[i][3], data[i][4], data[i][5],
                                           data[i][6], data[i][7], data[i][8], data[i][9], data[i][10], data[i][11],
                                           data[i][12])

                plane_data[data[i][0]] = plane_instance

            else:
                if data[i][8]:
                    plane_data.pop(data[i][0])  # on_ground true olunca silinir
                else:
                    plane_data[data[i][0]].update_data(data[i][6], data[i][5], data[i][7], data[i][8], data[i][9],
                                                       data[i][10])

            if plane_data[data[i][0]].true_track is None:
                plane_data[data[i][0]].true_track = 180  # default
            angle = int(plane_data[data[i][0]].true_track)
            icon = folium.Icon(angle=angle, **kw)

            folium.Marker(location=[float(data[i][6]), float(data[i][5])], icon=icon,
                          tooltip="Sign:" + plane_data[data[i][0]].callsign + " Icao24: " + plane_data[data[i][0]].icao24 + " angle: " + str(
                              plane_data[data[i][0]].true_track)).add_to(m)

        flight_df = pd.DataFrame(data)
        flight_df = flight_df.loc[:, 0:16]
        flight_df.columns = col_name
        flight_df = flight_df.fillna('No Data')  # replace NAN with No Data

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        # flight_df = flight_df.sort_values(by='time_position')
        # print(flight_df)
        print(flight_df[['icao24', 'callsign', 'time_position', 'true_track']])
        data = io.BytesIO()
        m.save(data, close_file=False)
        print("***")

        self.webView.setHtml(data.getvalue().decode())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    myApp = MyApp()
    myApp.show()


    # time.sleep(10)
    # myApp.setView("sdflkjaf")

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')