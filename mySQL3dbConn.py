
# coding: utf-8

# In[5]:

#!/usr/bin/env python


"""enables to establish SQLITE3 database connector and cursor as well as executes SQL statements.

.. module:: mySQL3dbConn
   :platform: Windows
   :synopsis: A useful module indeed.

.. moduleauthor:: Jan Foerster <jan.foerster@airbus.com>


"""

#__license__ = 'Jan FOERSTER'
#__revision__ = ' $Id: MyXML.py 1 2017-07-30 09:27:45z cokelaer $ '
#__docformat__ = 'reStructuredText'

import sqlite3, sys, pprint

class mySQLLITE3(sqlite3.Connection):
    """mySQLLITE3 class. Container for SQLLite3 Database Connections and SQL Statements.
 
    .. class:: mySQLLITE3
       Initializes only private variables, containing results of callable methods.
      
       :method: :func:`open`
       :method: :func:`execute_SQLStatements`
       :method: :func:`execute_SQLStatementsFile`
       :method: :func:`insert_Dictionary`
       :method: :func:`execute_SQL_Params`
       :method: :func:`commit_SQL`
       :method: :func:`rollback_SQL`
       :method: :func:`close`

       :function: :func:`query_OneResult`
       :function: :func:`query_AllResults`
       :function: :func:`query_AllResults`
        
        
    """ 

    #constructs class
    def __init__(self, sqlite3_home_path_in = None, sqlite3_dbname_in = None):
               
        self._connection = None
        self._cursor = None
                
        if sqlite3_dbname_in:
            self.open(sqlite3_home_path_in + sqlite3_dbname_in) 

    #deconstructs class        
    def __del__(self):
        self.close()

    #opens set, in case of entering a 'with' statement
    def __enter__(self):
        return self

    #closes set, in case of leaving a 'with' statement
    def __exit__(self,exc_type,exc_value,traceback):        
        self.close()
       
        
    #create (or opens) sqlite3 database (connection)    
    def open(self, name):        
        """Opens Connection and Cursor, if database has been indicated during class construction or even later

        :param str name: Absolute path and name of database

        :Example:
        
        >>> dbUdacity.open('C:\\Users\\test.db')
        
        
        """ 
        try:
            self._connection = sqlite3.connect(name)
            self._connection.isolation_level = None
            self._cursor = self._connection.cursor()

        except sqlite3.Error as e:
            print("Error connecting to database!")
        
    #commits remaining open SQL statements and closes sqlite3 cursor & database    
    def close(self):      
        """closes Cursor and Connection prior class destruction
                       
        :Example:
        
        >>> dbUdacity.close()
        
        
        """ 
        if self._connection:
            self._connection.commit()
            self._cursor.close()
            self._connection.close()
            
    def query_OneResult(self, query_in):
        """Query-SQL statements with first result
        
        :param str query_in: SELECT-SQL-Statement as single command line
                
        :Example:
        
        >>> dbUdacity.query_OneResult('SELECT * FROM TABLE apples;')
        
        
        """ 
        self._cursor.execute(query_in)
        return (self._cursor.fetchone())

    def query_AllResults(self, query_in):
        """Query-SQL statements with all results
        
        :param str query_in: SELECT-SQL-Statement as single command line
                
        :Example:
        
        >>> dbUdacity.query_OneResult('SELECT * FROM TABLE apples;')
        
        
        """ 
        self._cursor.execute(query_in)
        return (self._cursor.fetchall())
    
    def execute_SQLStatements(self, sql_script_in):
        """Execute-SQL statements as command line
        
        :param str sql_script_in: SQL-Statement as single command line
                
        :Example:
        
        >>> dbUdacity.execute_SQLStatements('SELECT * FROM TABLE apples;')
        
        
        """ 
        try:
            self._cursor.executescript(sql_script_in)   
        except sqlite3.OperationalError as err:
            self._connection.rollback()
            pprint.pprint('SQLLite3 Error: %s' % (err))
  
    
    #executes set of SQL statements as a lot
    def execute_SQLStatementsFile(self, file_in):
        """Execute-SQL statements from file, e.g. to create or drop tables
        
        :param str sql_statement_in: SQL-Statement including questionmarks as spaceholder for parameters
        :param str params_in: String or List of Strings as parameters
        
        :Example:
        
        >>> dbUdacity.execute_SQLStatementsFile('C:\\Users\\OSM_Create_Tables.sql')
        
        
        """ 
        with open (file_in, 'rb') as sqlfile:
            sqlCommands = sqlfile.read()
            try:
                self._cursor.executescript(sqlCommands)
            except sqlite3.OperationalError as err:
                self._connection.rollback()
                pprint.pprint('SQLLite3 Command: %s generated following Error: %s' % (sqlCommands, err))

    def insert_Dictionary(seld, sql_statement_in, dict_in):
        """Insert-SQL statement with Parameters
        
        :param str sql_statement_in: SQL-Statement including questionmarks as spaceholder for parameters
        :param str params_in: String or List of Strings as parameters
        
        :Example:
        
        >>> dbUdacity.insert_Dictionary('INSERT INTO Cars VALUES(?, ?, ?)', {[1, 2, 3], [1, 3, 5]})
        
        
        """ 
        try:
#            with con:
            self._cursor.executemany(sql_statement_in, dict_in)
        except sqlite3.OperationalError as err:
            self._connection.rollback()
            pprint.pprint('SQLLite3 Operational Error: %s' % (err))
        except sqlite3.IntegrityError as err:
            pprint.pprint('SQLLite3 Integrity Error: %s' % (err))
    
    def execute_SQL_Params(self, command_in, params_in):
        """Update-SQL statement with Parameters
        
        :param str command_in: SQL-Statement including questionmarks as spaceholder for parameters
        :param str params_in: String or List of Strings as parameters
        
        :Example:
        
        >>> dbUdacity.execute_SQL_Params('UPDATE Cars SET Price=? WHERE Id=?', [uPrice, uId])
        
        
        """ 
        try:
            self._cursor.execute(command_in, list(params_in))
        except sqlite3.OperationalError as err:
            self._connection.rollback()
            pprint.pprint('SQLLite3 Error: %s' % (err))
     
    def commit_SQL(self):
        """commits SQL statements since last comit

        :Example:
        
        >>> dbUdacity.commit_SQL()
        
        
        """ 
        self._connection.commit()
               
    def rollback_SQL(self):
        """rolls-back SQL statements since last comit

        :Example:
        
        >>> dbUdacity.rollback_SQL()
        
        
        """ 
        self._connection.rollback()

if __name__ == '__main__':  
    #dbUdacity = mySQLLITE3('C:\\Users\\JanUser\\sqlite\\sqlite_windows\\', 'test4.db')
    #dbUdacity.execute_SQLStatementsFile('C:\\Users\\JanUser\\Documents\\Udacity\\Sybullus\\L3 MongoDB\\Project\\OSM_Drop_Tables.sql')
    #dbUdacity.commit_SQL()
    #dbUdacity.execute_SQLStatementsFile('C:\\Users\\JanUser\\Documents\\Udacity\\Sybullus\\L3 MongoDB\\Project\\OSM_Create_Tables.sql')
    #dbUdacity.close()

