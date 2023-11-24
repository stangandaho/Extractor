[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10152979.svg)](https://doi.org/10.5281/zenodo.10152979)


## Description
The **`Extractor`** QGIS plugin is a tool for extracting data from raster layers using vector features like points, lines, and polygons. It's invaluable for complex spatial analyses, especially in time series studies, allowing extraction from multiple layers to track changes over time. It can be used to analyze land use shifts by extracting vegetation cover, urbanization, etc., across different time points. It's also vital in landscape studies, extracting environmental variables (elevation, slope, etc.) to understand biodiversity patterns and ecosystem functions.

## installation
The installation of the plugin is done as usual from the QGIS plugin repository. In the Plugins menu, go to All tab. In the search bar, type 'Extractor' and click on Install. After the installation, the Extractor will appear in the Raster Menu of QGIS and in toolbar as shown in the image below. Click on it to go to the Extractor interface.

<img src="https://user-images.githubusercontent.com/58343945/225006009-d42cc5f3-5b4f-4c82-8614-81ef38308b2c.png" alt="Extractor location" width="600" height="200">

If no problems occurred during the installation of the plugin and you click on the icon, its interface will appear as shown in this image.

<img src="https://user-images.githubusercontent.com/58343945/224814864-6783ca90-3a2c-4631-8f60-e5367cdc09d3.png" alt="Extractor interface" width="600" height="450">

> To prevent some errors when installing or running Extractor, it is recommended to have a version of QGIS that runs python version 3.7.9 or higher. So a QGIS version of 3.14 or higher is recommended. You can check python version from *Help* menu in QGIS (Help -> About => Python version). You can also check python version runing the code snippet below in the python console accessible from the QGIS **_Plugins_** menu.

```python
import sys
print(sys.version)
```

## How does it work?

Firstly, you are asked to choose on how many images you want to work (one image or several). If you choose 'Single', you will be asked to choose the raster after browsing in the explorer. Otherwise, you will choose a folder that contains all the raster you want to extract from.

> For the moment the GeoTIF files are more manageable.

* ###  Single
Single checked allows you to choose the raster. If you don't set any other options and start the extraction by clicking "Extract", **`Exractor`** will start extracting all data in the raster. 

> Please note! If the raster is relatively large, the extraction may crash QGIS.  

The different options for extracting data from a raster depend on objectives. For point vectors, the extraction is direct. For a line, extraction of all data (__Whole data__) can be done as well as statistics can be applied (__Zonal statistics__). It is the same for polygon vectors, where the data within the polygons can be extracted as statistics can be applied. 

* ### Multiple
For what is multiple raster, "Multiple" should be checked. Only zonal statistics can be applied mainly with lines and polygons.  

All extractions lead to the display of the relative table. This table can be downloaded in .csv or .txt format by clicking on "Save". It can be deleted with the "Clear" button. 
For wrong settings during extraction, error dialogues appear to inform what is missing or what needs to be done. After adding the files, they can be explored in the main Canva of QGIS.

## Credits
The icons used in this plugin were sourced from SVG Repo (https://www.svgrepo.com/), created by SVG Repo LLC and licensed under GNU GPL license.
