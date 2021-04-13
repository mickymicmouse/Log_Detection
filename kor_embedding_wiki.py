# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 15:52:02 2021

@author: seoun
"""
# 위키 파일을 다운받는다.
# wikiextractor를 사용하여 데이터만 추출

f = open(r'C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\wiki_data.txt', encoding='utf8')
i = 0
while True:
    line = f.readline()
    if line!='\n':
        i+=1
        print("%d번째 줄 : " %i + line)
    if i==5:
        break
f.close()


from konlpy.tag import Okt
okt = Okt()
fread = open(r'C:\Users\seoun\OneDrive\Desktop\Labs\LogData Project\Embedding\wiki_data.txt', encoding='utf8')
n=0
result=[]

while True:
    line = fread.readline()
    if not line: 
        break
    n+=1
    if n%5000:
        print("%d 번째 줄" %n)
    tokenlist = okt.pos(line, stem= True, norm=True)
    temp=[]
    for word in tokenlist:
        if word[1] in ["Noun"]: #명사인지
            temp.append(word[0])
    if temp:
        result.append(temp)
fread.close()

# 각 줄마다 명사만 모아서 만듦

print('총 샘플의 개수 : {}'.format(len(result)))

# Word2Vec 훈련 시키기

from gensim.models import Word2Vec
model = Word2Vec(sentences = result, vector_size = 100, window = 5, min_count=5, workers =4, sg=0)
model_result1 = model.wv.most_similar("대한민국")

