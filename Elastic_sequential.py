# -*- coding: utf-8 -*-
"""
Created on Thu Apr 15 17:28:32 2021

@author: seoun
"""

import pandas as pd
import numpy as np
import pickle
import os

# 데이터 로드
df_acc_log = pd.read_csv(r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\elasticData.csv", encoding= "utf8")

# 변수 선택
col = df_acc_log.columns
remove_cols=['Unnamed: 0', 'src_ip_long','end_time','was_ip','sg_keyword_reason_bit', 
             'logging_time_ui','str_time_ui','elapsed_time','logging_time','was_ip_long','download_check',
             'sg_multi_reason_bit','src_ip','sg_reason','was_country_lat','work_name','sys_crud_auth','was_trid',
             'sg_multi_reason','src_country_lat','security_grade','params','sys_id_auth','security_score',
             'work_time', 'end_time_ui','str_time','sg_keyword_reason','keyword_count','sg_reason_bit','acc_luid']
cols = list(set(col)-set(remove_cols))


# res 리스트에 각 로그의 데이터를 삽입하기
# 2차원 데이터 형태
# 임베딩 입력 데이터 형태로 변환 
res = []
for i in range(len(df_acc_log)):
    line = df_acc_log.loc[i,:]
    sent=[]
    if i%5000==0:
        print("%d 번째 로그입니다" %i)
    for c in cols:
        word = str(line[c])
        word = word.replace(" ","")
        if word=="" or word=="UNKNOWN" or word == "nan" or word == "none":
            continue
        else:    
            sent.append(word)
    res.append(sent)
    

Data_root = r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\Data"

with open(os.path.join(Data_root,"df_acc_log"),"rb") as file:
    df_acc_log = pickle.load(file)

with open(os.path.join(Data_root,"df_acc_log_tokenized"),"rb") as file:
    res = pickle.load(file)