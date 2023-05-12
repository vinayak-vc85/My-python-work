import time
import pandas as pd



myvars = {}
data_lst=[]
with open("input.txt") as myfile:
    for line in myfile:
        name, var = line.partition(":")[::2]
        myvars[name.strip()] = var.strip()
        
        if name.strip() =='':
            print('Inside space')
            print(myvars)
print(data_lst)

# print(myvars['SITE NAME'])
# for val in data_lst:
#     print(val)
#     print("#########################")
#     # print(pd.DataFrame.from_dict(val) )