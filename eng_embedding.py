# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 13:13:09 2021

@author: seoun
"""

import nltk
nltk.download('punkt')

import urllib.request
import zipfile
from lxml import etree
import re
from nltk.tokenize import word_tokenize, sent_tokenize


# 데이터 이해하기
urllib.request.urlretrieve(r"https://raw.githubusercontent.com/GaoleMeng/RNN-and-FFNN-textClassification/master/ted_en-20160408.xml", 
                           filename = "ted_en-20160408.xml")

targetXML = open(r'C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\ted_en-20160408.xml','r',encoding='UTF8')
target_text = etree.parse(targetXML)

# xml 파일로 부터 <content> </content> 사이의 내용 불러오기
parse_text = '\n'.join(target_text.xpath('//content//text()'))

#괄호로 구성된 내용 제거
content_text = re.sub(r'\([^)]*\)', '', parse_text)

# 입력 코퍼스에 대해 nltk를 이용하여 문장 토큰화 수행
sent_text = sent_tokenize(content_text)

normalized_text = []
for string in sent_text:
    tokens = re.sub(r"[^a-z0-9]+"," ", string.lower())
    normalized_text.append(tokens)

result = [word_tokenize(sentence) for sentence in normalized_text]


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




