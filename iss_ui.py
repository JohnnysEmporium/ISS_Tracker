import sys, os, requests, time, threading

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *


class WebEnginePage(QWebEnginePage):

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        print("javaScriptConsoleMessage: ", level, message, lineNumber, sourceID)


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("ISS Tracker")
        MainWindow.resize(977, 710)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 977, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.browser()
        self.buttons()
            
    def buttons(self):
        self.button_focus = QtWidgets.QPushButton('Set Focus')
        self.button_focus.setCheckable(True)
        self.button_focus.setChecked(True)
        self.gridLayout.addWidget(self.button_focus)
            
    def browser(self):
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "map.html"))
        local_url = QUrl.fromLocalFile(file_path)
        self.web = QWebEngineView(self.centralwidget)
#         console logging
        self.web.setPage(WebEnginePage(self.web))
        self.gridLayout.addWidget(self.web)
        self.web.load(local_url)    
        self.frame = self.web.page()
        
    def get_iss_pos(self):
        response = requests.get('http://api.open-notify.org/iss-now.json')
        response = response.json()
        lat = str(response['iss_position']['latitude'])
        lon = str(response['iss_position']['longitude'])
        return lat, lon
    
    def get_iss_pass_times(self, lat, lon):
        response = requests.get('http://api.open-notify.org/iss-pass.json?lat={}&lon={}'.format(lat, lon))
        response = response.json()

    def create_marker(self):
        while True:
            if not EXIT_SIGNAL:
                try:
					print('lecimyyyyyy')
                    lt, lg = self.get_iss_pos()
                    marker = 'addISSMarker({},{})'.format(lt, lg)
                    self.frame.runJavaScript(marker)
                    time.sleep(5)
                    
                    if self.button_focus.isChecked():
                        goTo = 'goTo({},{})'.format(lt, lg)
                        self.frame.runJavaScript(goTo)     
                    
                except:
                    pass
            else:
                break

    
def _exit():
    global EXIT_SIGNAL
    EXIT_SIGNAL = True
    thread.join()


EXIT_SIGNAL = False    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    thread = threading.Thread(target=ui.create_marker)
    app.
    MainWindow.show()

    sys.exit(app.exec_())

# app.onsignalexit connect czy cos takiego 
# ZROBIC ISS PASS TIMES I PEOPLE IN SPACE Z http://api.open-notify.org/, dodac info o predkosci
