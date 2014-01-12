mlia-examples
=============

Python and R code to do miscellaneous Data Mining tasks. Python code started with the Machine Learning in Action book by Peter Harrington, and since then have moved to using scikit-learn.

src/book/
==========

Examples from Peter Harrington's Machine Learning in Action (MLIA).

The code is __not__ a direct copy of whats in the book or in the github site, but does the same thing. I have tried to make the code shorter and (at least to me) more understandable.

Data files are not copied over. You will find the data files (of the same name as in the code) in the [book's source code site on GitHub](https://github.com/pbharrin/machinelearninginaction).

src/event\_reco/
================
My solution for the Kaggle Event Recommendation Challenge. Given a training set of users who are interested/not\_interested in events, and user and event metadata and some social (user's friends information) metadata, the objective is to order the events in the test set per user, so events with higher probability are recommended first. The approach I have taken is to construct a set of different kinds of recommenders, and construct features from the recommender scores, then build a predictive model (SGD) to predict the value of interested. The distance from the separating hyperplane is the measure of the likelihood of recommendation.

src/salary\_pred/
=================
A solution to the Adzuna Salary Prediction Challenge on Kaggle. Given a set of job ads, predict the salary for the job. The solution is incomplete and predicts very poorly. Uses NLTK and Scikit-Learn.

src/bird\_strikes
=================
A set of visualizations using R. The data was provided as part of a programming assignment using Tableau in the Coursera Introduction to Data Science course. I wanted to see if I could produce something equivalent using R.

src/network\_analysis
====================
Partial/In-progress solutions to Coursera's Social Network Analysis course that I took late 2013. My approach was to solve as many questions as I could without depending on visualization tools such as Gephi or Netlogo (and sometimes my solutions are incorrect) and relying on NetworkX and IGraph.

src/enron\_network
==================
Code for my Peer Programming Assignment for the Social Network Analysis course on Coursera. I build a graph of people based on the from and to email addresses in the dataset, and investigate various centrality measures and other indicators of node importance (PageRank and HITS Authority) to see how effective they are at finding the guilty (tested against a list of 12 individuals who were found guilty).

src/recsys\_eval
================
Pandas code to answer questions about a evaluation run for multiple recommenders across multiple user neighborhood sizes.

src/yelp\_ufc
==============
Scikit-Learn code to build and evaluate 3 Naive Bayes classifers to predict if a review is useful, funny or cool. Uses data from the Yelp challenge on Kaggle that requires solutions to also predict number of votes that a review will receive in each category. I wanted to figure out if Sentiment Analysis could be treated as a classification problem (rather than use polarity keywords).

