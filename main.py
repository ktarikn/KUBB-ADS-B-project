import sys
import io
import time

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton , QLabel,QSizePolicy
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QFont
import folium
import requests
import pandas as pd
import numpy as np

from PlaneData import PlaneData
from folium import plugins

#icon types
kw = {"prefix": "fa", "color": "green", "icon": "plane"}
uk = {"prefix": "fa", "color": "gray", "icon": "question-circle"}
se = {"prefix": "fa", "color": "red", "icon": "medkit"}
ob = {"prefix": "fa", "color": "gray", "icon": "exclamation-triangle"}

plane_data = {}
location = [40, 35]
plane_instance=None

#n = folium.Map(location=location, zoom_start=6)
class MyApp(QWidget):
    webView = object()

    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        
        
        self.setLayout(hbox)
        
        self.window_width, self.window_height = 1800, 900
        self.setMinimumSize(self.window_width, self.window_height)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_map)
        self.timer.start(5000)  # Update map every 5 seconds (5000 milliseconds)

        self.m = folium.Map(location=location, zoom_start=6, zoom_control=False, scrollWheelZoom=False)
        # save map data to data object
        map_data = io.BytesIO()
        self.m.save(map_data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(map_data.getvalue().decode())
        hbox.addWidget(self.webView)
        hbox.addLayout(vbox)
        """
        explanation = QLabel()
        explanation.setMaximumWidth(200)
        explanation.setWordWrap(True)
        
        explanation.setText("If you click 'Stop', the map won't update but you can zoom")
        explanation.setFont(QFont("Aerial",8))
        vbox.addWidget(explanation)
        """
        self.stopped = False
        self.button = QPushButton()
        self.button.setMaximumWidth(250)
        self.button.setText("Stop to zoom")
        self.button.clicked.connect(self.action)
        vbox.addWidget(self.button)
        
        # to avoid waiting 5 seconds for the initial map to fully load
        self.update_map()

    def action(self):
        if not self.stopped:
            self.stopped = True
            self.button.setText("Go Live")
            self.timer.stop()

            self.m.options.update({
                'scrollWheelZoom': True
            })
            map_data = io.BytesIO()
            self.m.save(map_data, close_file=False)
            self.webView.setHtml(map_data.getvalue().decode())
        else:
            self.stopped = False
            self.button.setText("Stop to zoom")
            self.m.options.update({
                'scrollWheelZoom': False
            })
            map_data = io.BytesIO()
            self.m.save(map_data, close_file=False)
            self.webView.setHtml(map_data.getvalue().decode())
            self.update_map()
            self.timer.start(5000)

    def setView(self, input):
        self.webView.setHtml(input)

    def update_map(self):
        # REST API QUERY
        
        self.m = folium.Map(location=location, zoom_start=6, zoom_control=False, scrollWheelZoom=False)
        url_data = "https://betulls:481projesi@opensky-network.org/api/states/all?lamin=35.902&lomin=25.909&lamax=42.026&lomax=44.574&extended=1"
        response = requests.get(url_data).json()
        marker_group = folium.FeatureGroup(name="Markers")
       
        self.m.add_child(marker_group)

        # LOAD TO PANDAS DATAFRAME
        col_name = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'long', 'lat',
                    'baro_altitude',
                    'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi',
                    'position_source', 'category']

        data = response['states']

        for i in range(len(data)):

            if data[i][0] not in plane_data:
                plane_instance = PlaneData(data[i][0], data[i][1], data[i][3], data[i][5],
                                           data[i][6], data[i][8], data[i][9], data[i][10], data[i][17])
                plane_data[data[i][0]] = plane_instance
            else:
                if data[i][8]:
                    plane_data.pop(plane_data[data[i][0]].icao24)  # delete when on_ground is true
                    continue
                else:
                    plane_data[data[i][0]].update_data(data[i][5], data[i][6], data[i][8], data[i][9],
                                                       data[i][10])

            curr_plane = plane_data[data[i][0]]
            if curr_plane.true_track is None:
                curr_plane.true_track = 180  # default

            angle = int(curr_plane.true_track+90)
            icon = folium.Icon(angle=angle, **kw)

            if curr_plane.category and curr_plane.category >=0 and curr_plane.category <= 1:
                icon = folium.plugins.BeautifyIcon(
                    icon='question-circle',
                    border_color='transparent',
                    background_color='transparent',
                    border_width=1,
                    text_color='#003EFF',
                    inner_icon_style='color: gray; margin:0px;font-size:2em;transform: rotate({0}deg);'.format(angle)
                )
            elif curr_plane.category and curr_plane.category >=2 and curr_plane.category <= 15:
                icon = folium.plugins.BeautifyIcon(
                    icon='plane',
                    border_color='transparent',
                    background_color='transparent',
                    border_width=1,
                    text_color='#003EFF',
                    inner_icon_style='color: #4829d6; margin:0px;font-size:2em;transform: rotate({0}deg);'.format(angle)
                )
            elif curr_plane.category and curr_plane.category >= 16 and curr_plane.category <= 17:
                icon = folium.plugins.BeautifyIcon(
                    icon='medkit',
                    border_color='transparent',
                    background_color='transparent',
                    border_width=1,
                    text_color='#003EFF',
                    inner_icon_style='color: red; margin:0px;font-size:2em;transform: rotate({0}deg);'.format(angle)
                )
            elif curr_plane.category and curr_plane.category >= 18 and curr_plane.category <= 20:
                icon = folium.plugins.BeautifyIcon(
                    icon='exclamation-triangle',
                    border_color='transparent',
                    background_color='transparent',
                    border_width=1,
                    text_color='#003EFF',
                    inner_icon_style='color: yellow; margin:0px;font-size:2em;transform: rotate({0}deg);'.format(angle)
                )
            else :
                icon = folium.plugins.BeautifyIcon(
                    icon='plane',
                    border_color='transparent',
                    background_color='transparent',
                    border_width=1,
                    text_color='#003EFF',
                    inner_icon_style='color: #2a1780; margin:0px;font-size:2em;transform: rotate({0}deg);'.format(angle)
                )

            folium.Marker(
                location=[float(curr_plane.latitude), float(curr_plane.longitude)],
                icon=icon,
                tooltip="Sign:" + curr_plane.callsign + " Icao24: " + curr_plane.icao24 + " angle: " + str(
                    curr_plane.true_track)
            ).add_to(marker_group)


            """
            a = folium.Marker(location=[float(curr_plane.latitude), float(curr_plane.longitude)], icon=icon,
                          tooltip="Sign:" + curr_plane.callsign + " Icao24: " + curr_plane.icao24 + " angle: " + str(
                              curr_plane.true_track)).add_to(marker_group)
            """
        
            folium.PolyLine(
                    locations=[((curr_plane).location_history)[:curr_plane.idx]],
                    color="blue",
                    tooltip="previous path",
                    weight=3,
                ).add_to(self.m)
        #    print(curr_plane.location_history)

        # Setting up the dataframe
        flight_df = pd.DataFrame(data)
        flight_df = flight_df.loc[:, 0:17]
        flight_df.columns = col_name
        flight_df = flight_df.fillna('No Data')  # replace NAN with No Data
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)

        print(flight_df[['icao24', 'callsign', 'time_position', 'true_track']])

        map_data = io.BytesIO()
        self.m.save(map_data, close_file=False)
        print("***")
        self.webView.setHtml(map_data.getvalue().decode())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')
