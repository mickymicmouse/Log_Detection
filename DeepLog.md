# DeepLog

### 프로세스

#### 로그키 데이터 전처리

1. HDFS 파일 수집
2. Drain을 이용해서 변환
3. Block ID(하드 디스크 주소)로 그룹화 (시퀀스 데이터 생성)
4. 각 block ID별로 슬라이딩 윈도우 진행
5. 텐서화 시키기



#### 모델 실행

1. LSTM 모델 구현



[관련 github](https://github.com/donglee-afar/logdeep)



* 3가지 벡터를 모두 넣었을 경우

![image-20210415155900262](C:\Users\seoun\AppData\Roaming\Typora\typora-user-images\image-20210415155900262.png)

* sequential 벡터만 넣었을 경우

![image-20210415161203806](C:\Users\seoun\AppData\Roaming\Typora\typora-user-images\image-20210415161203806.png)





* 3가지 데이터

  * sequenctial

  ```python
  sequence_vector=[5,5,5,22,11,9,11,9,11,9] 
  ```

  * quantitative

  ```python
  sequence_vector=[5,5,5,22,11,9,11,9,11,9] 
  count_vector=[0]*28
  count_vector[5] = 3
  count_vector[9] = 3
  count_vector[11] = 3
  count_vector[22] = 1
  ```

  * semantic
    * 각 슬라이딩 윈도우 된 것을 event2semantic.json을 사용해서 진행
      * event2semantic.json = fasttext를 이용한 딕셔너리
    * 문장 벡터를 활용하여 sequence vector 변환
    * [vector 생성](https://github.com/donglee-afar/logdeep/issues/3)
    * Facebook 오픈 소스 빠른 텍스트 사전 훈련된 단어 벡터 모델을 사용하여 Word 벡터를 추출하고 tf-idf 방법을 사용하여 로그에 대한 문장 벡터를 생성합니다(각 엔트에 해당).신분증).
    * event2semantic.json 생성 코드

```python
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 10:54:57 2019

@author: lidongxu1
"""
import re
import spacy
import json

def data_read(filepath):
    fp = open(filepath, "r")
    datas = []  # 存储处理后的数据
    lines = fp.readlines()  # 读取整个文件数据
    i = 0  # 为一行数据
    for line in lines:
        row = line.strip('\n') # 去除两头的换行符，按空格分割
        datas.append(row)
        i = i + 1   
    fp.close()
    return datas

def camel_to_snake(name):
    """
    # To handle more advanced cases specially (this is not reversible anymore):
    # Ref: https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case  
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def replace_all_blank(value):
    """
    去除value中的所有非字母内容，包括标点符号、空格、换行、下划线等
    :param value: 需要处理的内容
    :return: 返回处理后的内容
    # https://juejin.im/post/5d50c132f265da03de3af40b
    # \W 表示匹配非数字字母下划线
    """
    result = re.sub('\W+', ' ', value).replace("_", ' ')
    result = re.sub('\d',' ',result)
    return result
# https://github.com/explosion/spaCy
# https://github.com/hamelsmu/Seq2Seq_Tutorial/issues/1
nlp = spacy.load('en_core_web_sm')
def lemmatize_stop(text):
    """
    https://stackoverflow.com/questions/45605946/how-to-do-text-pre-processing-using-spacy
    """
#    nlp = spacy.load('en_core_web_sm')
    document = nlp(text)
    # lemmas = [token.lemma_ for token in document if not token.is_stop]
    lemmas = [token.text for token in document if not token.is_stop]
    return lemmas

def dump_2_json(dump_dict, target_path):
    '''
    :param dump_dict: submits dict
    :param target_path: json dst save path
    :return:
    '''
    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, bytes):
                return str(obj, encoding='utf-8')
            return json.JSONEncoder.default(self, obj)

    file = open(target_path, 'w', encoding='utf-8')
    file.write(json.dumps(dump_dict, cls=MyEncoder, indent=4))
    file.close()

data = data_read('template.txt')
result = {}
for i in range(len(data)):
    temp = data[i]
    temp = camel_to_snake(temp)
    temp = replace_all_blank(temp)
    temp = " ".join(temp.split())
    temp = lemmatize_stop(temp)
    result[i] = temp
print(result)
dump_2_json(result, 'eventid2template.json')





# 单独保存需要用到的fasttext词向量
template_set = set()
for key in result.keys():
    for word in result[key]:
        template_set.add(word)

import io
from tqdm import tqdm

# https://github.com/facebookresearch/fastText/blob/master/docs/crawl-vectors.md
def load_vectors(fname):
    fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
    n, d = map(int, fin.readline().split())
    data = {}
    for line in tqdm(fin):
        tokens = line.rstrip().split(' ')
        data[tokens[0]] = map(float, tokens[1:])
    return data

fasttext = load_vectors('cc.en.300.vec')

template_fasttext_map = {}

for word in template_set:
    template_fasttext_map[word] = list(fasttext[word])
    

dump_2_json(template_fasttext_map,'fasttext_map.json')

import os
import json
import numpy as np
import pandas as pd
from collections import Counter
import math

def read_json(filename):
    with open(filename, 'r') as load_f:
        file_dict = json.load(load_f)
    return file_dict

eventid2template = read_json('eventid2template.json')
fasttext_map = read_json('fasttext_map.json')
print(eventid2template)
dataset = list()
with open('data/'+'deepLog_hdfs_train.txt', 'r') as f:
    for line in f.readlines():
        line = tuple(map(lambda n: n - 1, map(int, line.strip().split())))
        dataset.append(line)
print(len(dataset))
idf_matrix = list()
for seq in dataset:
    for event in seq:
        idf_matrix.append(eventid2template[str(event)])
print(len(idf_matrix))
idf_matrix = np.array(idf_matrix)
X_counts = []
for i in range(idf_matrix.shape[0]):
    word_counts = Counter(idf_matrix[i])
    X_counts.append(word_counts)
print(X_counts[1000])
X_df = pd.DataFrame(X_counts)
X_df = X_df.fillna(0)
print(len(X_df))
print(X_df.head())
events = X_df.columns
print(events)
X = X_df.values
num_instance, num_event = X.shape

print('tf-idf here')
df_vec = np.sum(X > 0, axis=0)
print(df_vec)
print('*'*20)
print(num_instance)
# smooth idf like sklearn
idf_vec = np.log((num_instance + 1)  / (df_vec + 1)) + 1
print(idf_vec)
idf_matrix = X * np.tile(idf_vec, (num_instance, 1))
X_new = idf_matrix
print(X_new.shape)
print(X_new[1000])

word2idf = dict()
for i,j in zip(events,idf_vec):
    word2idf[i]=j
    # smooth idf when oov
    word2idf['oov'] = (math.log((num_instance + 1)  / (29+1)) + 1)

print(word2idf)
def dump_2_json(dump_dict, target_path):
    '''
    :param dump_dict: submits dict
    :param target_path: json dst save path
    :return:
    '''
    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, bytes):
                return str(obj, encoding='utf-8')
            return json.JSONEncoder.default(self, obj)

    file = open(target_path, 'w', encoding='utf-8')
    file.write(json.dumps(dump_dict, cls=MyEncoder, indent=4))
    file.close()

dump_2_json(word2idf,'word2idf.json')
import json
import numpy as np
from collections import Counter

def read_json(filename):
    with open(filename, 'r') as load_f:
        file_dict = json.load(load_f)
    return file_dict

event2template = read_json('eventid2template.json')
fasttext = read_json('fasttext_map.json')
word2idf = read_json('word2idf.json')


event2semantic_vec = dict()
# todo :
# 计算每个seq的tf，然后计算句向量
for event in event2template.keys():
    template = event2template[event]
    tem_len = len(template)
    count = dict(Counter(template))
    for word in count.keys():
        # TF
        TF = count[word]/tem_len
        # IDF
        IDF = word2idf.get(word,word2idf['oov'])
        # print(word)
        # print(TF)
        # print(IDF)
        # print('-'*20)
        count[word] = TF*IDF
    # print(count)
    # print(sum(count.values()))
    value_sum = sum(count.values())
    for word in count.keys():
        count[word] = count[word]/value_sum
    semantic_vec = np.zeros(300)
    for word in count.keys():
        fasttext_weight = np.array(fasttext[word])
        semantic_vec += count[word]*fasttext_weight
    event2semantic_vec[event] = list(semantic_vec)
def dump_2_json(dump_dict, target_path):
    '''
    :param dump_dict: submits dict
    :param target_path: json dst save path
    :return:
    '''
    class MyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, bytes):
                return str(obj, encoding='utf-8')
            return json.JSONEncoder.default(self, obj)

    file = open(target_path, 'w', encoding='utf-8')
    file.write(json.dumps(dump_dict, cls=MyEncoder, indent=4))
    file.close()

dump_2_json(event2semantic_vec,'event2semantic_vec_sameoov.json')      
```

