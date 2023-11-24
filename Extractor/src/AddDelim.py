from qgis.PyQt.QtWidgets import (QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, 
                                 QTableWidget, QTableWidgetItem, QHBoxLayout)
from qgis.core import (QgsVectorLayer, Qgis, 
                       QgsProject, QgsVectorFileWriter, QgsCoordinateReferenceSystem)
from qgis.utils import iface
from qgis.gui import QgsProjectionSelectionWidget
from PyQt5.QtGui import QIcon, QFont
import pandas as pd
import os

class Delim(QDialog):
    def __init__(self, file_path):
        super().__init__()
        # Dialog
        self.setWindowTitle("Delimited Text Options")#ok
        # Set dialog icon
        icon_file = os.path.normpath( os.path.join(os.path.dirname(__file__), 'icons', 'icon.svg') )
        icon_file = icon_file.replace("\src", "")
        self.setWindowIcon(QIcon(icon_file)) 
        # Set font
        qgis_font = iface.mainWindow().font()
        self.setFont(qgis_font)
        # Set a fixed width and height for the dialog
        self.setFixedSize(600, 500) 

        self.layout = QVBoxLayout()#ok
        self.vlayout_sep = QHBoxLayout()
        self.vlayout_lon = QHBoxLayout()
        self.vlayout_lat = QHBoxLayout()
        # 
        self.file_label = QLabel("Select CSV/TXT File:")#ok
        self.layout.addWidget(self.file_label)#ok

        self.delimiter_label =  QLabel("Separator:")#ok
        self.vlayout_sep.addWidget(self.delimiter_label)#ok

        self.delimiter_edit = QComboBox()
        self.delimiter_edit.addItems([",", ";", "' '"])
        self.delimiter_edit.currentIndexChanged.connect(self.adjusted_table)
        self.delimiter_edit.currentIndexChanged.connect(self.populate_columns)

        self.vlayout_sep.addWidget(self.delimiter_edit)


        self.longitude_label = QLabel("Longitude:")
        self.vlayout_lon.addWidget(self.longitude_label)
        self.longitude_combo = QComboBox()
        self.longitude_combo.currentIndexChanged.connect(self.adjusted_table)
        self.vlayout_lon.addWidget(self.longitude_combo)

        self.latitude_label = QLabel("Latitude:")
        self.vlayout_lat.addWidget(self.latitude_label)
        self.latitude_combo = QComboBox()
        self.latitude_combo.currentIndexChanged.connect(self.adjusted_table)
        self.vlayout_lat.addWidget(self.latitude_combo)

        self.layout.addLayout(self.vlayout_sep)#, , 
        self.layout.addLayout(self.vlayout_lon)
        self.layout.addLayout(self.vlayout_lat)

        # Projection selection widget
        self.projection_widget = QgsProjectionSelectionWidget(self)
        self.layout.addWidget(self.projection_widget)
        default_crs = QgsCoordinateReferenceSystem('EPSG:4326')
        self.projection_widget.setCrs(default_crs)

        # Table to show adjusted data
        self.adjusted_table = QTableWidget()
        self.layout.addWidget(self.adjusted_table)

        self.setLayout(self.layout)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.load_csv)
        self.layout.addWidget(self.ok_button)

        self.setLayout(self.layout)
        ##
        self.file_path = file_path
        file_name, file_ext = os.path.splitext(os.path.basename(self.file_path))
        self.file_label.setText(f"Selected File: {'... ' + file_name + file_ext}")
        self.populate_columns()

    def populate_columns(self):
        delimiter = self.delimiter_edit.currentText()
        if delimiter == ";":
            df = pd.read_csv(filepath_or_buffer = self.file_path, sep = ";")
        elif delimiter == " ":
            df = pd.read_csv(filepath_or_buffer = self.file_path, sep = " ")
        else:
            df = pd.read_csv(filepath_or_buffer = self.file_path)
        
        header = df.columns.to_list()
        self.latitude_combo.clear()
        self.longitude_combo.clear()
        self.latitude_combo.addItems(header)
        self.longitude_combo.addItems(header)

    def adjusted_table(self):
        latitude_column = self.latitude_combo.currentText()
        longitude_column = self.longitude_combo.currentText()
        delimiter = self.delimiter_edit.currentText()
        # Placeholder data for the table (replace with your actual data)
        try:
            if delimiter == ";":
                df = pd.read_csv(filepath_or_buffer = self.file_path, sep = ";")
            elif delimiter == " ":
                df = pd.read_csv(filepath_or_buffer = self.file_path, sep = " ")
            else:
                df = pd.read_csv(filepath_or_buffer = self.file_path)
            table_data = df.head(10)[[longitude_column, latitude_column]]
            self.adjusted_table.setRowCount(len(table_data))
            self.adjusted_table.setColumnCount(len(table_data.columns))
            # Populate QTableWidget with DataFrame content
            for i, (index, row) in enumerate(table_data.iterrows()):
                for j, val in enumerate(row):
                    item = QTableWidgetItem(str(val))  # Convert to string for QTableWidgetItem
                    self.adjusted_table.setItem(i, j, item)
                    
            self.adjusted_table.setHorizontalHeaderLabels([longitude_column, latitude_column]) # Set column headers
        except:
            pass

    def load_csv(self):
        latitude_column = self.latitude_combo.currentText()
        longitude_column = self.longitude_combo.currentText()
        new_espg = self.projection_widget.crs().postgisSrid()
        
        if latitude_column and longitude_column:
            delimiter = self.delimiter_edit.currentText()
            uri = "file:///{}?delimiter={}&xField={}&yField={}&crs=EPSG:{}".format(self.file_path, 
                                                                                   delimiter, longitude_column, 
                                                                                   latitude_column, new_espg)
            layer_name, extension = os.path.splitext(os.path.basename(self.file_path))
            layer = QgsVectorLayer(uri, layer_name, "delimitedtext")
            
            if layer.isValid():
                QgsProject.instance().addMapLayer(layer)
                #Write
                save_options = QgsVectorFileWriter.SaveVectorOptions()
                save_options.driverName = 'ESRI Shapefile'
                save_options.fileEncoding = "UTF-8"
                transform_context = QgsProject.instance().transformContext()


                QgsVectorFileWriter.writeAsVectorFormatV3(layer, r"{}".format(self.file_path.replace(extension, ".shp")), 
                                                        transform_context, save_options)
            else:
                iface.messageBar().pushMessage("Error", "Extractor can't add layer", level=Qgis.Critical)



