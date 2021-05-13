# -*- coding: utf-8 -*-
"""
Created on Thu May  6 15:27:06 2021

@author: seoun
"""

import pandas as pd
import os
import pickle

Data_root = r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\Data"


#%% 원본 데이터 로
df_sql_log = pd.read_csv(os.path.join(Data_root, "al_was_sql_info.csv"), encoding= "utf8")



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

#%% 부서이름별 정렬

with open(os.path.join(Data_root, "known_sql_df"),"rb") as file:
    df = pickle.load(file)

df.sort_values(by=['dept_name', 'exec_str_time'], inplace = True)

with open(os.path.join(Data_root, "sorted_df_sql_log_dept_name"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "sorted_df_sql_log_dept_name"), "rb") as file:
    df = pickle.load(file)
print("부서별 정렬")

#%% 유저이름별 정렬

with open(os.path.join(Data_root, "known_sql_df"),"rb") as file:
    df = pickle.load(file)

df.sort_values(by=['user_name', 'exec_str_time'], inplace = True)

with open(os.path.join(Data_root, "sorted_df_sql_log_user_name"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "sorted_df_sql_log_user_name"), "rb") as file:
    df = pickle.load(file)
print("부서별 정렬")


#%% SQL 로 이벤트 ID 생성
# SQL 를 통한 이벤트 ID 만들기 
# 총 2305개의 SQL 종류 존재
# n_min 을 통해 MOV로 넘길 sql 선정 
# ID sql_n 은 MOV 값으로 설정 
# ID sql_n +1 은 OOV 값으로 설정 
# 50 -> 430 30 -> 544 

log_entry = "user_name"

with open(os.path.join(Data_root, "sorted_df_sql_log_"+log_entry), "rb") as file:
    df_sql_log = pickle.load(file)

sql_value = df_sql_log["sql_syntax"].value_counts()
sql_n = len(sql_value)
total_n = len(df_sql_log)

n_min = 50
sql_unique = sql_value[sql_value>n_min].keys()
sql_n = len(sql_unique)


sql_dict = dict()
for i in range(sql_n):
    sql_dict[sql_unique[i]]=i
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


df = df_sql_log.copy()
df.reset_index(drop=True, inplace=True)
df['event_id']=pd.DataFrame(event_id)

# URL로 만든 event ID를 추가한 데이터 프레임 저장
with open(os.path.join(Data_root, "sorted_df_sql_log_eventID_"+log_entry), "wb") as file:
    pickle.dump(df, file)

#%% log entry & SQL event id 파일 생성
# log_entry 변수를 바꾸어서 진행(부서별(dept_name), 이름별(user_name))
log_entry = "user_name"

with open(os.path.join(Data_root, "sorted_df_sql_log_eventID_"+log_entry), "rb") as file:
    df = pickle.load(file)

dept_name = df[log_entry].unique()
dept_n = len(df[log_entry].unique())
dept_dict=dict()
for i in range(dept_n):
    dept_dict[dept_name[i]]=[]

for idx in range(len(df)):
    if idx%5000 == 0:
        print("%d 번째 로그입니다" %idx)
    dept_dict[df[log_entry][idx]].append(df.iloc[idx]['event_id'])

sql_seq = []
for k in dept_dict.keys():
    sql_seq.append(dept_dict[k])

sql_seq.sort(key = len, reverse = True)
with open(os.path.join(Data_root, "sql_seq_"+log_entry), "wb") as file:
    pickle.dump(sql_seq, file)

#%% train, valid 분할
log_entry = "user_name"
with open(os.path.join(Data_root, "sql_seq_"+log_entry), "rb") as file:
    sql_seq = pickle.load(file)

nums = len(df)
ratio = 0.8
train_num = int(nums*ratio)

# train과 valid의 개수를 비슷하게 맞추기 위함 
count = 0
idx = 0
for seq in sql_seq:
    idx += 1
    count += len(seq)
    if count>=train_num:
        break

sql_train = sql_seq[:idx]
sql_valid = sql_seq[idx:]

with open(os.path.join(Data_root, "sql_train_"+log_entry), "wb") as file:
    pickle.dump(sql_train, file)

with open(os.path.join(Data_root, "sql_valid_"+log_entry), "wb") as file:
    pickle.dump(sql_valid, file)



