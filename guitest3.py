import time
import sys
import io
import folium # pip install folium
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView # pip install PyQtWebEngine

"""
Folium in PyQt5
"""
class MyApp(QWidget):
    webView = object()
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Folium in PyQt Example')
        self.window_width, self.window_height = 1600, 900
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        coordinate = (0, 0)
        m = folium.Map(
        	
        	zoom_start=8,
        	location=coordinate
        )
        group_1 = folium.FeatureGroup("first group").add_to(m)
        folium.Marker((0, 0), icon=folium.Icon("red") ,popup="Flight no XYZ Altitude:32794, Latitude:412387").add_to(group_1)
        folium.Marker((1, 0), icon=folium.Icon("red")).add_to(group_1)
        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        self.webView = QWebEngineView()
        self.webView.setHtml(data.getvalue().decode())
        layout.addWidget(self.webView)
    def setView(self,input):
        self.webView.setHtml(input)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet('''
        QWidget {
            font-size: 35px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()
    #time.sleep(10)
    #myApp.setView("sdflkjaf")
    

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')