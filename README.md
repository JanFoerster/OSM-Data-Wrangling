# Wrangle OpenStreetMap Data: Hamburg, Germany
Storage for Udacity OSM Data Wrangling Project

In this project, I analyze the OpenStreetMap data of Hamburg, Germany. I perform automated data cleaning via python scripts, and import the data into a SQL database which can be used for querying the data.
All files related to this project are located in these ZIP files within the different folders.

- 'Project+Report+OSM+Hamburg.html': Project Report as html file
- 'Project+Report+OSM+Hamburg.ipynb': Project Report as iPython Notebook file

Please download all zip files from all folders and extract them in one target folder. The 'osmHamburg.zip' files need to be extracted within SQLite3 folders. The 'jfo.zip' file need to be extracted under Anaconda2/Lib/site-packages.

- folder '01.OSMXML' contains both OpenStreetMap xml files (370 MB original, 80 MB for Samples)
__[https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/01-OSMXML]__here

- All Python package files need to be unzipped under Anaconda2/Lib/site-packages. See 'py' folder (https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/py) containing 'jfo' package and it's Sphinx documentation
  - 'jfo' Python package
    - Module 'schema.py': schema of transformation between XML tags and database table data types
    - Class 'myXML': loads OSM XML file and audits street names, ZIP codes, phone numbers etc
    - Class 'mySQL3dbConn': creates Connection and Cursor to SQLITE3 database
    - Class 'myDictWriter': writes validated and schemed csv files from dictionaries
        
  - 'doc' subfolder: Sphinx documentation, starting with 'modules.html'  
    
- All OpenStreetMap files need to be unzipped together in same destination folder, whereas the Final Report, csv files and sql files are saved. see 'osm' folder ((https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/osm), containing zipped OSB XML files
  - 'OpenStreetMap-Hamburg-Sample.osm': zipped in one file and contains OSM data Hamburg, Germany as XML tags and attributes (80 MB)
  - 'OpenStreetMap-Hamburg-31.osm': zipped in two files and contains OSM data Hamburg, Germany as XML tags and attributes (380 MB)

- All csv files need to be saved together in same destination folder, whereas the Final Report, osm files and sql files are saved. 'csv' folder (https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/csv), containing zipped CSV files
  - csv_nodes.zip
    - nodes.csv
    - nodes_tags.csv
  - csv_ways.zip
    - ways.csv
    - ways_nodes.csv
    - ways_tags.csv
    
- All SQL files need to be saved together in same destination folder, whereas the Final Report, osm files and csv files are saved. 'sql' folder (https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/sql), containing SQL files
  - 'OSM_Create_Tables.sql': Creates SQLite3 tables
  - 'OSM_Drop_Tables.sql': Drops existing SQLite3 tables
  - 'OSM_Import_CSV.sql': Import csv file generated from XML file
    
- This 'Readme.md' file
