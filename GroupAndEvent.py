# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 17:28:32 2021

@author: seoun
"""

import pandas as pd
import pickle
import os
#%% 데이터 로드 및 변수 선택
# 데이터 로드
Data_root = r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\Data"
df_acc_log = pd.read_csv(r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\elasticData.csv", encoding= "utf8")

# 변수 선택
col = df_acc_log.columns
remove_cols=['Unnamed: 0', 'src_ip_long','end_time','was_ip','sg_keyword_reason_bit', 
             'logging_time_ui','str_time_ui','elapsed_time','logging_time','was_ip_long','download_check',
             'sg_multi_reason_bit','src_ip','sg_reason','was_country_lat','work_name','sys_crud_auth','was_trid',
             'sg_multi_reason','src_country_lat','security_grade','params','sys_id_auth','security_score',
             'work_time', 'end_time_ui','sg_keyword_reason','keyword_count','sg_reason_bit','acc_luid']
cols = list(set(col)-set(remove_cols))
df = df_acc_log[cols]

# 변수 정리된 데이터 프레임 저장
with open(os.path.join(Data_root, "df"), "wb") as file:
    pickle.dump(df, file)


#%% 그룹화 - log entry 생성(부서별, 개인별, 직급별, 시간별)
# 부서 이름별 정렬
with open(os.path.join(Data_root, "df"),"rb") as file:
    df = pickle.load(file)
    
df.sort_values(by=['dept_name', 'str_time'], inplace = True)

with open(os.path.join(Data_root, "sorted_df_acc_log_dept_name"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "sorted_df_acc_log_dept_name"), "rb") as file:
    df = pickle.load(file)
print("부서이름별 정렬")


#%% 부서코드별 정렬
with open(os.path.join(Data_root, "df"),"rb") as file:
    df = pickle.load(file)

df.sort_values(by=['dept_code', 'str_time'], inplace = True)

with open(os.path.join(Data_root, "sorted_df_acc_log_dept_code"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "sorted_df_acc_log_dept_code"), "rb") as file:
    df = pickle.load(file)
print("부서별 정렬")
#%% 직급이름별 정렬
with open(os.path.join(Data_root, "df"),"rb") as file:
    df = pickle.load(file)
    
df.sort_values(by=['position_name', 'str_time'], inplace = True)

with open(os.path.join(Data_root, "sorted_df_acc_log_position_name"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "sorted_df_acc_log_position_name"), "rb") as file:
    df = pickle.load(file)
print("직급이별 정렬")

#%% 직급별 정렬
with open(os.path.join(Data_root, "df"),"rb") as file:
    df = pickle.load(file)
    
df.sort_values(by=['position_code', 'str_time'], inplace = True)

with open(os.path.join(Data_root, "sorted_df_acc_log_position_code"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "sorted_df_acc_log_position_code"), "rb") as file:
    df = pickle.load(file)
print("직급별 정렬")


#%% 개인별 정렬
with open(os.path.join(Data_root, "df"),"rb") as file:
    df = pickle.load(file)
    
df.sort_values(by=['user_sn', 'str_time'], inplace = True)

with open(os.path.join(Data_root, "sorted_df_acc_log_user_sn"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "sorted_df_acc_log_user_sn"), "rb") as file:
    df = pickle.load(file)
print("개인별 정렬")

#%% 시간별 정렬
# 사실상 전체 데이터를 넣는 것
with open(os.path.join(Data_root, "df"),"rb") as file:
    df = pickle.load(file)
    
df.sort_values(by=['str_time'], inplace = True)

with open(os.path.join(Data_root, "sorted_df_acc_log_time"), "wb") as file:
    pickle.dump(df, file)
    
with open(os.path.join(Data_root, "sorted_df_acc_log_time"), "rb") as file:
    df = pickle.load(file)
print("시간별 정렬")


#%% URL로 이벤트 ID 생성
# URI를 통한 이벤트 ID 만들기 
# 총 427개의 URI 종류 존재
# ID 427 은 OOV 값으로 설정
log_entry = "time"

with open(os.path.join(Data_root, "sorted_df_acc_log_"+log_entry), "rb") as file:
    df = pickle.load(file)

uri_n = len(df['uri'].value_counts())
dfvc = df['uri'].value_counts()
uri_unique = df['uri'].unique()

uri_dict = dict()
for i in range(uri_n):
    uri_dict[uri_unique[i]]=i
uri_dict["OOV"]=uri_n


event_id = []
for i in range(len(df)):
    if i%5000 == 0:
        print("%d 로그입니다." %i)
    event_id.append(uri_dict[df.iloc[i]['uri']])

df.reset_index(drop=True, inplace=True)
df['event_id']=pd.DataFrame(event_id)

# URL로 만든 event ID를 추가한 데이터 프레임 저장
with open(os.path.join(Data_root, "sorted_df_acc_log_eventID_"+log_entry), "wb") as file:
    pickle.dump(df, file)






#%% log entry & URL event id 파일 생성
# log_entry 변수를 바꾸어서 진행(부서별(dept_code), 직급별(position_code), 개인별(user_id))
log_entry = "dept_name"

with open(os.path.join(Data_root, "sorted_df_acc_log_eventID_"+log_entry), "rb") as file:
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
with open(os.path.join(Data_root, "uri_seq_"+log_entry), "wb") as file:
    pickle.dump(uri_seq, file)

#%% train, valid 분할
log_entry = "dept_name"
with open(os.path.join(Data_root, "uri_seq_"+log_entry), "rb") as file:
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

with open(os.path.join(Data_root, "uri_train_"+log_entry), "wb") as file:
    pickle.dump(uri_train, file)

with open(os.path.join(Data_root, "uri_valid_"+log_entry), "wb") as file:
    pickle.dump(uri_valid, file)

#%% 저장 확인
with open(os.path.join(Data_root, "uri_train_dept_code"), "rb") as file:
    train = pickle.load(file)
with open(os.path.join(Data_root, "uri_valid_dept_code"), "rb") as file:
    valid1 = pickle.load(file)
    
with open(os.path.join(Data_root, "uri_train"), "rb") as file:
    train2 = pickle.load(file)
with open(os.path.join(Data_root, "uri_valid"), "rb") as file:
    valid2 = pickle.load(file)
    
with open(os.path.join(Data_root, "uri_valid_user_sn"), "rb") as file:
    valid3 = pickle.load(file)
with open(os.path.join(Data_root, "uri_valid_position_code"), "rb") as file:
    valid4 = pickle.load(file)
#%% log entry & URL event id 파일 생성
# 전체데이터(시간으로 sorting)에 대해 데이터 생성

log_entry = "time"
with open(os.path.join(Data_root, "sorted_df_acc_log_eventID_"+log_entry), "rb") as file:
    df = pickle.load(file)

uri_seq=[]
for idx in range(len(df)):
    if idx%5000 == 0:
        print("%d 번째 로그입니다" %idx)
    uri_seq.append(df.iloc[idx]['event_id'])

nums = len(df)
ratio=0.8
train_num = int(nums*ratio)
uri_train = [uri_seq[:train_num]]
uri_valid = [uri_seq[train_num:]]

with open(os.path.join(Data_root, "uri_train_"+log_entry), "wb") as file:
    pickle.dump(uri_train, file)

with open(os.path.join(Data_root, "uri_valid_"+log_entry), "wb") as file:
    pickle.dump(uri_valid, file)


