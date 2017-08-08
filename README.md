# Wrangle OpenStreetMap Data: Hamburg, Germany
Storage for Udacity OSM Data Wrangling Project

In this project, I analyze the OpenStreetMap data of Hamburg, Germany. I perform automated data cleaning via python scripts, and import the data into a SQL database which can be used for querying the data.
All files related to this project are located in this ZIP file.

- 'Project Report OSM Hamburg.ipynb': Project Report as iPython notebook file

- py folder (https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/py) containing 'jfo' package and it's documentation
  - 'jfo' Python package
    - Module 'schema.py': schema of transformation between XML tags and database table data types
    - Class 'myXML': loads OSM XML file and audits street names, ZIP codes, phone numbers etc
    - Class 'mySQL3dbConn': creates Connection and Cursor to SQLITE3 database
    - Class 'myDictWriter': writes validated and schemed csv files from dictionaries
        
  - 'doc' subfolder: Sphinx documentation, starting with 'modules.html'  
    


- 'OpenStreetMap-Hamburg-Sample.osm': contains OSM data Hamburg, Germany as XML tags and attributes


- csv folder (https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/csv), containing zipped CSV files
  - csv_nodes.zip
    - nodes.csv
    - nodes_tags.csv
  - csv_ways.zip
    - ways.csv
    - ways_nodes.csv
    - ways_tags.csv
  
  
- SQL files with code for
  - 'OSM_Create_Tables.sql': Creates SQLite3 tables
  - 'OSM_Drop_Tables.sql': Drops existing SQLite3 tables
  - 'OSM_Import_CSV.sql': Import csv file generated from XML file
  
  
- This 'Readme.md' file

- 'OpenStreetMap-Hamburg-Sample.osm': contains OSM data Hamburg, Germany as XML tags and attributes
