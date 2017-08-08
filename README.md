# Wrangle OpenStreetMap Data: Hamburg, Germany
Storage for Udacity OSM Data Wrangling Project

In this project, I analyze the OpenStreetMap data of Hamburg, Germany. I perform automated data cleaning via python scripts, and import the data into a SQL database which can be used for querying the data.
All files related to this project are located in this ZIP file.

- 'Project Report OSM Hamburg.ipynb': Project Report as iPython notebook file

- 'jfo': Python code as package in directory

- Module 'schema.py': schema of transformation between XML tags and database table data types
- Class 'myXML': loads OSM XML file and audits street names, ZIP codes, phone numbers etc
- Class 'mySQL3dbConn': creates Connection and Cursor to SQLITE3 database
- Class 'myDictWriter': writes validated and schemed csv files from dictionaries
- 'doc': contains SPHINX documentation about classes


- 'OpenStreetMap-Hamburg-Sample.osm': contains OSM data Hamburg, Germany as XML tags and attributes


- CSV files
  - nodes.csv
  - nodes_tags.csv
  - ways.csv
  - ways_nodes.csv
  - ways_tags.csv
  
  
- SQL files with code for
  - 'OSM_Create_Tables.sql': Creates SQLite3 tables
  - 'OSM_Drop_Tables.sql': Drops existing SQLite3 tables
  - 'OSM_Import_CSV.sql': Import csv file generated from XML file
  
  
- This 'Readme.md' file
