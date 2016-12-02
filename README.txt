
******************************************************************************
Optimal Itinerary -- README

(Code has been tested only on Windows 10 and Linux Ubuntu 16.04.)

******************************************************************************
Table of Contents

1. Data Acquisition and Pre-Processing
1.1 Road Network Data Acquisition
1.2 Road Network Pre-Processing
1.3 Trip Advisor Data Acquisition and Pre-Processing
2. Modules to Install
2.1 Scipy 
2.2 Pandas 
2.3 Geocoder
2.4 Scrapy
2.5 Shapefile
2.6 OGR / GDAL
2.7 QGIS
2.8 Tkinter
2.9 Shapely 
2.10 PIL
2.11 ImageTK
3. How to Run the Code

******************************************************************************
1. Data Acquisition and Pre-Processing

1.1 Road Network Data Acquisition

Pre-processed road network data (in the form of shapefiles) for the following states in the U.S. are included: Alabama, Alaska, California, Colorado, District of Columbia, Hawaii, New York, and Texas.

If you would like to run the code for other states, you will need to download the raw road network data and run the pre-processing code as described in Section 1.2.

The road network data for the rest of North America can be found at http://download.geofabrik.de/north-america.html

Information regarding the road network data can be found at: 
http://download.geofabrik.de/osm-data-in-gis-formats-free.pdf


1.2 Road Network Data Pre-Processing

If you are running the shapefiles included, they are pre-processed, so this section will not be needed. However, if you downloaded raw road network data, then you will need to follow the pre-processing instructions in this section.

First, re-save the Open Street Map (OSM) road shapefile as '<state>_roads.shp' (e.g. 'texas_roads.shp').

Before running preprocess_shapefiles.py to pre-process the shapefiles for the road network data, you will need to make sure Line 1 points to the place where QGIS is installed on your computer, and change the variable dest in Line 8 to equal '<state>' as specified above (e.g. dest = 'texas').

After running preprocess_shapefiles.py, verify code ran correctly by checking that the resultant shapefiles called '<state>_roads_final.shp' (e.g. 'texas_roads_final.shp') and its supporting files are in /spatial/final.


1.3 Trip Advisor Data Acquisition and Pre-Processing

When you run the scrape_gui.py code in Section 3, it will acquire the Trip Advisor Data and process the data automatically.


******************************************************************************
2. Modules to Install

2.1 Scipy 
(https://www.scipy.org/install.html)
Windows & Linux: pip install scipy 


2.2 Pandas 
(http://pandas.pydata.org/pandas-docs/stable/install.html)
Windows & Linux: pip install pandas


2.3 Geocoder
(https://pypi.python.org/pypi/geocoder)
Windows & Linux: pip install geocoder


2.4 Scrapy
(https://doc.scrapy.org/en/latest/intro/install.html)
Windows & Linux: pip install scrapy


2.5 Shapefile
(https://pypi.python.org/pypi/pyshp)
Windows & Linux: pip install pyshp


2.6 OGR / GDAL
(http://gis.stackexchange.com/questions/9553/installing-gdal-and-ogr-for-python)


2.7 QGIS
(https://www.qgis.org/en/site/forusers/alldownloads.html) 


2.8 Tkinter
(http://tkinter.unpythonic.net/wiki/How_to_install_Tkinter)


2.9 Shapely 
(https://pypi.python.org/pypi/Shapely)


2.10 PIL
Windows: conda install pil
- If there is an error that says "_imagingtk is not found", then:
	pip uninstall pillow
	pip install Image
Linux: pip install PIL


2.11 ImageTK
(http://stackoverflow.com/questions/10630736/no-module-named-image-tk)
Windows: pip install Image
Linux: sudo apt-get install python-imaging-tk

******************************************************************************
3. How to Run the Code

Run scrape_gui_final.py. When the GUI shows up, enter the city with its state in the first box (e.g. Austin, TX), and the hotel name in the second box (e.g. Hotel Ella). The output will be a one-day itinerary, map, and attraction reviews for the city, starting and ending at the hotel.

Average run-time for the code takes approximately 5-10 minutes, depending on the size of the shapefiles.

******************************************************************************
