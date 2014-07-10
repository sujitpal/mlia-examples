# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt

def feature_normalize(X):
    X_norm = X
    mu = np.mean(X, axis=0)
    sigma = np.std(X, axis=0)
    X_norm = np.multiply(X - mu, (1/sigma))
    return X_norm, mu, sigma

def compute_cost(X, y, theta):
    hx = X * np.matrix(theta)
    return (hx - y).T * (hx - y) / (2 * len(y))

def gradient_descent(X, y, theta, alpha, num_iters): 
    m = len(y)   # number of training examples
    j_history = np.zeros((num_iters))
    for i in range(num_iters):
        hx = X * np.matrix(theta)
        diff = hx - y
        theta = theta - (alpha / m) * (X.T * diff)
        j_history[i] = compute_cost(X, y, theta)
    return theta, j_history

def normal_equation(X, y):
    return np.dot(np.dot(LA.pinv(np.dot(X.T, X)), X.T), y)

print "Loading data..."
data = np.loadtxt("../../data/mlpas/ex1data2.txt", delimiter=",")
X = data[:, :-1]
y = data[:, -1:]

print "First 10 examples from dataset..."
print "X =", X[0:10, :]
print "y =", y[0:10]

print "Normalizing features..."
print "(Scale features and set them to zero mean)..."
X, mu, sigma = feature_normalize(X)
print "X =", X[0:10, :]

print "Add intercept term to X..."
X = np.hstack((np.ones((X.shape[0], 1)), X))

print "Running gradient descent..."
alpha = 0.01
num_iters = 400
theta = np.zeros((3, 1))
theta, j_history = gradient_descent(X, y, theta, alpha, num_iters)

print "Plot the convergence graph..."
plt.plot(range(len(j_history)),  j_history, 'b-', linewidth=2)
plt.xlabel("# iterations")
plt.ylabel("Cost")
plt.show()
print "Theta computed from gradient descent =", theta

print "Test different learning rates..."
alphas = [0.1, 0.03, 0.01, 0.003, 0.001]
num_iters = 50
for i in range(len(alphas)):
    theta_l = np.zeros((3, 1))
    theta_l, j_history = gradient_descent(X, y, theta_l, alphas[i], num_iters)
    plt.plot(range(len(j_history)), j_history, label="alpha=%5.3f" % (alphas[i]))
plt.xlabel("# iterations")
plt.ylabel("Cost")
plt.legend()
plt.show()

print "Estimate the price of a 1650 sqft, 3 BR house..."
Xtest = np.matrix([[1650.0, 3.0]])
Xtest = np.multiply(Xtest - mu, (1/sigma))
Xtest = np.hstack((np.ones((1,1)), Xtest))
price = Xtest * theta
print "Predicted price (using gradient descent) = $ %9.2f" % price[0,0]

print "Calculate Theta using Normal Equation..."
data = np.loadtxt("../../data/mlpas/ex1data2.txt", delimiter=",")
X = data[:, :-1]
X = np.hstack((np.ones((X.shape[0], 1)), X))
y = data[:, -1:]
theta = normal_equation(X, y)
print "Theta computed from Normal Equation =", theta
Xtest = np.matrix([[1.0, 1650.0, 3.0]])
print "Estimate the price of a 1650 sqft, 3 BR house..."
price = Xtest * theta
print "Predicted price (using normal equation) = $ %9.2f" % price[0,0]
    
