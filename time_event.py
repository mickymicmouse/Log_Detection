# -*- coding: utf-8 -*-
"""
Created on Mon May 17 16:08:21 2021

@author: seoun
"""

#%% known data df_acc_log 로드하기

import pandas as pd
import pickle
import os

Data_root = r"C:\Users\seoun\Desktop\Labs\LogData Project\Embedding\Data"
with open(os.path.join(Data_root, "known_df"),"rb") as file:
    df = pickle.load(file)
    
#%% 부서코드별 정렬
with open(os.path.join(Data_root, "known_df"),"rb") as file:
    df = pickle.load(file)

# df = new_df.copy()

df.sort_values(by=['dept_code', 'str_time'], inplace = True)

with open(os.path.join(Data_root, "sorted_df_acc_log_dept_code"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "sorted_df_acc_log_dept_code"), "rb") as file:
    df = pickle.load(file)
print("부서별 정렬")


#%%