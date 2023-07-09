
import sys, os
import logging
logging.basicConfig(format="%(levelname)-s - %(filename)-s %(lineno)-s in %(funcName)s(): %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)
from PyQt5.QtCore import QObject, pyqtSlot, QVariant, QUrl, pyqtSignal, QThread, pyqtProperty, QAbstractListModel
from PyQt5.QtWidgets import QApplication, QFileDialog 
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtQuick import QQuickImageProvider
from PyQt5.QtGui import QPixmap, QImage
import pickle
from structGen import ComStructGen

from time import time

## list dir tree filtered by extention
def listFileTree(rootPath=None, ext="", excludedFiles=[]):
    """ list all files from a root directory (top dir) to the last (bottom dir) which has the given extention """
    """ rootPath: str or None"""
    """ ext: [str, str, ...] or str """
    if type(ext)!=list:
        ext = [ext]
    ret = []
    if rootPath==None:
        rootPath = "."
    for root, dirs, files in os.walk(rootPath, topdown=False):
        for name in files:
            if name.split(".")[-1] in ext and not name in excludedFiles:
                if root.startswith(".\\"):
                    root = root[2:]
                if not root=="":
                    ret.append(os.path.join(root, name))
                else:
                    if name.startswith(".\\"):
                        name = name[2:]
                    ret.append( name)
    return ret

def QrcWrite(rootPath=None, ext=["qml", "png", "qmldir"], fileName="qml_rc", asPy=True, rmQrcIfPy=True, excludedFiles=[]):
    """ generate (filtered by givens ext) a tree file to write the qrc file and convert it to py file """
    if rootPath:
        qrcPath = os.path.join(rootPath, fileName+".qrc")
    else:
        qrcPath = fileName+".qrc"
    files = listFileTree(rootPath=rootPath, ext=ext, excludedFiles=excludedFiles)
    qrcFile = open( qrcPath, "w")
    qrcBeginsLines = """<RCC>
      <qresource prefix="/">"""
    qrcEndsLines = """
      </qresource>
  </RCC>"""
    qrcFileHeader = """
          <file>filePath</file>"""
    qrcFile.write(qrcBeginsLines)
    for file in files:
        qrcFile.write(qrcFileHeader.replace("filePath", file))
    qrcFile.write(qrcEndsLines)
    qrcFile.close()
    if asPy:
        if rootPath:
            os.system('pyrcc5 -o "'+os.path.join(rootPath, fileName+".py")+'" "'+qrcPath+'"')
        else:
            os.system('pyrcc5 -o "'+fileName+".py"+'" "'+qrcPath+'"')
        if rmQrcIfPy:
            os.remove(qrcPath)

def QmldirWrite(rootPath=None, excludedFiles=[]):
    """ generate the qml tree file to write the qmldir file """
    files = listFileTree(rootPath=rootPath, ext="qml", excludedFiles=excludedFiles)
    if rootPath:
        qmldirFile = open(os.path.join(rootPath, "qmldir"), "w")
    else:
        qmldirFile = open("qmldir", "w")
    for file in files:
        qmldirFile.write(os.path.basename(file).replace(".qml", " "+file)+"\n")
    qmldirFile.close()

pyinstallerEXE = sys.argv[0].endswith(".exe")
if not pyinstallerEXE:
    import winsound
    QrcWrite(rootPath=None, ext=["qml", "png", "qmldir"], fileName="qmlResources", rmQrcIfPy=False)
    QmldirWrite(rootPath=None)
    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)
import qmlResources 

class worker(QObject):
    def __init__(self):
        super(QObject, worker).__init__(self)
            


class MainApp(QObject):
    def __init__(self, engine, ctx):
        ###
        self.worker = worker()
        self.wThread = QThread()
        self.worker.moveToThread(self.wThread)
        self.wThread.start()
        ###

        self.STD = ComStructGen(globals(), "STD", colorBack="#424242",
                                                    colorMiddle="#222222",
                                                    colorFore="#333333",
                                                    colorHovered="#7ddfff",
                                                    colorSelected="#ffe066",
                                                    margins=4,
                                                    AppWidth=1500,
                                                    AppHeight=850,
                                                    AppTitle="Python Applications Installer",
                                                    out="")
        ###
        engine.load(QUrl('qrc:/main.qml'))
        win = engine.rootObjects()[0]
        ###
        super(MainApp, self).__init__(win)
        ###
        self.win = win
        self.ctx = ctx
        win.show()

    def closeEvent(self, event):
        self.wThread.terminate()
        event.accept()

    @pyqtSlot(QVariant, QVariant, QVariant)
    def setProp(self, objName, prop, value):
        # Set a qml property of an object
        self.win.findChild(QObject, str(objName)).setProperty(str(prop), value)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("freeHand")
    app.setOrganizationDomain("None")
    app.setApplicationName("PyApps Installer")
    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    py_mainapp = MainApp(engine, ctx)
    sys.exit(app.exec())