import taufactor as tau
import tifffile
import numpy as np
import matplotlib.pyplot as plt
 
 
#Creating the training set
x = np.array([3,5,6])
y = np.array([2,3,4])
#ploting the training set on a scatter graph
plt.plot(x,y, '.', markersize=10)
plt.xlim([0,7])
plt.ylim([0,6])
plt.grid()

#defining a get prediction function (y = xw)
def getpred(w, x):
    X = np.c_[x, np.ones_like(x)]
    return X@w

#initialising the weights
w = [-1, 4]

#creating a test set
xtest = np.linspace(0, 7, 100)
ytest = getpred(w, xtest)
plt.plot(xtest, ytest, '-')

#defining a cost function (xw - y)^2
def costfunc(w, xtest, ytest):
    return np.sum((getpred(w, xtest) - ytest)**2)
#defining the gradient of the test function (-2xTy + 2xTxw)
def costfuncgrad(w, x, y):
    X = np.c_[x, np.ones_like(x)]
    return -2*X.T@y + 2*X.T@X@w
#defining the learning rate to be multiplied with the gradient
lr = 0.01
# a for loop acting as a gradient descent function to update the weights based on the gradient of the cost function and the learning rate
for i in range(10000):
    grad = costfuncgrad(w, x, y)
    w = w - grad * lr

#ploting the new predicted data with the new weights
ytest = getpred(w, xtest)
plt.plot(xtest, ytest, '-')
plt.show()