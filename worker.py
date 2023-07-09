from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from time import sleep, time
import qdarkstyle, sys, os
import logging
logging.basicConfig(format='%(levelname)s:%(name)s:%(lineno)s:  %(message)s', level=logging.DEBUG)


class Worker(QObject):
    _sig = pyqtSignal(str)

    def __init__(self):
        super(Worker, self).__init__()

    @pyqtSlot(bool)
    def func(self, flag):
        print(flag)