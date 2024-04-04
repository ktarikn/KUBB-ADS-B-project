import sys
import io
import traceback
from PyQt5 import QtWidgets
import Simdemo
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSizePolicy, \
    QLineEdit, QDesktopWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
from folium import plugins
import requests
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from PlaneData import PlaneData

#icon types
kw = {"prefix": "fa", "color": "green", "icon": "plane"}
uk = {"prefix": "fa", "color": "gray", "icon": "question-circle"}
se = {"prefix": "fa", "color": "red", "icon": "medkit"}
ob = {"prefix": "fa", "color": "gray", "icon": "exclamation-triangle"}

plane_data = {}

plane_instance=None

#n = folium.Map(location=location, zoom_start=6)

class WelcomeWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Welcome to KUBB's project demo :3")
        self.resize(700, 350)  # Pencere boyutunu ayarla
        self.center()  # Pencereyi ekranın ortasına konumlandır

        layout = QVBoxLayout(self)

        # Açıklama metni
        label = QLabel("Welcome to the KUBBs-ADSB Project!\nYou can pursue Icaos to zoom on planes.\nZooming on them will allow you to see its previous location graph.", self)
        label.setAlignment(Qt.AlignCenter)  # Metni yatayda ortala
        layout.addWidget(label)

        # Düğme
        self.enter_button = QPushButton("Enter", self)
        self.enter_button.clicked.connect(self.showMainScreen)
        layout.addWidget(self.enter_button, alignment=Qt.AlignCenter)  # Düğmeyi yatayda ortala

    def center(self):
        # Pencereyi ekranın ortasına konumlandır
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)


    def showMainScreen(self):
        self.hide()  # WelcomeWindow penceresini gizle
        self.main_window = MyApp()  # MyApp penceresini oluştur
        self.main_window.show()  # MyApp penceresini göster

