import numpy as np


def sigmoid(x):
    if (x > 0).all():
        return 1.0 / (1.0 + np.exp(-x))
    else:
        return np.exp(x) / (1.0 + np.exp(x))

train_set_x = np.array([[0.6, 0.1], [0.2, 0.3]])
Y =  np.array([[1, 0], [0, 1]])


# 样本数量
nTrain = train_set_x.shape[1]
n_x = train_set_x.shape[0]

Iterations = 1  # iteration numbers
alpha = 0.1  # learnning rate
Layers = [2, 3, 2]  # nn units of hidden layer and output layer
nL = len(Layers) - 1  # nn层数

W = [[] for i in range(len(Layers))]
b = [[] for i in range(len(Layers))]

W[1] = np.array([[0.1,-0.2], [0, 0.3], [ 0.2, -0.4]])
W[2] =np.array([[-0.4, 0.1, 0.6], [0.2, -0.1, -0.2]])
b[1] = np.array([[0.1], [0.2], [0.5]])
b[2] =  np.array([[-0.1], [0.6]])

dW = W.copy()
db = b.copy()
Z = []
A = []
for i in range(len(Layers)):
    A.append(np.zeros((Layers[i], nTrain)))
    Z.append(np.zeros((Layers[i], nTrain)))
A[0] = train_set_x
dZ = Z.copy()
dA = A.copy()
cost = []

for i in range(Iterations):
    # forward propagation
    for l in np.arange(nL) + 1:
        Z[l] = np.dot(W[l], A[l - 1]) + b[l]  # 线性输出
        if l==nL:
            A[l] = sigmoid(Z[l])       #输出层激活函数使用sigmoid  输出为0-1
        else:                          #隐层激活函数使用relu
            A[l] = sigmoid(Z[l])
    dZ[nL] = (A[nL] - Y) / nTrain  # 输出层dZ计算
    for l in nL - np.arange(nL):  # 隐层梯度计算
        dW[l] = np.dot(dZ[l], A[l - 1].T)
        db[l] = np.sum(dZ[l], axis=1, keepdims=True)
        if l > 1:
            dA[l - 1] = np.dot(W[l].T, dZ[l])  # 计算前一层的dA、dZ
            dZ[l - 1] = dA[l - 1].copy()
            dZ[l - 1][Z[l - 1] < 0] = 0
    for l in range(1, nL + 1):
        W[l] = W[l] - alpha * dW[l]  # 更新参数
        b[l] = b[l] - alpha * db[l]
    print(W)
    print(b)













