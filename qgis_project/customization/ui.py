from pathlib import Path

from qgis.core import QgsApplication
from qgis.utils import iface
from qgis.PyQt.QtGui import QIcon


def load_ui_customization(ini_file_path):
    """
    Loads UI customization settings from a specified .ini file into QGIS.
    """
    # Load the customization file
    app = QgsApplication.instance()
    app.loadCustomization(ini_file_path)

    # Enable customization
    app.setCustomizationEnabled(True)


ICON_FILE = Path(".") / "icon.png"

# TODO: Load me.
CUSTOMIZATION_FILE = Path(".") / "interface_customization.ini"

def customize_ui():
    icon = QIcon("./icon.png")
    iface.mainWindow().setWindowIcon(icon)
    iface.mainWindow().setWindowTitle("Treescape")

    # Not working yet.
    # load_ui_customization(CUSTOMIZATION_FILE)
