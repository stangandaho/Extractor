from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QComboBox, QTableWidget, 
QTableWidgetItem, QPushButton, QHBoxLayout, QLabel, QApplication)
from qgis.PyQt.QtCore import Qt
from qgis.gui import QgsProjectionSelectionWidget
import sys
import pandas as pd

class Delim(QDialog):
    def __init__(self, file_path, parent=None):
        super(Delim, self).__init__(parent)
        self.setWindowTitle("Delimited Text File Options")
        
        #df = pd.read_csv(filepath_or_buffer= file_path, sep = sep)
        self.file_path = file_path
        sep_ = [";", ",", "=", "\t"]

        col_layout = QHBoxLayout()
        layout = QVBoxLayout()

        # Dropdowns to select CSV file columns
        self.lon = QComboBox()
        self.lat = QComboBox()
        self.sep = QComboBox()
        self.projection_widget = QgsProjectionSelectionWidget(self)

        # Dropdown for selecting separator
        self.sep.addItems(sep_)
        self.sep.currentIndexChanged.connect(self.update_table)

        col_layout.addWidget(QLabel("Separator:"))
        col_layout.addWidget(self.sep)

        col_layout.addWidget(QLabel("Longitude:"))
        col_layout.addWidget(self.lon)

        col_layout.addWidget(QLabel("Latitude:"))
        col_layout.addWidget(self.lat)

        layout.addLayout(col_layout)

        # Projection selection widget
        layout.addWidget(self.projection_widget)

        # Table to show adjusted data
        self.adjusted_table = QTableWidget()
        layout.addWidget(self.adjusted_table)

        # Button to update the table with selected columns and separator
        self.update_button = QPushButton("Set")
        layout.addWidget(self.update_button)
        self.update_button.clicked.connect(self.convert_delim_to_shp)

        self.setLayout(layout)

        self.df = pd.read_csv(filepath_or_buffer=r"{}".format(self.file_path), sep = self.sep.currentText())
        self.colnames = self.df.columns.to_list()

        self.lon.currentIndexChanged.connect(self.update_table)
        self.lat.currentIndexChanged.connect(self.update_table)

        # Populate dropdowns with options
        #columns =  list(set(df.columns.to_list())) # 
        self.lon.addItems(self.colnames)
        self.lat.addItems(self.colnames)

        # Retrieve selected column names
        self.set_lon = self.lon.currentText()
        self.set_lat = self.lat.currentText()


    def update_table(self):
        
        # Placeholder data for the table (replace with your actual data)
        try:
            table_data = self.df.head(8)[[self.set_lon, self.set_lat]]

            self.adjusted_table.clear()
            self.adjusted_table.setRowCount(len(table_data))
            self.adjusted_table.setColumnCount(len(table_data.columns))

        # Populate QTableWidget with DataFrame content
            for i, (index, row) in enumerate(table_data.iterrows()):
                for j, val in enumerate(row):
                    item = QTableWidgetItem(str(val))  # Convert to string for QTableWidgetItem
                    self.adjusted_table.setItem(i, j, item)
                    
            self.adjusted_table.setHorizontalHeaderLabels([self.set_lon, self.set_lat])  # Set column headers
        except:
            pass
    
    
    def convert_delim_to_shp(self):
        pass#print(self.df.columns.to_list())

