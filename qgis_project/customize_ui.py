from qgis.utils import iface
from qgis.PyQt.QtGui import QIcon


def customize_ui():
    icon = QIcon("./icon.png")
    iface.mainWindow().setWindowIcon(icon)
    iface.mainWindow().setWindowTitle("Treescape")
