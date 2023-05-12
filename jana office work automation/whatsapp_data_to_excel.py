import time
import pandas as pd


df=pd.read_excel('template.xlsx')
print(df)
myvars = {}
data_lst=[]
with open("input.txt") as myfile:
    for line in myfile:
        name, var = line.partition(":")[::2]
        myvars[name.strip()] = var.strip()
        
        if name.strip() =='':
            print('Inside space')
            print(myvars['HMR'] ,myvars["SITE I'D"])
            df.loc[df['Site ID']==myvars["SITE I'D"],'Present MED HMR']= myvars['HMR'] 
            df.loc[df['Site ID']==myvars["SITE I'D"],'Present MED EB reading']= myvars['EB'] 
            df.loc[df['Site ID']==myvars["SITE I'D"],' Month Filling Qty']= myvars['TOTAL FILLING'] 
            df.loc[df['Site ID']==myvars["SITE I'D"],' Present MED Total DC load']= myvars['TOTAL LOAD'] 
print(data_lst)
print(df[pd.notnull(df['Present MED HMR'])]['Present MED HMR'])
df.to_excel('output.xlsx')
