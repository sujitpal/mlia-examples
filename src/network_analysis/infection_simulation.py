from __future__ import division
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

INFECT_RATE = 0.15
RECOVER_RATE = 0.40
NUM_NODES = 200
AVG_DEGREE = 3.8
TIME_UNITS = 20000

# create a basic Erdos-Renyi graph with 200 nodes and 0.5 probability
# to simulate a default population.
#G = nx.erdos_renyi_graph(NUM_NODES, (AVG_DEGREE / (NUM_NODES - 1)))
#print "# nodes=", G.number_of_nodes(), ", # edges=", G.number_of_edges()

# generate Erdos-Renyi graph. Networkx provides a method for creating
# an Erdos-Renyi graph given the number of nodes and the probability
# of edge creation, but we try to use the approach in the assignment
# Netlogo program template where we calculate the number of links and 
# assign edges to an empty graph.
G = nx.Graph()
nodes = np.arange(0, NUM_NODES)
for node in nodes:
  G.add_node(node)
tot_edges = int(NUM_NODES * AVG_DEGREE / 2) + 1
num_edges = 0
while num_edges < tot_edges:
  n1 = int(random.uniform(0, NUM_NODES))
  n2 = int(random.uniform(0, NUM_NODES))
  if n1 == n2: continue
  G.add_edge(n1, n2)
  num_edges = G.number_of_edges()
print "graph created:(%d,%d)" % (G.number_of_nodes(), G.number_of_edges())

# initially everyone is well, we set infected to 0, then infect a 
# random person
infected = np.zeros(NUM_NODES)
infected[int(random.uniform(0, NUM_NODES))] = 1

# At each time unit, for each node, we check if its infected. If it is we
# infect its neighbors with p(INFECT_RATE). At the end, we un-infect the
# original node with p(RECOVER_RATE). At each stage we print the time 
# unit and the number infected in the population.
num_infected = np.zeros(TIME_UNITS)
for t in range(0, TIME_UNITS):
  for n in G.nodes():
    if infected[n] == 1:
      neighbors = G[n]
      if len(neighbors) > 0:
        for nn in neighbors.keys():
          if random.uniform(0, 1) <= INFECT_RATE:
            infected[nn] = 1
      if random.uniform(0, 1) <= RECOVER_RATE:
        infected[n] = 0
  num_infected[t] = len(infected[infected == 1])
  print "at time %d, #-infected=%d" % (t, num_infected[t])
print "average #-people infected=", np.mean(num_infected)
plt.plot(num_infected)
plt.show()


