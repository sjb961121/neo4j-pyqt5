import os
import sys

d = os.path.dirname(__file__)
__path = os.path.dirname(d)
sys.path.append(__path) # 添加自己指定的搜索路径

import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtGui import QPixmap, QGuiApplication
from PyQt5.QtCore import Qt, QUrl, QEvent,QObject,pyqtSignal,pyqtSlot
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebChannel import *

import py2neo


from mypy2neo import search
from gui.my import Ui_Form
from myLib import myLib




class channel_showNode(QObject):
    fromJS = pyqtSignal(str)
    toJS = pyqtSignal(str)
    def __init__(self, parent = None):
        super().__init__(parent)

    @pyqtSlot(str)
    def JSSendMessage(self, strParameter):
        print('showNode(%s) from Html' %strParameter)
        self.fromJS.emit(strParameter)

class channel_expandNode(QObject):
    fromJS = pyqtSignal(str)
    toJS = pyqtSignal(str)
    def __init__(self, parent = None):
        super().__init__(parent)

    @pyqtSlot(str)
    def JSSendMessage(self, strParameter):
        print('expandNode(%s) from Html' %strParameter)
        self.fromJS.emit(strParameter)

class channel_showPicPro(QObject):
    fromJS = pyqtSignal(str)
    toJS = pyqtSignal(str)
    def __init__(self, parent = None):
        super().__init__(parent)

    @pyqtSlot(str)
    def JSSendMessage(self, strParameter):
        print('showPicPro(%s) from Html' %strParameter)
        self.fromJS.emit(strParameter)


class neo4j(QtWidgets.QWidget):
    ToJS_showNode = pyqtSignal(str)
    ToJS_expandNode = pyqtSignal(str)
    #ToJS_showPicPro = pyqtSignal(str)
    def __init__(self, parent = None):

        super().__init__(parent)
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        graph = py2neo.Graph("http://localhost:7474", auth=("neo4j", "961121"))
        str1 = "MATCH (n:ErrorPlan) RETURN n"
        result = graph.run(str1).to_subgraph()
        self.items_list=[]
        for s in list(result.nodes):
            self.items_list.append(dict(s).get('name'))
        self.ui.completer = QtWidgets.QCompleter(self.items_list)
        self.ui.completer.setFilterMode(Qt.MatchContains)
        self.ui.completer.setMaxVisibleItems(10)
        self.ui.Check_lineEdit.setCompleter(self.ui.completer)

        self.resize(QGuiApplication.primaryScreen().availableSize() );

        self.defaultPicture = os.path.dirname(os.path.dirname(d)) + \
        "\\static\\pictures\\1.gif"

        self.__setlayout()

        # self.splitterV1.splitterMoved.connect(self.__pictureSizeChange)

        # self.splitter.splitterMoved.connect(self.__pictureSizeChange)

        # self.__draw(self.defaultPicture)


    def __setlayout(self):
        layout = QtWidgets.QHBoxLayout()
        self.splitterV1 = QtWidgets.QSplitter(self)
        self.splitterV1.setOrientation(Qt.Vertical)

        # self.splitterV1.addWidget(self.ui.SqlToolBox)
        self.splitterV1.addWidget(self.ui.labelTitle)
        self.splitterV1.addWidget(self.ui.Check_lineEdit)
        self.splitterV1.addWidget(self.ui.btnConfirms)
        # self.splitterV1.addWidget(self.ui.btnConfirms_kg)
        self.splitterV1.addWidget(self.ui.widget)
        self.splitterV1.addWidget(self.ui.btnConfirms_kg)
        # self.splitterV1.setStretchFactor(0, 0)


        # self.splitterV1.setContentsMargins(5,5,5,5)
        # self.splitterV1.addWidget(self.ui.LabelWidget)
#        self.url = 'file:///' + os.path.dirname(os.path.dirname(d)) +\
 #       '/static/html/JSTest.html'

         #---Web widget and layout-------------------------
        self.browser = QWebEngineView(self)
        self.pWebChannel = QWebChannel(self.browser.page())

        self.browser_kg=QWebEngineView(self)
        self.browser_kg.setVisible(False)
        #------js和qt通信--------------------------




        self.channel_expandNode = channel_expandNode(self)
        self.pWebChannel.registerObject('channel_expandNode',self.channel_expandNode)

        self.channel_showNode = channel_showNode(self)
        self.pWebChannel.registerObject("channel_showNode",self.channel_showNode)

        self.channel_showPicPro = channel_showPicPro(self)
        self.pWebChannel.registerObject('channel_showPicPro',self.channel_showPicPro) 

        self.browser.page().setWebChannel(self.pWebChannel)

        #self.url = 'file:///F:/demo/now/static/html/JSTest.html'
        self.url = 'file:///' + os.path.dirname(os.path.dirname(d)) +\
       '/static/html/show.html'
        self.url = self.url.replace('\\','/')
        self.browser.page().load(QUrl(self.url))
        self.browser.show()
        # self.browser.setVisible(False)
