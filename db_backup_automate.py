from operator import contains
import pandas as pd
import pyodbc


def create_connection_wa(self,db='master'):
      conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-RPEP7UC\SQLEXPRESS;"
                      "Database="+db+";"
                      "Trusted_Connection=yes;")
      return conn


cnxn=create_connection_wa("my_data")
cnxn.autocommit = True
crsr = cnxn.cursor()

crsr.execute( r"BACKUP DATABASE my_data  TO DISK = 'F:\corestack\backups\my_data.bak';"  )

while (crsr.nextset()):
    if  "BACKUP DATABASE successfully processed" in str(crsr.messages[0]) :
        print("backup of database my_data was successfully processed")
    pass

crsr.close()
cnxn.autocommit = False
cnxn.close() 