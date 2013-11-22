import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

# Objective was to find if a diffusion process is faster or slower 
# in a lattice network with and without shortcuts. The simulation 
# here leads to a conclusion opposite of the netlogo visualization.
def q1():
  # given in question
  infection_rate = 0.25
  recovery_rate = 0.30
  # from NetLogo model file (may be incorrect!)
  num_nodes = 200
  num_neighbors = 4
  xvals = range(0, 20000)
  for p_rewire in [0.0, 1.0]:
    G = nx.watts_strogatz_graph(num_nodes, num_neighbors, p_rewire)
    infected = np.zeros(num_nodes, dtype=int)
    # randomly infect one of the nodes
    random_node = random.uniform(0, num_nodes)
    infected[random_node] = 1
    yvals = []
    for xval in xvals:
      for node in range(0, num_nodes):
        if infected[node] == 1:
          if random.uniform(0, 1) <= recovery_rate:
            infected[node] = 0
            continue
          if random.uniform(0, 1) <= infection_rate:
            neighbors = G[node].keys()
            for neighbor in neighbors:
              infected[neighbor] = 1
      num_infected = len(infected[infected == 1])
      print("For p=%f, timeunit=%d, #-infected=%d" % 
        (p_rewire, xval, num_infected))
      yvals.append(num_infected)
    plt.plot(xvals, yvals, color='b' if p_rewire == 0 else 'r')
  plt.show()

# Objective is to compare speed of solving graph coloring problem
# ie adjacent nodes have different colors between a small world
# network topology (ie watts_strogatz) and a preferential attachment
# topology (ie barabasi_albert).
# Ref: GraphColoring.nlogo
def q2():
  pass

# Opinion propagation (using rules of triadic closures) using payoffs
# a = payoff for playing blue, b = payoff for playing red and c = cost
# of being bilingual.
# q3: a=3 b=2 c=4 bilingual=off init-prob-blue=83
# allocate opinion at random, then calculate change over time
def q3and4():
  pass

# Compare a random graph vs preferential attachment graph to track the
# diffusion of an idea across a network, measuring max final fitness
# and time to converge to a solution.
# n_nodes = 200, k=5, nn=24, iters=4000, each node takes input from k nodes plus
# itself. Each node has a fitness table, listing contribution it makes to
# fitness given current states of all its inputs. tables of fitness 
# contributions are populated from a uniform distribution in [0,1].
# Given a combination of all N node states, N contributions can be
# averaged to compute single fitness value.
def q5():
  pass

def main():
#  q1()
#  q2()
  q3and4()
  q5()

if __name__ == "__main__":
  main()
