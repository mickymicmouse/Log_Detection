# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 17:27:49 2021

@author: seoun
"""

import pandas as pd
import numpy as np

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

# product_name = all UNKNOWN value

np_acc_log = np.array(df_acc_log)

sample=[]
for line in np_acc_log[:10]:
    sample.append(line)
    

df_info = df_acc_log.info()
df = df_acc_log[cols]

df['dept_code'][df['dept_code']!="UNKNOWN"]

# res 리스트에 각 로그의 데이터를 삽입하기
# 2차원 데이터 형태
# 임베딩 입력 데이터 형태로 변
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

# 정수 인코딩









# 워드 임베딩!
#Word2Vec 학습
from gensim.models import Word2Vec
model = Word2Vec(sentences = res, vector_size= 50, window = 10, min_count=10, workers = 4, sg = 1)

# size = 워드 벡터의 특징 값. 즉, 임베딩 된 벡터의 차원.
# window = 컨텍스트 윈도우 크기
# min_count = 단어 최소 빈도 수 제한 (빈도가 적은 단어들은 학습하지 않는다.)
# workers = 학습을 위한 프로세스 수
# sg = 0은 CBOW, 1은 Skip-gram.

model_result = model.wv.most_similar("UNKNOWN")
print(model_result)
model.wv.vectors.shape

#유사도 비교
model.wv.similarity("x","x")

# 모델 save & load
from gensim.models import KeyedVectors
model.wv.save_word2vec_format('eng_w2v')
loaded_model = KeyedVectors.load_word2vec_format('eng_w2v')

# 글로브 모델 학습
from glove import Corpus, Glove

corpus = Corpus()
corpus.fit(res, window = 1)

glove = Glove(no_components = 100, learning_rate = 0.05)
glove.fit(corpus.matrix, epochs = 20, no_threads=4, verbose=True)
glove.add_dictionary(corpus.dictionary)

glove.most_similar("351")


# 패스트 텍스트 훈련
from gensim.models import FastText
model = FastText(res, vector_size=100, window = 5, min_count=5, workers=4, sg=1)
model_result =model.wv.most_similar("electorfi")

