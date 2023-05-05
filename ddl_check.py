import pandas as pd
import pyodbc
import df_compare as dfc
import PySimpleGUI as sg

class ddl_check:
  def __init__(self, filename):
    self.filename = filename
    
  def read_file(self):
      df  = pd.read_excel(self.filename,  sheet_name='emp_data', header=1, na_values='None', skiprows=4)
      return df

  def create_connection_wa(self,db='master'):
      conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=DESKTOP-RPEP7UC\SQLEXPRESS;"
                      "Database="+db+";"
                      "Trusted_Connection=yes;")
      return conn


  def get_schema(self,con,db,tbl_name):
      schm_query="""
      select  IC.COLUMN_NAME as column_name,
case when IC.CHARACTER_MAXIMUM_LENGTH is null then  IC.DATA_TYPE else concat(IC.DATA_TYPE,'(',IC.CHARACTER_MAXIMUM_LENGTH,')') end as data_type,
case when C.COLUMN_NAME = IC.COLUMN_NAME THEN 'PRIMARY_KEY'
     when IC.IS_NULLABLE='NO' then 'NOT NULL'
	 when IC.IS_NULLABLE='YES' then 'NULLABLE'else 'NA' end  as constraints
FROM   INFORMATION_SCHEMA.COLUMNS IC
left join INFORMATION_SCHEMA.TABLE_CONSTRAINTS T 
on IC.TABLE_NAME=T.TABLE_NAME and
IC.TABLE_SCHEMA=T.TABLE_SCHEMA 
JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE C  
ON C.CONSTRAINT_NAME=T.CONSTRAINT_NAME  
and 
C.TABLE_NAME=T.TABLE_NAME
and T.CONSTRAINT_TYPE='PRIMARY KEY' and IC.TABLE_NAME='"""+tbl_name+"""' and IC.TABLE_CATALOG='"""+db+"""';"""
      #cursor = con.cursor()
      df = pd.read_sql(schm_query, con)
      return df



sg.theme('Topanga')



dc = ddl_check("STM_fmt.xlsx")
con=dc.create_connection_wa()

df_db = pd.read_sql("SELECT name FROM sys.databases;", con)
layout = [   
        [sg.Text('Choose your Database ',size=(30, 1), font='Lucida',justification='left')],
        [sg.Combo(df_db['name'].values.tolist(),size=(15,15),key='db')],
        [sg.Button('OK', font=('Times New Roman',12)),sg.Button('CANCEL', font=('Times New Roman',12))]
        ]

Window =sg.Window('Database Selection',layout)
e,v=Window.read()
Window.close()
db=v['db']

con=dc.create_connection_wa(db)

df_tbl = pd.read_sql("SELECT distinct TABLE_NAME  FROM  INFORMATION_SCHEMA.COLUMNS;", con)
layout = [   
        [sg.Text('Choose your Table ',size=(30, 1), font='Lucida',justification='left')],
        [sg.Combo(df_tbl['TABLE_NAME'].values.tolist(),size=(15,15),key='tbl')],
        [sg.Button('OK', font=('Times New Roman',12)),sg.Button('CANCEL', font=('Times New Roman',12))]
        ]

Window =sg.Window('Table Selection',layout)
e,v=Window.read()
Window.close()
tbl=v['tbl']


df_db =dc.get_schema(con,db,tbl)
print(df_db)

df_file=dc.read_file()

dfc.dataframe_cmp(df_db,df_file)

con.close()