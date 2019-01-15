from __future__ import division

import numpy as np
import matplotlib.pyplot as plt

from scipy.io import loadmat

def visualize_data(Y):
    plt.imshow(Y, aspect=0.4)
    plt.xlabel("Users")
    plt.ylabel("Movies")
    plt.show()

def average_rating(Y, R, row_num):
    return np.mean(Y[row_num, R[row_num, :]])
    
def load_movie_dict():
    movie_dict = {}
    fmov = open("../../data/mlpas/ex8_movieids.txt", 'rb')
    for line in fmov:
        movie_id, movie_name = line.strip().split("\t")
        movie_dict[int(movie_id) - 1] = movie_name
    fmov.close()
    return movie_dict
    
def print_ratings(ratings, movie_dict):
    for i in range(ratings.shape[0]):
        if ratings[i] > 0:      
            print "Rated %d for '%s'" % (ratings[i, 0], movie_dict[i])

def mean_center(R, mu):
    Rmc = R
    Rmc[Rmc == 0] = mu
    Rmc = R - mu
    return Rmc
    
# Load data
data = loadmat("../../data/mlpas/ex8_movies.mat")
Y = data["Y"]  # ratings (num_movies x num_users)
R = data["R"]  # indicator matrix, R[i,j] = 1 if movie i rated by user j
params = loadmat("../../data/mlpas/ex8_movieParams.mat")
M = params["X"]  # feature vector for movies
U = params["Theta"]  # feature vector for users
movie_dict = load_movie_dict()  # Movie dictionary (id => name)

# Compute average rating for first movie

# Populate my ratings
# We will build item-item and user-user collaborative filtering algorithms
# to predict the movie ratings for my unrated movies using this information.
R = np.zeros((Y.shape[0], 1))
for i,j in [(0, 4), (97, 2), (6, 3), (11, 5), (53, 4), (63, 5), 
           (65, 3), (68, 5), (182, 4), (225, 5), (354, 5)]:
    R[i] = j
# mean rating for me
mu = np.mean(R[R > 0])

# Visualize input data
print_ratings(R, movie_dict)
print "Mean Rating for Test User:", mu
visualize_data(Y)

Rmc = mean_center(R, mu)

#### Item-Item Collaborative Filtering
#### Formula:
####                      sum(sim(i, j) * (r(u, j) - mu(u))
#### pred(u, i) = mu(u) + -----------------------------------
####                               sum(sim(i, j))
####

# cosine similarity between items
MM = np.dot(M, M.T) / np.linalg.norm(M, ord=2)

num_preds = 0
for j in range(Rmc.shape[0]):
    if Rmc[j, 0] != 0:
        continue
    r = mu + (np.sum(np.dot(Rmc.T, MM[j, :])) / np.sum(MM[j, np.where(Rmc != 0)[0]]))
    if num_preds < 10:
        print "Predicted II rating of %3.2f for '%s'" % (r, movie_dict[j])
    num_preds += 1

# vectorized predictions
P = mu + np.divide(np.dot(Rmc.T, MM), np.sum(MM[:, np.where(Rmc != 0)[0]], axis=1))
num_preds = 0
for j in range(Rmc.shape[0]):
    if Rmc[j, 0] != 0:
        continue
    if num_preds < 10:
        print "Predicted Vectorized II rating of %3.2f for '%s'" % (P[0, j], movie_dict[j])
    num_preds += 1

# Histogram of ratings
plt.hist(P.T, bins=10)
plt.title("Item-Item Results for Test User")
plt.xlabel("Predicted Rating")
plt.ylabel("Counts")
plt.show()
    
#### User-User Collaborative Filtering
#### Formula:
####                        sum(sim(u, v) * (r(v, i) - mu(v)))
#### pred(u, i) = mu(u) + --------------------------------------
####                            sum(sim(u, v))
####

#### Since this is a new user, we can't use the Thetas. We model User similarity
#### from our user's rating R as cosine similarity between the R vector with each
#### column in the Y vector
Usim = np.divide(np.dot(Y.T, R), 
                 (np.linalg.norm(Y, axis=0, ord=2).reshape((Y.shape[1], 1)) * 
                 np.linalg.norm(R, ord=2)))
Ymc = mean_center(Y, mu)
P = mu + (np.dot(Ymc, Usim) / np.sum(Usim, axis=0)[0])
num_preds = 0
for j in range(Rmc.shape[0]):
    if Rmc[j, 0] != 0:
        continue
    if num_preds < 10:
        print "Predicted Vectorized UU rating of %3.2f for '%s'" % (P[j, 0], movie_dict[j])
    num_preds += 1

# Histogram of ratings
plt.hist(P, bins=10)
plt.title("User-User Results for Test User")
plt.xlabel("Predicted Rating")
plt.ylabel("Counts")
plt.show()