class MyApp(QWidget):
    webView = object()
    def __init__(self):
        super(MyApp, self).__init__()
        self.zoom_start= 6
        self.location = [40, 35]
        self.pursued=False
        self.pursuedPlane=""
        self.simulated = False
        self.data = data = []
        self.setWindowTitle('Folium in PyQt Example')
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        
        self.setStyleSheet("background-color: #e5e6eb;") # light gray
        self.setLayout(hbox)
        
        self.window_width, self.window_height = 1800, 900
        self.setMinimumSize(self.window_width, self.window_height)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_map)
        self.timer.start(5000)  # Update map every 5 seconds (5000 milliseconds)

       

        self.m = folium.Map(location=self.location, zoom_start=6, zoom_control=False, scrollWheelZoom=False)
        # save map data to data object
        map_data = io.BytesIO()
        self.m.save(map_data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(map_data.getvalue().decode())
        hbox.addWidget(self.webView)
        hbox.addLayout(vbox)
        """
        
        
        self.icaoLabel = QLabel()
        self.icaoLabel.setText()
        """

        # b1b3bd, hover a1a3ad, pressed 9799a1, text 46464a original gray colors for buttons
        line_style = """
                        QLineEdit {
                            background-color: #f0f0f0; 
                            border: 2px solid #f0f0f0; 
                            border-radius: 10px;
                            padding: 15px 32px;
                            color: #46464a; 
                            font-size: 28px;
                            text-align: center;
                        }
                        ::placeholder { text-align: center; }
                    """

        self.icaoInput = QLineEdit()
        self.icaoInput.setStyleSheet(line_style)
        self.icaoInput.setPlaceholderText("Enter Icao")
        self.icaoInput.setMaximumWidth(250)
        vbox.addWidget(self.icaoInput)
        self.icaobutton = QPushButton()
        self.icaobutton.setStyleSheet("""
                        QPushButton {
                            background-color: #FF343C;
                            border: none;
                            color: #641518;
                            padding: 15px 32px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 28px;
                            margin: 4px 2px;
                            cursor: pointer;
                            border-radius: 10px;
                        }
                        QPushButton:hover {
                            background-color: #D82D33;
                        }
                        QPushButton:pressed {
                            background-color: #C82A30; 
                        }
                    """)
        self.icaobutton.clicked.connect(self.pursueIcao)
        self.icaobutton.setText("PursueIcao")
        vbox.addWidget(self.icaobutton)

        self.simbutton = QPushButton()
        self.simbutton.setStyleSheet("""
                        QPushButton {
                            background-color: #0DBBBB;
                            border: none;
                            color: #005252;
                            padding: 15px 32px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 28px;
                            margin: 4px 2px;
                            cursor: pointer;
                            border-radius: 10px;
                        }
                        QPushButton:hover {
                            background-color: #03A6A6;
                        }
                        QPushButton:pressed {
                            background-color: #019393; 
                        }
                    """)
        self.simbutton.clicked.connect(self.simulate)
        self.simbutton.setText("Simulate")
        vbox.addWidget(self.simbutton)

        self.stopped = False
        self.button = QPushButton()
        self.button.setStyleSheet("""
                        QPushButton {
                            background-color: #86B75F;
                            border: none;
                            color: #41582E;
                            padding: 15px 32px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 28px;
                            margin: 4px 2px;
                            cursor: pointer;
                            border-radius: 10px;
                        }
                        QPushButton:hover {
                            background-color: #7FAC5B;
                        }
                        QPushButton:pressed {
                            background-color: #70994F; 
                        }
                    """)
        self.button.setMaximumWidth(250)
        self.button.setText("Stop to zoom")
        self.button.clicked.connect(self.action)
        vbox.addWidget(self.button)
        
        # to avoid waiting 5 seconds for the initial map to fully load
        self.update_map()

    def simulate(self):
        if(self.simulated):
            self.simulated=False
            self.simbutton.setText("Simulate")
        else:
            self.simulated=True
            self.simbutton.setText("Stop Sim")
    def pursueIcao(self):
        
        if(not self.pursued):

            if(self.icaoInput.text() in plane_data):
                
                self.zoom_start=11
                self.pursuedPlane = self.icaoInput.text()
                #self.location=[float(plane_data[self.icaoInput.text()].latitude),float(plane_data[self.icaoInput.text()].longitude)]
                self.pursued=True
                self.icaobutton.setText("Unpursue")
                try:
                    plt.title("Longitude and Latitude Coordinates")
                    plt.xlabel("latitude")
                    plt.ylabel("longitude") #arrayin [][0] ' ı latitude tutyoruz. diğeri de longtitu' tutyor
                    idx = plane_data.get(self.icaoInput.text()).idx
                    latitude = [plane_data.get(self.icaoInput.text()).location_history[:idx,0]]
                    longitude = [plane_data.get(self.icaoInput.text()).location_history[:idx, 1]]
                    plt.plot(latitude,longitude,marker='o',linestyle="-")
                    plt.grid(True)
                    plt.show()
                except Exception:
                    print(traceback.format_exc())

        else:
            self.zoom_start=6
            self.location = [40,35]
            self.icaobutton.setText("Pursue")
            self.pursued=False
            
    
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
        if(self.pursued and self.pursuedPlane in plane_data):
            self.location=[float(plane_data[self.pursuedPlane].latitude),float(plane_data[self.pursuedPlane].longitude)]
        self.m = folium.Map(location=self.location, zoom_start=self.zoom_start, zoom_control=False, scrollWheelZoom=False)
        url_data = "https://betulls:481projesi@opensky-network.org/api/states/all?lamin=35.902&lomin=25.909&lamax=42.026&lomax=44.574&extended=1"
        response = requests.get(url_data).json()
        marker_group = folium.FeatureGroup(name="Markers")
       
        self.m.add_child(marker_group)

        # LOAD TO PANDAS DATAFRAME
        col_name = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 'long', 'lat',
                    'baro_altitude',
                    'on_ground', 'velocity', 'true_track', 'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi',
                    'position_source', 'category']

        self.data = response['states']

        


        for i in range(len(self.data)):

            if self.data[i][0] not in plane_data:
                plane_instance = PlaneData(self.data[i][0], self.data[i][1], self.data[i][3], self.data[i][5],
                                           self.data[i][6], self.data[i][8], self.data[i][9], self.data[i][10], self.data[i][17])
                plane_data[self.data[i][0]] = plane_instance
            else:
                if self.data[i][8]:
                    plane_data.pop(plane_data[self.data[i][0]].icao24)  # delete when on_ground is true
                    continue
                else:
                    plane_data[self.data[i][0]].update_data(self.data[i][5], self.data[i][6], self.data[i][8], self.data[i][9],
                                                       self.data[i][10])

            curr_plane = plane_data[self.data[i][0]]
            if curr_plane.true_track is None:
                curr_plane.true_track = 180  # default

            angle = int(curr_plane.true_track-90)
            icon = folium.Icon(angle=angle, **kw)
            
            buf = 8-len(curr_plane.icao24)
            
               

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
                    inner_icon_style='color: #4A4F4F; margin:0px;font-size:2em;transform: rotate({0}deg);'.format(angle)
                )
            if(not self.simulated):
                folium.Marker(
                    location=[float(curr_plane.latitude), float(curr_plane.longitude)],
                    icon=icon,
                    tooltip="Sign:" + curr_plane.callsign + " Icao24: " + curr_plane.icao24 + " angle: " + str(
                        curr_plane.true_track)
                ).add_to(marker_group)


                folium.PolyLine(
                        locations=[((curr_plane).location_history)[:curr_plane.idx]],
                        color="blue",
                        tooltip="previous path",
                        weight=3,
                    ).add_to(self.m)
            else:
                folium.Marker(
                    location=[float(curr_plane.simulatedLatitude), float(curr_plane.simulatedLongitude)],
                    icon=icon,
                    tooltip="Sign:" + curr_plane.callsign + " Icao24: " + curr_plane.icao24 + " angle: " + str(
                        curr_plane.true_track)
                ).add_to(marker_group)


                folium.PolyLine(
                        locations=[((curr_plane).simulation_history)[:curr_plane.idx]],
                        color="blue",
                        tooltip="previous path",
                        weight=3,
                    ).add_to(self.m)
        #    print(curr_plane.location_history)

        # Setting up the dataframe
        flight_df = pd.DataFrame(self.data)
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
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())
