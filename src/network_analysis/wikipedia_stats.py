import networkx as nx
import collections
import matplotlib.pyplot as plt
import numpy as np
import math
import operator

filename = "../../data/network-analysis/wikipedia.gml"

# Estimate the exponent of the power law for the degree distribution of
# the wikipedia graph. We iterate through the nodes of the graph, then
# accumulate the degree distribution, then fit a line to the log-log
# graph of the degree distribution. The power law distribution is given by:
#  ln(y) = c - alpha * ln(x)
# where y is the number of nodes at each degree
# and   x is a range of numbers from 0 to max_degree
# Estimating alpha is equivalent to fitting a straight line to the log-log
# scatterplot and calculating the (negative of) the gradient.
# REF: http://www1.cs.columbia.edu/~coms6998/Notes/lecture6p1.pdf
# ANS: [-1.8941, 9.8704]
G = nx.read_gml(filename, relabel=False)
ddist = collections.defaultdict(int)
for node in G.nodes():
  ddist[G.degree(node)] += 1
#plt.plot(ddist.keys(), ddist.values())
#plt.show()
x = [math.log(x) for x in ddist.keys()[1:]]
y = [math.log(y) for y in ddist.values()[1:]]
line = np.polyfit(x, y, deg=1)
print line
plt.scatter(x, y)
plt.plot(x, np.polyval(line, x), color="red")
plt.show()

# Find which nodes have the highest in-degree and out-degree
# The in_degree() and out_degree() methods return a map of nodeId:degree
# pairs, so max on value returns the one with the highest degree.
in_degrees = G.in_degree()
out_degrees = G.out_degree()
max_in_degree_node = max(in_degrees.iteritems(), 
  key=operator.itemgetter(1))[0]
max_out_degree_node = max(out_degrees.iteritems(), 
  key=operator.itemgetter(1))[0]
print "node with max in-degree =", G.node[max_in_degree_node]
print "node with max out-degree =", G.node[max_out_degree_node]

# Find the node with the max between-ness centrality
bcs = nx.betweenness_centrality(G)
max_bc_node = max(bcs.iteritems(), key=operator.itemgetter(1))[0]
print "node with max betweenness centrality =", G.node[max_bc_node]

# Find the node with the highest pagerank.
pageranks = nx.pagerank(G, alpha=0.85)
max_pagerank = max(pageranks.iteritems(), key=operator.itemgetter(1))[0]
print "node with highest pagerank =", G.node[max_pagerank]


