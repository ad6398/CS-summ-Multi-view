# -*- coding: utf-8 -*-
"""Stage_Segmentation.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TsopJgxCAPmXqWMbYGtvThy3wfs86sKu
"""

import pickle
with open('train_sentence_transformer.pkl', 'rb') as f:
    train = pickle.load(f)
with open('val_sentence_transformer.pkl', 'rb') as f:
    val = pickle.load(f)
with open('test_sentence_transformer.pkl', 'rb') as f:
    test = pickle.load(f)

import json
with open('test.json', encoding = 'utf8') as json_file:
    data = json.load(json_file)
    
conversations = []
summaries = []
for i in range(0, len(data)):
    if len(data[i]['dialogue'].split('\r\n')) > 1:
        sentences = data[i]['dialogue'].split('\r\n')
    else:
        sentences = data[i]['dialogue'].split('\n')

    conversations.append(sentences)
    summaries.append(data[i]['summary'].strip('\n').replace('\r\nt', ' '))

import numpy as np
length = []
for i in range(0, len(train)):
    length.append(len(train[i]))
for i in range(0, len(val)):
    length.append(len(val[i]))
for i in range(0, len(test)):
    length.append(len(test[i]))
X = []
for i in range(0, len(train)):
    for j in range(0, len(train[i])):
        X.append(np.array(train[i][j]))
for i in range(0, len(val)):
    for j in range(0,len(val[i])):
        X.append(np.array(val[i][j]))
for i in range(0, len(test)):
    for j in range(0, len(test[i])):
        X.append(np.array(test[i][j]))

from hmmlearn import hmm

remodel = hmm.GaussianHMM(n_components=4, n_iter = 50, covariance_type = 'diag', verbose = True, init_params="cm", params="cmts")
remodel.startprob_ = np.array([1, 0.0, 0.0, 0.0])
remodel.transmat_ = np.array([
                 [0.33, 0.34, 0.33, 0],
                 [0.0, 0.33, 0.34, 0.33],
                 [0.0, 0.0, 0.5, 0.5],
                 [0.0, 0.0, 0.0, 1.0]]
                            )

remodel.startprob_

remodel.transmat_

remodel.fit(X, length)

remodel.transmat_

remodel.startprob_

def encode_convs(profix):
    sent_label = []
    with open(profix + '_sentence_transformer.pkl', 'rb') as f:
        data = pickle.load(f)
    for i in range(0, len(data)):
        labels = remodel.decode(np.array(data[i]))[1]
        sent_label.append(labels)
    
    with open(profix + '_sent_trans_cons_label.pkl', 'wb') as f:
        pickle.dump(sent_label, f)
    return sent_label

l = encode_convs('train')

l = encode_convs('val')

l = encode_convs('test')
