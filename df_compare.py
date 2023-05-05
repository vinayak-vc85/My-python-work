import pandas as pd
import numpy as np
from tkinter import filedialog
from pathlib import Path
import PySimpleGUI as sg
#import style_excel as se

class df_compare:
    def __init__(self, filename='sttm_difference.xlsx'):
        self.filename = filename
        
        

def check_columns(list1,list2):
    for val in list1:
        if val in list2:
            pass
        else:
            print("[Warning:] The column named {}, that you entered is not in the column list of second dataframe. kindly check the column name".format(val))


def write_excel(writer,DataFrame,sheetname):

    
    DataFrame.to_excel(writer, sheet_name=sheetname, na_rep='', float_format=None,  header=True, index=False)
    
    if sheetname!="All Difference":
        for column in DataFrame:
            column_length = max(DataFrame[column].astype(str).map(len).max(), len(column))
            col_idx = DataFrame.columns.get_loc(column)
            writer.sheets[sheetname].set_column(col_idx, col_idx, column_length)
    else:
        pass


def dataframe_cmp(df_left_ns,df_right_ns):

    sg.theme('Topanga') 
    writer = pd.ExcelWriter('sttm_difference.xlsx', engine='xlsxwriter')
    left_cols=list(df_left_ns.columns)
    right_cols=list(df_right_ns.columns)

    

    for count, item in enumerate(left_cols):
        if left_cols[count]!=right_cols[count]:
            print("cols not matching",left_cols[count],right_cols[count])
            df_right_ns.rename(columns={right_cols[count]: item}, inplace=True)
    

    df_left = df_left_ns.apply(lambda x: x.str.strip() if x.dtype == "object" else x).astype(str)
    df_right = df_right_ns.apply(lambda x: x.str.strip() if x.dtype == "object" else x).astype(str)

    df_left.drop_duplicates(subset=None, keep='first', inplace=True)
    df_right.drop_duplicates(subset=None, keep='first', inplace=True)

    col_list=list(df_left.columns)
    layout = [[sg.Text("Choose your key columns: ",size=(25,1)),
                    sg.Listbox(col_list,key="h",select_mode="multiple",size=(30,15))],
        [sg.Submit(), sg.Cancel()]]
    window = sg.Window('SChema Check', layout)
    event, mul_values = window.read()
    window.close()
    user_list=mul_values['h']
    print("Choosen values :  ",user_list )


    check_columns(user_list,list(df_left.columns))
    check_columns(user_list,list(df_right.columns))
    col_list=list(df_right.columns)

    for val in user_list:
        col_list.remove(val)
    for val in col_list:
        if val in df_left.columns:
            col_list = [val+'_y' if i==val else i for i in col_list]
    print(col_list)

    #Creating empty dataframes
    df_all_matches = pd.DataFrame()
    df_all_diffference = pd.DataFrame()
    result = pd.DataFrame()

    df_left_join = df_left.merge(df_right, how = 'outer' ,indicator=True,on=user_list).drop(columns=col_list).loc[lambda x : x['_merge']=='left_only']
    #print(df_left_join)
    left_cols=list(df_left_join.columns)
    write_excel(writer,df_left_join,"Left file only")

    df = df_left.merge(df_right, how = 'outer' ,indicator=True,on=user_list).loc[lambda x : x['_merge']=='right_only']
    print(df)
    for val in user_list:
        col_list.insert(len(user_list), val)
    new_col_list=list(df_left_join.columns)
    for i in range(len(new_col_list)):
        if new_col_list[i].endswith("_x"):
            new_col_list[i] = str(new_col_list[i]).replace('_x','_y')
    print(df.columns)
    print("$$$$$$$$$$$$$$44444")
    print(new_col_list)
    new_df_right=df[new_col_list]
    print(new_df_right)
    new_df_right["_merge"]="right_only"
    write_excel(writer,new_df_right,"Right file only")

    for val in user_list:
        col_list.remove(val)
    df=pd.merge(df_left,df_right,on=user_list).drop(columns=col_list)
    df['_merge']="both_sources"
    #print(df)
    col_values=df[user_list].drop_duplicates().values.tolist()
    for val in user_list:
        for colval in col_values:
            print(colval[0])
        
            df_left_row_us = df_left[df_left[val] == colval[0]]
            df_left_row = df_left_row_us.sort_values(user_list)
            df_left_row.fillna(value = ' ',inplace = True)
            #print("Left file data:")  
            #print(df_left_row)

            df_right_row_us = df_right[df_right[val] == colval[0]].set_axis(list(df_left.columns), axis=1)
            df_right_row = df_right_row_us.sort_values(user_list)
            df_right_row.fillna(value = ' ',inplace = True)
            #print("Right file data:")  
            #print(df_right_row)
            
        
            df_left_row=df_left_row.replace(np.nan, '').astype(str)
            df_right_row=df_right_row.replace(np.nan, '').astype(str)
        
            try:
                df3 = pd.merge(df_left_row, df_right_row, how='outer', indicator='Exist')
            except:
                print("Left data types:")
                print(df_left_row.dtypes)
                print("Right data types:")
                print(df_right_row.dtypes)
            df2= df3.loc[df3['Exist']=='both']
            #print(df2)
            df3 = df3.loc[df3['Exist'] != 'both']
            df_all_matches=df_all_matches.append(df2)
            #print(df3)
            if df3.empty:
                pass
            
            else:
                
                comparevalues = df_left_row.values == df_right_row .values
                print(comparevalues)

                rows,cols = np.where(comparevalues==False)
                
                for item in zip(rows,cols):
                                
                    try:
                        df_left_row.iloc[item[0],item[1]] = ' {} --> {} '.format(df_left_row.iloc[item[0], item[1]], df_right_row.iloc[item[0],item[1]])
                    except:
                        print("rows and cols  ",item[0],item[1])     
                        print(df_left_row)  
                        print("#####right row is #########")
                        print(df_right_row)
                    df_all_diffference=df_all_diffference.append(df_left_row.iloc[item[0]])
    df_all_diffference.drop_duplicates()
    df_all_diffference_exception=df_all_diffference
    df_all_diffference = (df_all_diffference.style.applymap(lambda v: 'background-color: lightcoral; color:white;font-size: 10pt;border-collapse:collapse' if '-->' in str(v)  else ''))

            
                
        
    #print(df_all_diffference)    
    try:
        write_excel(writer,df_all_diffference,"All Difference")  
    except:
        write_excel(writer,df_all_diffference_exception,"All Difference")  

    print("Both Matches")
    print(df_all_matches)
    write_excel(writer,df_all_matches,"Both Matches") 
    writer.save()       

    layout = [[sg.Text('Process Completed ! ')], [sg.Button("OK")]]

    # Create the window
    window = sg.Window("Completion", layout,size=(400, 100),element_justification='c')

    # Create an event loop
    while True:
        event, values = window.read()
        # End program if user closes window or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break
    #s=se.style_excel()
    #s.perform_style()
    window.close()


