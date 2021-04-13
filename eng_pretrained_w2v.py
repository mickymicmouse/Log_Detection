# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 16:12:32 2021

@author: seoun
"""

import gensim
# 모델 다운로드 해야됨
# 다운로드 경로
# https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
model = gensim.models.keyedvectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
print(model.vectors.shape) # 모델의 크기 확인

print (model.similarity('this', 'is')) # 두 단어의 유사도 계산하기
print (model.similarity('post', 'book'))

print(model['book']) # 단어 'book'의 벡터 출력