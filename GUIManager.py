

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

class GUIManager(QWidget):
    ElementList = list()
    
    def __init__(self, layout = QHBoxLayout(), sizeY = 1200, sizeX = 1300):
        super().__init__()
        self.webView = QWebEngineView()
        self.setWindowTitle('KUBBs-ADSB')
        self.window_width, self.window_height = sizeY, sizeX
        self.setMinimumSize(self.window_width, self.window_height)
        
        
        self.setLayout(layout)

    def addwidget(self,widget):
        
        if(isinstance(widget,QBoxLayout)):
            self.addLayout(widget)
            return
        self.layout().addWidget(widget)
    def addWidgetWithAlignment(self,widget,align):
        self.layout().addWidget(widget,alignment=align)
    def getLayout(self):
        return self.layout
    def addLayout(self,lay):
        
        cur_layout = self.layout()
        if(isinstance(cur_layout,QBoxLayout)):
            cur_layout.addLayout(lay)
    
   