def dataframe_cmp_only(df_left_ns,df_right_ns,key_col):

    
    left_cols=list(df_left_ns.columns)
    right_cols=list(df_right_ns.columns)
    user_list=[]
    

    for count, item in enumerate(left_cols):
        if left_cols[count]!=right_cols[count]:
            print("cols not matching",left_cols[count],right_cols[count])
            df_right_ns.rename(columns={right_cols[count]: item}, inplace=True)
    

    df_left = df_left_ns.apply(lambda x: x.str.strip() if x.dtype == "object" else x).astype(str)
    df_right = df_right_ns.apply(lambda x: x.str.strip() if x.dtype == "object" else x).astype(str)

    df_left.drop_duplicates(subset=None, keep='first', inplace=True)
    df_right.drop_duplicates(subset=None, keep='first', inplace=True)

    col_list=list(df_left.columns)
   
    user_list.append(key_col)
    print("Key column is :  ",user_list )


    check_columns(user_list,list(df_left.columns))
    check_columns(user_list,list(df_right.columns))
    col_list=list(df_right.columns)

    for val in user_list:
        col_list.remove(val)
    for val in col_list:
        if val in df_left.columns:
            col_list = [val+'_y' if i==val else i for i in col_list]
    print(col_list)

    #Creating empty dataframes
    df_all_matches = pd.DataFrame()
    df_all_diffference = pd.DataFrame()
   


    for val in user_list:
        col_list.remove(val)
    df=pd.merge(df_left,df_right,on=user_list).drop(columns=col_list)
    df['_merge']="both_sources"
    #print(df)
    col_values=df[user_list].drop_duplicates().values.tolist()
    for val in user_list:
        for colval in col_values:
            print(colval[0])
        
            df_left_row_us = df_left[df_left[val] == colval[0]]
            df_left_row = df_left_row_us.sort_values(user_list)
            df_left_row.fillna(value = ' ',inplace = True)
            #print("Left file data:")  
            #print(df_left_row)

            df_right_row_us = df_right[df_right[val] == colval[0]].set_axis(list(df_left.columns), axis=1)
            df_right_row = df_right_row_us.sort_values(user_list)
            df_right_row.fillna(value = ' ',inplace = True)
            #print("Right file data:")  
            #print(df_right_row)
            
        
            df_left_row=df_left_row.replace(np.nan, '').astype(str)
            df_right_row=df_right_row.replace(np.nan, '').astype(str)
        
            try:
                df3 = pd.merge(df_left_row, df_right_row, how='outer', indicator='Exist')
            except:
                print("Left data types:")
                print(df_left_row.dtypes)
                print("Right data types:")
                print(df_right_row.dtypes)
            df2= df3.loc[df3['Exist']=='both']
            #print(df2)
            df3 = df3.loc[df3['Exist'] != 'both']
            df_all_matches=df_all_matches.append(df2)
            #print(df3)
            if df3.empty:
                pass
            
            else:
                
                comparevalues = df_left_row.values == df_right_row .values
                print(comparevalues)

                rows,cols = np.where(comparevalues==False)
                
                for item in zip(rows,cols):
                                
                    try:
                        df_left_row.iloc[item[0],item[1]] =   df_right_row.iloc[item[0],item[1]]
                    except:
                        print("rows and cols  ",item[0],item[1])     
                        print(df_left_row)  
                        print("#####right row is #########")
                        print(df_right_row)
                    df_all_diffference=df_all_diffference.append(df_left_row.iloc[item[0]])
    return df_all_diffference.drop_duplicates()

      