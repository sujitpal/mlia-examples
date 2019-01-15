from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

def plot_data(X, y):
    pos = X[y[:, 0] == 1]
    neg = X[y[:, 0] == 0]
    plt.scatter(pos[:, 0], pos[:, 1], color='g', marker='+')
    plt.scatter(neg[:, 0], neg[:, 1], color='r', marker='o')
    plt.xlabel("Exam 1 score")
    plt.ylabel("Exam 2 score")
    plt.legend(("Admitted", "Not admitted"))
    plt.show()
    
def sigmoid(z):
    return 1 / (1 + np.exp(-z))
    
def cost_function(theta, X, y):
    m, n = X.shape
    htheta = sigmoid(X * theta)
    cost = (np.sum(-np.multiply(y, np.log(htheta)) - 
        np.multiply(1 - y, np.log(1 - htheta)))) / m
    gradient = (X.T * (htheta - y)) / m
    return cost, gradient

# load data
data = np.loadtxt("../../data/mlpas/ex2data1.txt", delimiter=",")
X = data[:, 0:2]
y = data[:, 2:3]

# plot the data
print "Plotting data with + for y=1 and o for y=0"
plot_data(X, y)

# Compute cost and gradient
m, n = X.shape
X = np.hstack((np.ones((m, 1)), X))  # add intercept term
initial_theta = np.matrix(np.zeros((n + 1, 1)))
cost, grad = cost_function(initial_theta, X, y)

print "Cost at initial thetas (zeros):", cost
print "Gradient at initial thetas (zeros):\n", grad

## Run minimize to obtain optimal theta
res = optimize.minimize(cost_function, initial_theta, args=(X, y), 
                        method="BFGS", jac=True, options={"maxiter": 400})
theta = res.x
cost = res.fun

#print "Cost at theta found by minimize:", cost
print "Theta:\n", theta

# Plot decision boundary

# Predict and Accuracies
