# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 21:18:16 2021

@author: seoun
"""

import pickle
import os
import pandas as pd

df_sql_info = pd.read_csv(r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\Data\al_was_sql_info.csv", encoding = "utf8")
col = df_sql_info.columns

sample = df_sql_info.head()

Data_root = r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\Data"
with open(os.path.join(Data_root, "df_sql_info"), "wb") as file:
    pickle.dump(df_sql_info, file)
    
with open(os.path.join(Data_root, "df_sql_info"), "rb") as file:
    df_sql_info=pickle.load(file)

# sql 로그 파일 생성
with open(os.path.join(Data_root, "sql.log"), "w", encoding='utf8') as file:
    for i in range(len(df_sql_info)):
        line = df_sql_info['sql_syntax'][i]
        # if i==len(df_sql_info)-1:
        #     line = df_sql_info['sql_syntax'][i]
        file.writelines(line)
    file.close()


# sql 파싱 
from moz_sql_parser import parse
t = df_sql_info['sql_syntax'][1100].replace("?", "param")
p = parse(t)

#부서별로 결합 후 정렬
df = df_sql_info[['sql_syntax','dept_name', 'exec_str_time']]
#부서로 정렬 이후 같은 부서 내에서 시간 순 정렬
df.sort_values(by=['dept_name','exec_str_time'], inplace = True)

with open(os.path.join(Data_root, "df_sql_info_sorted"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "df_sql_info_sorted"), "rb") as file:
    df=pickle.load(file)
