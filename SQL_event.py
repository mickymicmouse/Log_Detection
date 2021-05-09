# -*- coding: utf-8 -*-
"""
Created on Thu May  6 15:27:06 2021

@author: seoun
"""

import pandas as pd
import os

Data_root = r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\Data"
df_sql_log = pd.read_csv(os.path.join(Data_root, "al_was_sql_info.csv"), encoding= "utf8")


import pickle

#%% SQL 데이터 로딩 
Data_root = r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\Data"
with open(os.path.join(Data_root, "al_was_sql_info"), "rb") as file:
    df_sql_log = pickle.load(file)

#%% 데이터 확인 
cols = df_sql_log.columns
sample = df_sql_log.head(20)
df_sql_log["app_nm"].value_counts()
len(df_sql_log["sql_syntax"].unique())
sql_value = df_sql_log["sql_syntax"].value_counts()

# 50이상의 sql 종류 
sql_value[sql_value>50]

df_sql_log['dept_name']

#%% unknown data 삭제 
new_df_sql_log=[]
for i in range(len(df_sql_log)):
    if i % 5000 ==0:
        print(i)
    dept_name = df_sql_log.iloc[i]['dept_name']
    if dept_name != "UNKNOWN":
        new_df_sql_log.append(df_sql_log.iloc[i])
new_df = pd.DataFrame(new_df_sql_log)

with open(os.path.join(Data_root, "known_sql_df"), "wb") as file:
    pickle.dump(new_df, file)

#%% SQL 로 이벤트 ID 생성
# SQL 를 통한 이벤트 ID 만들기 
# 총 2305개의 SQL 종류 존재
# n_min 을 통해 MOV로 넘길 sql 선정 
# ID sql_n 은 MOV 값으로 설정 
# ID sql_n +1 은 OOV 값으로 설정 
# 50 -> 430 30 -> 544 

df_sql_log = new_df.copy()

sql_value = df_sql_log["sql_syntax"].value_counts()
sql_n = len(sql_value)
total_n = len(df_sql_log)

n_min = 50
sql_unique = sql_value[sql_value>n_min].keys()
sql_n = len(sql_unique)


sql_dict = dict()
for i in range(sql_n):
    sql_dict[sql_unique[i]]=sql_unique[i]
sql_dict["MOV"]=sql_n
sql_dict["OOV"]=sql_n+1

event_id = []
keys = list(sql_dict.keys())
for i in range(total_n):
    if i%5000 == 0:
        print("%d 로그입니다." %i)
    sql_syn = df_sql_log.iloc[i]['sql_syntax']
    if sql_syn in keys:
        event_id.append(sql_dict[sql_syn])
    else:
        event_id.append(sql_dict['MOV'])


df = df_sql_log
df.reset_index(drop=True, inplace=True)
df['event_id']=pd.DataFrame(event_id)

# URL로 만든 event ID를 추가한 데이터 프레임 저장
with open(os.path.join(Data_root, "sql_event_id"), "wb") as file:
    pickle.dump(df, file)

#%% 