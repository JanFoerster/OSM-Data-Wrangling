# Wrangle OpenStreetMap Data: Hamburg, Germany
__Jan Foerster__
__(c) 2017__

Storage for Udacity OSM Data Wrangling Project

In this project, I analyze the OpenStreetMap data of Hamburg, Germany. I perform automated data cleaning via python scripts, and import the data into a SQL database which can be used for querying the data.
All files related to this project are located in these ZIP files within the different folders.

- 'Project+Report+OSM+Hamburg.html': Project Report as html file
- 'Project+Report+OSM+Hamburg.ipynb': Project Report as iPython Notebook file

Please download all zip files from all folders and extract them in one target folder. The 'osmHamburg.zip' files need to be extracted within SQLite3 folders. The 'jfo.zip' file need to be extracted under Anaconda2/Lib/site-packages.

- folder [01-OSMXML](<https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/01-OSMXML>) contains both OpenStreetMap xml files (370 MB original, 80 MB for Samples)
    - 'OpenStreetMap-Hamburg-Sample.osm': zipped in one file and contains OSM data Hamburg, Germany as XML tags and attributes (80 MB)
    - 'OpenStreetMap-Hamburg-31.osm': zipped in two files and contains OSM data Hamburg, Germany as XML tags and attributes (380 MB)

- folder [02-Python Package jfo](<https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/"02-Python Package jfo">) contains Python classes and modules used to import, analyze and wrangle XML data

- folder [03-Sphinx docs](<https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/03-Sphinx%20docs>) contains a full documentation of all classes and modules of jfo package derived from Sphinx as html sources

- folder [04-CSV](<https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/04-CSV>) contains all csv files generated from XML file for the five SQLite3 tables
    - csv_nodes.zip
      - nodes.csv
      - nodes_tags.csv
    - csv_ways.zip
      - ways.csv
      - ways_nodes.csv
      - ways_tags.csv

- folder [05-SQLite3 0DB](<https://github.com/JanFoerster/OSM-Data-Wrangling/tree/master/05-SQLite3%20DB>) contains SQLite3 database with imported csv files plus all applied SQL files, either directly from Python or from SQLite3 command-line
    - 'OSM_Create_Tables.sql': Creates SQLite3 tables
    - 'OSM_Drop_Tables.sql': Drops existing SQLite3 tables
    - 'OSM_Import_CSV.sql': Import csv file generated from XML file
    
- This 'Readme.md' file
