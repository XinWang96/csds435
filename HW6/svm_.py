import numpy as np
import pandas as pd
import re
import os
from sklearn.model_selection import KFold
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

if os.path.exists('DogsVsCats_train.txt') is False:

    Train = ""
    for line in open("./CSDS600_HW4_DogsVsCats/DogsVsCats/DogsVsCats/DogsVsCats.train"):
        #print(line)
        string = re.sub(' .*?:',' ', line)
        Train = Train+(string)
        #print(Train)
    f1 = open('DogsVsCats_train.txt','w')
    f1.write(Train)
    f1.close()


    Test = ""
    for line in open("./CSDS600_HW4_DogsVsCats/DogsVsCats/DogsVsCats/DogsVsCats.test"):
        #print(line)
        string = re.sub(' .*?:',' ', line)
        Test = Test+(string)
    f1 = open('DogsVsCats_test.txt','w')
    f1.write(Test)
    f1.close()

Train_data = pd.read_csv("DogsVsCats_train.txt",sep =' ',header=None)
Test_data = pd.read_csv("DogsVsCats_test.txt",sep =' ',header=None)
Train_data=np.array(Train_data)
Test_data=np.array(Test_data)
y_train = Train_data[:,0]
x_train = Train_data[:,1:]
y_test = Test_data[:,0]
x_test = Test_data[:,1:]

#
kf = KFold(n_splits=10, random_state=2,shuffle=True)

Linear = []
Poly = []
for i,(train_index, test_index) in enumerate(kf.split(x_train,y_train)):
    X_train_val = x_train[train_index]
    y_train_val = y_train[train_index]
    X_test_val = x_test[test_index]
    y_test_val = y_test[test_index]


    svm = SVC(kernel='linear')
    svm.fit(X_train_val,y_train_val)
    y_pre = svm.predict(X_test_val)
    Linear.append(accuracy_score(y_test_val, y_pre))  # 模型评估

    svm = SVC(kernel='poly',degree = 5)
    svm.fit(X_train_val,y_train_val)
    y_pre = svm.predict(X_test_val)
    Poly.append(accuracy_score(y_test_val, y_pre))

Val_acc_linear = np.mean(np.array(Linear))
Val_acc_poly = np.mean(np.array(Poly))

svm = SVC(kernel='linear')
svm.fit(x_train, y_train)
y_pre = svm.predict(x_train)
print("training,validation and test acc of linear model:")
print(accuracy_score(y_train, y_pre))
print(Val_acc_linear)
y_pre = svm.predict(x_test)
print(accuracy_score(y_test, y_pre))

svm = SVC(kernel='poly',degree = 5)
svm.fit(x_train, y_train)
y_pre = svm.predict(x_train)
print("training,validation and test acc of poly model:")
print(accuracy_score(y_train, y_pre))
print(Val_acc_poly)
y_pre = svm.predict(x_test)
print(accuracy_score(y_test, y_pre))

