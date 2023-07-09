from PyQt5.QtCore import QObject, QVariant, pyqtSignal, pyqtProperty
import logging
logger = logging.getLogger(__name__)

def ComStructGen( glob, context, className, *args, **kwargs):
    """ Generate a class inheriting from QObject. Interfacing qml/python by a common property mechanism """
    """ glob should be the current globals dictionary (so just call globals() method) """
    """ className is explicit """
    """ Each args should be a tuple of size 3 like: 
    (varName, 
    defValue (to write in the __init__ declaration eg. label="warning"), 
    raiseNotif (connect the notif to a signal 'changed')) """
    args = list(args)
    if not len(args):
        for key, val in kwargs.items():
            args.append((key, val, True))
    toDictFunc = """\n\n    @pyqtSlot(result=QVariant)
    def toDict(self):
        ret = {"""
    toDictFuncClose = """}
        return ret"""
    toDictData = """'varName': self.varName"""

    initArgsToList = """\n\n    @pyqtSlot(result=list)
    def classAttrs(self):
        return listing
        """

    classCodeStart = """class """+className+"""(QObject):
    changed = pyqtSignal()

    @pyqtSlot(result=QVariant)
    def className(self):
        return '"""+className+"""'
    def __init__(self"""

    classCodeEnd = """, parent=None):
        super("""+className+""", self).__init__(parent)"""

    initVars = """\n        self._varName = varName"""

    raiseNotifCode = """\n        self.varNameChanged.connect(self.changed.emit)"""

    PropertyBaseCode = """\n\n    varNameChanged = pyqtSignal()

    @pyqtProperty(QVariant, notify=varNameChanged)
    def varName(self):
        return self._varName

    @varName.setter
    def varName(self, varName):
        if self._varName != varName:
            self._varName = varName
            self.varNameChanged.emit() """
    
    PropertyAppended = ""
    
    initParamKeyWords = ""
    initParam = ""
    listing = []
    for name, defValue, raiseNotif in args:# iterate each args to write the code
        if defValue==None:# then no keyword
            initParam+= ", "+name
        elif type(defValue)==str and not "'" in defValue:# then add single quotation mark and write it as keyword
            initParamKeyWords+= ", "+name+"="+"'"+defValue+"'"
        elif type(defValue)==str:# should have a single quotation mark eg. given arg "'QObject'" then the code writed: QObject
            initParamKeyWords+= ", "+name+"="+defValue.replace("'", "")
        else:# enithing else 
            initParamKeyWords+= ", "+name+"="+str(defValue)
        classCodeEnd+= initVars.replace( "varName", name)
        if raiseNotif:
            classCodeEnd+= raiseNotifCode.replace( "varName", name)
            toDictFunc+= toDictData.replace( "varName", name) + ", "
        PropertyAppended+= PropertyBaseCode.replace( "varName", name)
        listing.append(name)
    initArgsToList = initArgsToList.replace("listing", str(listing))
    classCode= classCodeStart + initParam + initParamKeyWords + classCodeEnd + PropertyAppended + toDictFunc + toDictFuncClose + initArgsToList## concat all code parts
    exec(classCode, glob)# execut so declare the class in the given globals and then it can be called with the className eg. className='toto'; instance=toto()
    logger.info("Generated class '"+className+"' declared.")
    obj = globals()[className]()
    context.setContextProperty("STD", obj)
    return obj