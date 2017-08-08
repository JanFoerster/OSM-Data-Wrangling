
# coding: utf-8

# In[ ]:

#!/usr/bin/env python


"""
This function converts xlsx file into a dictionary
@author: Jan FOERSTER
@Date: 2017-07-25
@Version: 1.0
"""

import xlrd
from collections import defaultdict

def parse_xlsx2dict(xslxfile_in, xslxsheet_in):
    workbook = xlrd.open_workbook(xslxfile_in)
    sheet = workbook.sheet_by_index(xslxsheet_in)

    #data = defaultdict()
    data = [[sheet.cell_value(r, col) 
                for col in range(sheet.ncols)] 
                    for r in range(sheet.nrows)]

    for row in range(sheet.nrows):
        for col in range(sheet.ncols):
                #transform to a Python datetime tuple, from the Excel float
                if sheet.cell_type(row, col) == 3:
                    exceltime = sheet.cell_value(row, col)
                    data[row][col] = xlrd.xldate_as_tuple(exceltime, 0)
                    
    return data
        
#Get a slice of values in column 3, from rows 1-3
#sheet.col_values(3, start_rowx=1, end_rowx=4)

#Calculate Min & Max from Excel
#cv =sheet.col_values(1, start_rowx = 1, end_rowx = None)
    
#maxval = max(cv)
#minval = min(cv)
    
#maxpos = cv.index(maxval) + 1
#minpos = cv.index(minval) + 1
    
#maxtime = sheet.cell_value(maxpos, 0)
#realmaxtime = xlrd.xldate_as_tuple(maxtime, 0)
#mintime = sheet.cell_value(minpos, 0)
#realmintime = xlrd.xldate_as_tuple(mintime, 0)
        
#data = {
#            'maxtime': realmaxtime,
#            'maxvalue': maxval,
#            'mintime': realmintime,
#            'minvalue': minval,
#            'avgcoast': sum(cv) / float(len(cv))
#    }


"""
Test Purposes as stand-alone
"""
if __name__ == "__main__":
    print parse_xlsx2dict("2013_ERCOT_Hourly_Load_Data.xls", 0)

