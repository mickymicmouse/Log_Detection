# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 17:27:49 2021

@author: seoun
"""

import pandas as pd
import numpy as np

df_acc_log = pd.read_csv(r"C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\elasticData.csv", encoding= "utf8")
col = df_acc_log.columns
cols = ['dept_code','company_code','position_code','app_nm']

# product_name = all UNKNOWN value

np_acc_log = np.array(df_acc_log)

sample=[]
for line in np_acc_log[:10]:
    sample.append(line)
    

df_info = df_acc_log.info()

df = df_acc_log[cols]

df['product_name'][df['product_name']!="UNKNOWN"]


#Word2Vec 학습
from gensim.models import Word2Vec
model = Word2Vec(sentences = result, vector_size= 100, window = 5, min_count=5, workers = 4, sg = 0)

# size = 워드 벡터의 특징 값. 즉, 임베딩 된 벡터의 차원.
# window = 컨텍스트 윈도우 크기
# min_count = 단어 최소 빈도 수 제한 (빈도가 적은 단어들은 학습하지 않는다.)
# workers = 학습을 위한 프로세스 수
# sg = 0은 CBOW, 1은 Skip-gram.

model_result = model.wv.most_similar("hot")
print(model_result)

#유사도 비교
model.wv.similarity("x","x")

# 모델 save & load
from gensim.models import KeyedVectors
model.wv.save_word2vec_format('eng_w2v')
loaded_model = KeyedVectors.load_word2vec_format('eng_w2v')