#------------------------------------------------------------------------------
       # self.url = 'file:///F:/demo/now`/static/html/JSTest.html'
        
        #self.url = self.url.replace('\\','/')
        #print("self.url = ",self.url)

        #self.browser = QWebEngineView()
        #self.browser.load(QUrl(self.url))
        
        self.splitterV2 = QtWidgets.QSplitter(self)
        self.splitterV2.setOrientation(Qt.Vertical)
        self.splitterV2.addWidget(self.browser)
        self.splitterV2.addWidget(self.ui.table_sql)
        self.splitterV2.addWidget(self.browser_kg)

        # self.splitterV2.setStretchFactor(0,20)
        # self.splitterV2.setStretchFactor(1,5)
        self.splitterV2.setSizes([1000,300])
        # self.browser.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        self.splitter = QtWidgets.QSplitter(self)
        self.splitter.setOrientation(Qt.Horizontal) 
        self.splitter.addWidget(self.splitterV1)
        self.splitter.addWidget(self.splitterV2)

        self.splitter.setStretchFactor(0,2)
        self.splitter.setStretchFactor(1,8)

        layout.addWidget(self.splitter)
        self.setLayout(layout)

        #---------------------------------


        self.channel_showNode.fromJS.connect(self.returnShowNode)
        self.ToJS_showNode.connect(self.channel_showNode.toJS)
        self.channel_expandNode.fromJS.connect(self.returnExpandNode)
        self.ToJS_expandNode.connect(self.channel_expandNode.toJS)

        self.channel_showPicPro.fromJS.connect(self.changePicPro)
        # self.ToJS_showPicPro.connect(self.channel_showPicPro.toJS)

    def changePicPro(self,strParameter):
        if not strParameter.isdigit():
            return
        strParameter=int(strParameter)
        # if not strParameter:
        #     return
        a = search.search_return(strParameter)
        print("changePicPro")
        print(a.dict())
        self.__createSearch(a.dict())
        # self.__draw(a.picture_path())

    def returnShowNode(self,strParameter):
        if not strParameter.isdigit():
            return
        strParameter = int(strParameter)
        # if not strParameter:
        #     return
        a = search.search_return(strParameter)
        self.ToJS_showNode.emit(a.singleNode_json())

    def returnExpandNode(self,strParameter):
        if not strParameter.isdigit():
            return
        strParameter = int(strParameter)
        # if not strParameter:
        #     return
        a = search.search_return(strParameter)
        print("expandNode")
        self.ToJS_expandNode.emit(a.json())
        



#-------------------------------------------------------------
   
    def __draw(self, picture_path):
        if not picture_path:
            picture_path = self.defaultPicture
        else:
            picture_path = picture_path[0]
        self.ui.Picture.clear()
        pic = QPixmap(picture_path)
        self.ui.Picture.setPixmap(pic)


    def __pictureSizeChange(self):
        self.ui.Picture.resize(self.ui.LabelWidget.size())

    # def resizeEvent(self, event):
    #     self.ui.Picture.resize(self.ui.LabelWidget.size())
        

    def __createSearch(self, dic):
        self.ui.table_sql.setColumnCount(len(dic))
        self.ui.table_sql.setRowCount(1)
        self.ui.table_sql.setHorizontalHeaderLabels(dic.keys())
        self.ui.table_sql.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        # self.ui.table_sql.horizontalHeader().setSectionResizeMode(0,QtWidgets.QHeaderView.ResizeToContents)

        i = 0
        for dictKey in dic.keys():
            newItem = QtWidgets.QTableWidgetItem(dic[dictKey])
            self.ui.table_sql.setItem(0,i,newItem)
            i += 1

    @pyqtSlot()
    def on_btnConfirms_kg_clicked(self):
        # self.splitterV2.setVisible(False)
        # self.browser.page().load()
        self.ui.table_sql.setVisible(False)
        self.browser.setVisible(False)
        self.browser_kg.setVisible(True)
        self.url = 'file:///' + os.path.dirname(os.path.dirname(d)) + \
                   '/static/html/kg.html'
        self.url = self.url.replace('\\', '/')
        self.browser_kg.page().load(QUrl(self.url))
        # self.browser.show()

    @pyqtSlot()
    def on_btnConfirms_clicked(self):
        # self.ui.table_sql.setVisible(True)
        # self.url='http://www.baidu.com'
        # self.url = 'file:///' + os.path.dirname(os.path.dirname(d)) + \
        #            '/static/html/show.html'
        # self.url = self.url.replace('\\', '/')
        # self.browser.page().load(QUrl(self.url))
        # self.browser.show()
        self.browser.setVisible(True)
        self.ui.table_sql.setVisible(True)
        self.browser_kg.setVisible(False)

        search_name = self.ui.Check_lineEdit.text()

        graph = py2neo.Graph("http://localhost:7474", auth=("neo4j", "961121"))
        str1 = "MATCH(n{name:'%s'})RETURN n" % (search_name)
        result=graph.run(str1).to_subgraph()
        # print(len(result.nodes))
        if result==None:
            return
        if len(result.nodes)>1:
            return
        # print(result.identity)
        search_name=result.identity
        # a = str(result)  # fuck neo4j
        # neodict=dict(result) if result else None

        self.neo = search.search_return(search_name)
        node_dict = self.neo.dict()
        print(node_dict)
        if node_dict:
            self.__createSearch(node_dict)
            # self.__draw(self.neo.picture_path())
            self.ToJS_showNode.emit(self.neo.singleNode_json())
            # self.browser.page().load(QUrl(self.url))




if __name__ == "__main__":
    import sys
    qapp = QtWidgets.QApplication(sys.argv)
    app = neo4j()
    app.show()
    sys.exit(qapp.exec_())