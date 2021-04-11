import pandas as pd
import re
import os
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import numpy as np
from sklearn.ensemble import AdaBoostClassifier

Train_data = pd.read_csv("DogsVsCats_train.txt",sep =' ',header=None)
Test_data = pd.read_csv("DogsVsCats_test.txt",sep =' ',header=None)
Train_data=np.array(Train_data)
Test_data=np.array(Test_data)
y_train = Train_data[:,0]
x_train = Train_data[:,1:]
y_test = Test_data[:,0]
x_test = Test_data[:,1:]

ada=AdaBoostClassifier(n_estimators=10, base_estimator=SVC(kernel='poly',degree = 5,probability=True))#probability=True))
ada.fit(x_train,y_train)
y_pre = ada.predict(x_test)
print("K=10,Acc:",accuracy_score(y_test,y_pre))

ada=AdaBoostClassifier(n_estimators=20, base_estimator=SVC(kernel='poly',degree = 5,probability=True))#probability=True))
ada.fit(x_train,y_train)
y_pre = ada.predict(x_test)
print("K=20,Acc:",accuracy_score(y_test,y_pre))
