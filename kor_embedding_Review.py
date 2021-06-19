# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 13:58:00 2021

@author: seoun
"""

import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt

urllib.request.urlretrieve("https://raw.githubusercontent.com/e9t/nsmc/master/ratings.txt", filename="ratings.txt")
train_data = pd.read_table('ratings.txt')
print(len(train_data))
#널 값 존재 확인
print(train_data.isnull().values.any())
#널 값 삭제
train_data = train_data.dropna(how='any')
#한글 외 문자 제거
train_data['document'] = train_data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")
#불용어 처리
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

okt = Okt()
tokenized_data=[]
for sentence in train_data['document']:
    temp_X = okt.morphs(sentence, stem = True) # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords]
    tokenized_data.append(temp_X)

print('리뷰 최대 길이 : ', max(len(l) for l in tokenized_data))
print('리뷰 평균 길이 : ', sum(map(len, tokenized_data))/len(tokenized_data))

# 리뷰 길이 분포 확인
print('리뷰의 최대 길이 :',max(len(l) for l in tokenized_data))
print('리뷰의 평균 길이 :',sum(map(len, tokenized_data))/len(tokenized_data))
plt.hist([len(s) for s in tokenized_data], bins=50)
plt.xlabel('length of samples')
plt.ylabel('number of samples')
plt.show()

#word2vec 훈련(임베딩 모델)
from gensim.models import Word2Vec
model = Word2Vec(sentences = tokenized_data, vector_size = 100, window =5, min_count =5, workers=4,sg=0)
model.wv.vectors.shape
model.wv.vectors
model.wv.most_similar("행운")

