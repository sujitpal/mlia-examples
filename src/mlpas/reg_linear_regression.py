import numpy as np
import matplotlib.pyplot as plt
from scipy.io import loadmat
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error

data = loadmat("../../data/mlpas/ex5data1.mat")

# extract training data and plot
X = data["X"]
y = data["y"]
plt.scatter(X[:, 0], y, color='r')
plt.xlabel("Change in water level")
plt.ylabel("Water flowing out of dam")

# fit straight line to data
lm = LinearRegression()
lm.fit(X, y)
ypreds = [lm.predict(x)[0][0] for x in X[:, 0]]
plt.plot(X[:, 0], ypreds, color='b')
print "Linear Regression:", lm.coef_, lm.intercept_

# fit straight line with L1 regularization (lasso)
lasso_lm = Lasso()
lasso_lm.fit(X, y)
ypreds_lasso = [lasso_lm.predict(x)[0] for x in X[:, 0]]
plt.plot(X[:, 0], ypreds_lasso, color='m')
print "Lasso Regression:", lasso_lm.coef_, lasso_lm.intercept_

# fit straight line with L2 regularization (ridge)
ridge_lm = Ridge()
ridge_lm.fit(X, y)
ypreds_ridge = [ridge_lm.predict(x)[0] for x in X[:, 0]]
plt.plot(X[:, 0], ypreds_ridge, color='g')
print "Ridge Regression:", ridge_lm.coef_, ridge_lm.intercept_
plt.show()

# Plot learning curve (error vs training set size)
ms = range(1, X.shape[0] + 1)
train_errs = []
val_errs = []
Xval = data["Xval"]
yval = data["yval"]
for m in ms:
   lm = LinearRegression()
   lm.fit(X[0:m, :], y[0:m])
   ytrain_preds = [lm.predict(x)[0] for x in X[:, 0]]
   train_errs.append(mean_squared_error(y, ytrain_preds))
   yval_preds = [lm.predict(x)[0] for x in Xval[:, 0]]
   val_errs.append(mean_squared_error(yval, yval_preds))
plt.plot(ms, train_errs, color='g')
plt.plot(ms, val_errs, color='b')
plt.title("Learning curve for Linear Regression")
plt.xlabel("Number of training Examples")
plt.ylabel("Error")
plt.show()

# Polynomial fit

def convert_to_poly(X, degree):
    Xp = np.zeros((X.shape[0], degree))
    for d in range(degree):
        Xp[:, d] = X[:, 0]**(d + 1)
    return Xp

# Vary alpha (0 = no regularization, 1 = best fit, 10 = too much regularization)
X8 = convert_to_poly(X, 8)
lm_poly = Ridge(alpha=10, normalize=True)
lm_poly.fit(X8, y)
ypred_poly = [lm_poly.predict(x)[0] for x in X8]
plt.scatter(X8[:, 0], y, color='b')
xpred_poly = np.arange(int(np.min(X8[:, 0])), int(np.max(X8[:, 0])))
Xpoly = np.zeros((xpred_poly.shape[0], 1))
Xpoly[:, 0] = xpred_poly
X8poly = convert_to_poly(Xpoly, 8)
ypred_poly = [lm_poly.predict(x)[0] for x in X8poly]
plt.plot(xpred_poly, ypred_poly, 'r--')
plt.show()

# Plot learning curve to show overfitting
# Vary alpha (0 = no regularization, 1 = best fit, 10 = too much regularization)
ms = range(1, X.shape[0] + 1)
train_errs = []
val_errs = []
X8val = convert_to_poly(Xval, 8)
for m in ms:
    lm_poly = Ridge(alpha=10, normalize=True)
    lm_poly.fit(X8[0:m, :], y[0:m])
    ytrain_preds = [lm_poly.predict(x)[0] for x in X8]
    train_errs.append(mean_squared_error(y, ytrain_preds))
    yval_preds = [lm_poly.predict(x)[0] for x in X8val]
    val_errs.append(mean_squared_error(yval, yval_preds))
plt.plot(ms, train_errs, color='g')
plt.plot(ms, val_errs, color='b')
plt.title("Polynomial Regression Learning curve")
plt.xlabel("Number of training examples")
plt.ylabel("Error")
plt.show()

# Vary alpha from 0 to 10 and plot errors
alphas = [0, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1, 3, 10]
train_errs = []
val_errs = []
for alpha in alphas:
    lm_ridge = Ridge(alpha=alpha, normalize=True)
    lm_ridge.fit(X8, y)
    ytrain_preds = [lm_ridge.predict(x)[0] for x in X8]
    yval_preds = [lm_ridge.predict(x)[0] for x in X8val]
    train_errs.append(mean_squared_error(ytrain_preds, y))
    val_errs.append(mean_squared_error(yval_preds, yval))
plt.plot(alphas, train_errs, 'g')
plt.plot(alphas, val_errs, 'b')
plt.title("Select alpha using cross-validation")
plt.xlabel("Alpha")
plt.ylabel("Error")
plt.show()
