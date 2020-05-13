# sys lets us check what platform we are on to do some
# custom Mac stuff
import sys

# Basic QT classes
from PyQt5 import QtWidgets as qtw 
from PyQt5 import QtGui as qtg 
from PyQt5 import QtCore as qtc

from .rainbow_model import RainbowModel
from .settings_dialog import SettingsDialog

black = qtg.QColor(0,0,0)
red = qtg.QColor(255, 0, 0)
yellow = qtg.QColor(255,255,0)
also_red = qtg.QColor(255,0,0)

color_list = black, red, yellow, also_red
print(color_list)
color_set = set(list)
print(color_set)