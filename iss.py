from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtCore import QUrl
import sys, os, requests, time

class Ui_main():
    
    def __init__(self):
        self.web = QWebEngineView()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.web.load(local_url)
        self.web.show()
        
        

    def get_iss_pos(self):
        response = requests.get('http://api.open-notify.org/iss-now.json')
        response = response.json()
        self.lat = response['iss_position']['latitude']
        self.lon = response['iss_position']['longitude']
        frame = self.web.page()
        frame.runJavaScript('alert("wielkie dupsko")')

    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Ui_main()
    time.sleep(5)
    Ui_main().get_iss_pos()
    sys.exit(app.exec_())