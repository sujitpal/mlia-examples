# -*- coding: utf-8 -*-

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def warmup():
    """ return a (5x5) diagonal matrix """
    return np.eye(5)
    
def plot_data(x, y):
    plt.scatter(x, y, marker='x', color='red')
    pass

def compute_cost(X, y, theta):
    hx = theta.T * X
    return np.sum(np.array(hx - y) ** 2) / (2 * X.shape[1])

def gradient_descent(X, y, theta, alpha, num_iters):
    m = X.shape[1]
    costs = np.zeros(num_iters)
    for i in range(num_iters):
        hx = theta.T * X
        diff = hx - y
        for j in range(theta.shape[0]):
            theta[j] = theta[j] - (alpha / m) * np.dot(diff, X[j, :].T)
        costs[i] = compute_cost(X, y, theta)
    return theta, costs

def plot_abline(X, theta):
    xs = [np.min(X[1, :]), np.max(X[1, :])]
    ypred = [theta[0] + theta[1] * x for x in xs]
    plt.xlabel("Population")
    plt.ylabel("Profit")
    plt.plot(xs, ypred, 'b-')
    
print "Running warmup exercise..."
print warmup()

#print "Plotting data..."
data = np.loadtxt("../../data/mlpas/ex1data1.txt", delimiter=",")
m, n = data.shape    
print "R(data) = (%d,%d)" % (m, n)

plot_data(data[:, 0], data[:, 1])

print "Running Gradient Descent..."
X = np.matrix(np.vstack((np.ones(m), data[:, 0])))
y = data[:, 1]
theta = np.zeros((2, 1))  # initialize fitting parameters
# settings for gradient descent
iterations = 1500
alpha = 0.01
cost = compute_cost(X, y, theta)
print "initial cost =", cost
theta, costs = gradient_descent(X, y, theta, alpha, iterations)
print "Theta found by gradient descent:", theta.T

print "Plot a linear fit..."
plot_abline(X, theta)
plt.show()

print "Predict values for populations of 35,000 and 70,000..."
predict1 = np.matrix([1, 3.5]) * theta
print "For pop. 35,000 predicted profit = %f" % (predict1)
predict2 = np.matrix([1, 7.0]) * theta
print "For pop. 70,000 predicted profit = %f" % (predict2)

print "Visualizing J(theta[0], theta[1])..."

print "Plotting cost vs iterations"
plt.plot(range(iterations), costs)
plt.xlabel("#-iterations")
plt.ylabel("Cost")
plt.show()

print "Surface Plot of cost components vs cost"
theta_0 = np.linspace(-10, 10, 100)
theta_1 = np.linspace(-1, 4, 100)
jvals = np.zeros((len(theta_0), len(theta_1)))
for i in range(len(theta_0)):
    for j in range(len(theta_1)):
        thetas = np.array([theta_0[i], theta_1[j]])
        jvals[i, j] = compute_cost(X, y, thetas)
ax = plt.figure().gca(projection="3d")
ax.plot_surface(theta_0, theta_1, jvals.T, cmap=cm.coolwarm)
plt.xlabel("theta_0")
plt.ylabel("theta_1")
plt.show()

print "Contour Plot of components vs cost"
plt.contour(theta_0, theta_1, jvals.T, np.logspace(-2, 3, 20))
plt.xlabel("theta_0")
plt.ylabel("theta_1")
plt.plot(theta[0], theta[1], marker='x', color='r', ms=10)
plt.show()
