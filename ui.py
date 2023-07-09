from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QFrame, QLabel, QTableWidgetItem, QGridLayout
from PyQt5.QtGui import QPixmap, QBrush, QColor, QIcon, QPalette
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QThread, QPoint, QRectF, QSize, Qt, QTimer
from time import sleep, time
from worker import Worker
import qdarkstyle, sys, os
import logging
logging.basicConfig(format='%(levelname)s:%(name)s:%(lineno)s:  %(message)s', level=logging.DEBUG)

gen = 1
if __name__ == '__main__':
    if gen:
        os.system("pyuic5 -x designer.ui -o designer_ui.py")
        os.system("pyrcc5 images.qrc -o images_rc.py")
import designer_ui

class MainUi(QMainWindow, designer_ui.Ui_MainWindow):

    def __init__(self, parent=None):
        logging.info("start init")
        self.app = QApplication(sys.argv)
        logging.info("app ok")
        super(MainUi, self).__init__(parent)
        logging.info("super ok")
        self.setupUi(self)
        logging.info("setup ui ok")
        self.main()

    def closeEvent(self, event):
        logging.info("App exit")
        self.thread.terminate()
        event.accept()
        logging.info("closed")

    def main(self):
        self.app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
        
        # Thread
        self.worker = Worker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.start()
        logging.info("start worker")
        self.show()
        logging.info("show")
        sys.exit(self.app.exec_())

    def FileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(
            self, "QFileDialog.getOpenFileName()", "", "All Files (*);;Python Files (*.)", options=options)
        if fileName:
            return fileName
        else:
            return None

    def saveFileDialog(self, defpath=""):

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        my_dir = QFileDialog.getSaveFileName(
            self, 'Save as', defpath, options=options)
        if my_dir:
            return my_dir
        else:
            return None

    def DirDialog(self, defpath=""):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        options |= QFileDialog.ShowDirsOnly
        my_dir = QFileDialog.getExistingDirectory(
            self, 'Select directory', defpath, options=options)
        if my_dir:
            return my_dir
        else:
            return None

    def setStatusTips(self, text, t=1000):
        self.statusBar().showMessage(text, t)


if __name__ == "__main__":
    a = MainUi()