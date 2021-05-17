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

#%% 직급별 정렬
with open(os.path.join(Data_root, "known_df"),"rb") as file:
    df = pickle.load(file)

# df = new_df.copy()

df.sort_values(by=['position_code', 'str_time'], inplace = True)

with open(os.path.join(Data_root, "sorted_df_acc_log_position_code"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "sorted_df_acc_log_position_code"), "rb") as file:
    df = pickle.load(file)
print("직급별 정렬")


#%% 개인별 정렬 
with open(os.path.join(Data_root, "known_df"),"rb") as file:
    df = pickle.load(file)
    
# df = new_df.copy()    

df.sort_values(by=['user_sn', 'str_time'], inplace = True)

with open(os.path.join(Data_root, "sorted_df_acc_log_user_sn"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "sorted_df_acc_log_user_sn"), "rb") as file:
    df = pickle.load(file)
print("개인별 정렬")

#%% str time을 event ID로 생성
# class = 49 48time + 1OOV
log_entry = "dept_code"

with open(os.path.join(Data_root, "sorted_df_acc_log_"+log_entry), "rb") as file:
    df = pickle.load(file)
    

df['str_time'].head()
df.columns

df['str_time'].iloc[1].split("T")

import datetime as dt

time_dict = dict()
eventid=0
for i in range(24):
    for j in range(2):
        
        minute = str(30*j)
        hour = str(i)
        time_dict[hour+":"+minute]=eventid
        eventid+=1
time_dict["OOV"]=48

event_id = []
for i in range(len(df)):
    if i%5000 == 0:
        print("%d 로그입니다." %i)
        
    t = df.iloc[i]['str_time'].split("T")[1]
    t = t.split(":")
    hour = str(int(t[0]))
    minute = int(t[1])
    if minute<30:
        minute = "0"
    else:
        minute = "30"
    event_id.append(time_dict[hour+":"+minute])

df.reset_index(drop=True, inplace=True)
df['event_id']=pd.DataFrame(event_id)

# URL로 만든 event ID를 추가한 데이터 프레임 저장
with open(os.path.join(Data_root, "sorted_df_acc_log_time_eventID_"+log_entry), "wb") as file:
    pickle.dump(df, file)
    
#%% log entry & time event id 파일 생성
# log_entry 변수를 바꾸어서 진행(부서별(dept_code), 직급별(position_code), 개인별(user_id))
log_entry = "dept_code"

with open(os.path.join(Data_root, "sorted_df_acc_log_time_eventID_"+log_entry), "rb") as file:
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

uri_seq = []
for k in dept_dict.keys():
    uri_seq.append(dept_dict[k])

uri_seq.sort(key = len, reverse = True)
with open(os.path.join(Data_root, "time_seq_"+log_entry), "wb") as file:
    pickle.dump(uri_seq, file)

#%% train, valid 분할
log_entry = "dept_code"
with open(os.path.join(Data_root, "time_seq_"+log_entry), "rb") as file:
    uri_seq = pickle.load(file)

nums = len(df)
ratio = 0.8
train_num = int(nums*ratio)

# train과 valid의 개수를 비슷하게 맞추기 위함 
count = 0
idx = 0
for seq in uri_seq:
    idx += 1
    count += len(seq)
    if count>=train_num:
        break

uri_train = uri_seq[:idx]
uri_valid = uri_seq[idx:]

with open(os.path.join(Data_root, "time_train_"+log_entry), "wb") as file:
    pickle.dump(uri_train, file)

with open(os.path.join(Data_root, "time_valid_"+log_entry), "wb") as file:
    pickle.dump(uri_valid, file)
