
import sys
import io
import folium
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from GUIManager import GUIManager

app = QApplication(sys.argv)
manager = GUIManager()
widgetlist = []


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

webView = QWebEngineView()
webView.setHtml(data.getvalue().decode())
webView.setMinimumSize(800,800)
widgetlist.append(webView)
newlayout = QVBoxLayout()

newlayout.addWidget(QPushButton("fasdf"))
newlayout.addWidget(QLabel("flight no adsf"))

newlayout.addWidget(QCheckBox())
newlayout.addStretch(1)
#widgetlist.append("stretch")
widgetlist.append(newlayout)
for i in widgetlist:
    manager.addwidget(i)






    
manager.show()



try:
    sys.exit(app.exec_())
except SystemExit:
    print('Closing Window...')

