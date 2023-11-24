from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QIcon
import os

#icon_file
# Set dialog icon
icon_file = os.path.normpath( os.path.join(os.path.dirname(__file__), 'icons', 'icon.svg') )
icon_file = icon_file.replace("\src", "")

def missed_raster_path():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("Choose the raster file to continue")
    msgBox.setWindowTitle("Raster not provided")
    msgBox.setWindowIcon(QIcon(icon_file))
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()

def missed_vector_path():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("Choose the vector shape to overlap")
    msgBox.setWindowTitle("File missed")
    msgBox.setWindowIcon(QIcon(icon_file))
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()

def missed_raster_vector():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("Choose both raster and vector files")
    msgBox.setWindowTitle("Raster and Vector missed")
    msgBox.setWindowIcon(QIcon(icon_file))
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()

def is_directory():
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("The path must not be a folder")
    msgBox.setWindowTitle("Incorrect path")
    msgBox.setWindowIcon(QIcon(icon_file))
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()

def Unoverlable(): # Both Raster and Vector no provided and Checbox not checked and Combobox not selected
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("Make sure both raster and vector has valid CRS and overlapped")
    msgBox.setWindowTitle("CRS Problem")
    msgBox.setWindowIcon(QIcon(icon_file))
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()

## HANDLE VECTOR FEATURE UNMACTHING
def not_point(): # Both Raster and Vector no provided and Checbox not checked and Combobox not selected
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("You must select a point vector to extract")
    msgBox.setWindowTitle("Selections unmatched")
    msgBox.setWindowIcon(QIcon(icon_file))
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()

def not_polygon(): # Both Raster and Vector no provided and Checbox not checked and Combobox not selected
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("You must select a polygon vector to extract")
    msgBox.setWindowTitle("Selections unmatched")
    msgBox.setWindowIcon(QIcon(icon_file))
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()

def not_line(): # Both Raster and Vector no provided and Checbox not checked and Combobox not selected
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("You must select a line vector to extract")
    msgBox.setWindowTitle("Selections unmatched")
    msgBox.setWindowIcon(QIcon(icon_file))
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()

# HANDLE FOLDER PATH
def no_folder(): # 
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("You must provide the folder")
    msgBox.setWindowTitle("No folder selected")
    msgBox.setWindowIcon(QIcon(icon_file))
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()

def empty_folder(): # Both Raster and Vector no provided and Checbox not checked and Combobox not selected
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("The folder should contain unless a raster")
    msgBox.setWindowTitle("No raster in folder")
    msgBox.setWindowIcon(QIcon(icon_file))
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()

def no_stat(): # Both Raster and Vector no provided and Checbox not checked and Combobox not selected
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Critical)
    msgBox.setText("Choose unless a stat to apply")
    msgBox.setWindowTitle("No stat")
    msgBox.setWindowIcon(QIcon(icon_file))
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()