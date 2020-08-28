import sys
import os
import PyQt5.QtWidgets as QtWidgets
import PyQt5.QtCore as QtCore
d = os.path.dirname(__file__)
print(d)
sys.path.append(d)
from now.codes.gui import neo4j


# QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
qapp = QtWidgets.QApplication(sys.argv)
app = neo4j.neo4j()
app.show()
sys.exit(qapp.exec_())