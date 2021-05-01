# -*- coding: utf-8 -*-
"""
Created on Tue May 21 08:57:08 2019

@author: stjepan
"""

import numpy as np 
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split 
 
n_stages = 128
n_crp = 1000 

stage_delays = np.random.normal(size=n_stages+1) 
#print(stage_delays)

x = [] 
y = [] 

for _ in range(n_crp): 
    challenge_vector = np.random.randint(2, size=n_stages) 
    #print(challenge_vector)
    feature_vector = [] 
    for i in range(n_stages): 
        feature = 1 
        for j in range(i, n_stages): 
            feature = feature * pow(-1, challenge_vector[j])
        feature_vector.append(feature) 
    feature_vector.append(1)
    #print(feature_vector)
    puf_result = np.dot(stage_delays, feature_vector) > 0 
    x.append(feature_vector) 
    y.append(puf_result)

x_array = np.array(x) 
y_array = np.array(y)    
#print(x_array.shape)
#print(y_array.shape)

X_train, X_test, Y_train, Y_test = train_test_split(x_array, y_array, test_size = 0.2, random_state = 0)
print(X_train.shape)
clf = LogisticRegression(solver="lbfgs").fit(X_train, Y_train)
print(clf.score(X_train, Y_train))
Y_pred = clf.predict(X_test)
print(clf.score(X_test, Y_test))

