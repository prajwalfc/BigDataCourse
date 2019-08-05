# BigDataCourse
## Readme is available for each homework in respective directory
## About the course
The course aims to provide a broad understanding of big data and current technologies in managing and processing them with a focus on the urban environment.  With storage and networking getting significant cheaper and faster, big data sets could easily reach the hands of data enthusiasts with just a few mouse clicks. These enthusiasts could be policy makers, government employees or managers, who would like to draw insights and (business) value from big data. Thus, it is crucial for big data to be made available to the non-expert users in such a way that they can process the data without the need of a supercomputing expert. One such approach is to build big data programming frameworks that can deal with big data in as close a paradigm as the way it deals with “small data.” Also, such a framework should be as simple as possible, even if not as efficient as custom-designed parallel solutions. Users should expect that if their code works within these frameworks for small data, it will also work for big data. General topics of this course include: big data ecosystems, parallel and streaming programming model, MapReduce, Hadoop, Spark, Pig, and NoSQL solutions. Hands-on labs and exercises will be offered throughout to bolster the knowledge learned in each module.

## Tools used
- python2 or above
- Homework 5 and 6 are done NYU Hadoop Culster (called NYU dumbo)
# Installing Spark (unix and linux) (good luck to windows users)
- Step 1 : [Install Anaconda](https://www.anaconda.com/distribution/#download-section)
- Step 2: conda install pyspark
- run pyspark command in terminal, that should load pyspark shell.
- Note the install location using <b>pip show pyspark | grep Location</b>
- To write and run spark application in jupyter notebook enable pyspark shell in jupyter notebook
 by <b>export PYSPARK_DRIVER_PYTHON=`which jupyter`export PYSPARK_DRIVER_PYTHON_OPTS=notebookexport SPARK_HOME=[PySpark Location]/pyspark </b> in terminal or add in .bashrc in home directory in linux system.
 
## Enabling and handling  spatial data types in spark
Handling Spatial Data — Python
- [conda install geopandas](http://geopandas.org/install.html) should install geopandas with all dependecies like pandas,fiona,    shapely,pyproj,rtree
- make sure to install gdal library using apt-get install 
- sudo add-apt-repository -y ppa:ubuntugis/ppa
- sudo apt update 
- sudo apt upgrade # if you already have gdal 1.11 installed 
- sudo apt install gdal-bin python-gdal python3-gdal
- Most data can be stored in Python native structures: tuple, list, and dictionaries
- Useful packages for handling spatial data:
- fiona : read/write GIS files (a thin API for the GDAL/OGR I/O library)
- geopandas : extending pandas with geo support
- json : a built-in package for reading JSON files including GeoJSON
- pyproj: map projection (conversion from one projection to another)
- shapefile : a light-weight package for reading shapefiles
- shapely : provide geometric operations on 2D planes (oblivious to geographic projections), based on PostGIS engine GEOS

## Handling Spatial Data — Conversion
GDAL/OGR provides a powerful command line tool for conversion (and transformation) of geospatial data, similar to ImageMagick’s convert: [<b>ogr2ogr</b>](https://trac.osgeo.org/gdal/wiki/DownloadingGdalBinaries)
- Convert shapefile to geojson <b> ogr2ogr -f GeoJSON nyc.geojson nyc.shp </b>
- also reproject the data to EPSG:4326 coordinates (~GPS lat lon): <b>ogr2ogr -f GeoJSON -t_srs EPSG:4326 nyc.geojson nyc.shp</b>
- Further reading for R-tree please refer to [this](https://geoffboeing.com/2016/10/r-tree-spatial-index-python/) and [this](http://toblerity.org/rtree/tutorial.html)
