from __future__ import division
import collections
import community
import igraph as ig
import networkx as nx

## For the middle eastern recipe ingredients graph, find the ingredient
## that is in the same community as vanilla.
def q1():
  G = nx.read_gexf("../../data/network_analysis/MiddleEasternHW4.gexf")
  partition = community.best_partition(G.to_undirected())
  # partition is a map of node_id => partition_id. From gexf file, vanilla
  # is nodeID v41 which is partition 2. So we find all the others nodes in
  # the same partition and list their labels 
  vanilla_part_nodes = [x[0] for x in partition.iteritems() if x[1] == 2]
  print "[1] ingredient in same community as vanilla"
  for node in vanilla_part_nodes:
    if node == "v41": continue
    print "...", G.node[node]["label"]

## compute modularity of two different graphs and compare them
def q2():
  print "[2] compare modularity values"
  cuisines = ["SoutheastAsian", "NorthAmerican"]
  for cuisine in cuisines:
    G = nx.read_gexf("../../data/network-analysis/%sHW4.gexf" % (cuisine))
    H = G.to_undirected(reciprocal=False)
    part = community.best_partition(H)
    mod = community.modularity(part, H)
    print "...", cuisine, "modularity =", mod

## compare modularity of combined recipe graph with and without edge
## thresholding
def q3():
  print "[4] compare community stats before and after edge thresholding"
  G = nx.read_gexf("../../data/network-analysis/complements.gexf")
  H = G.to_undirected()
  part_before = community.best_partition(H)
  num_comm_before = len(set([x[1] for x in part_before.iteritems()]))
  mod_before = community.modularity(part_before, H)
  print("before thresholding, #-communities=%d, modularity=%f" % 
    (num_comm_before, mod_before))
  edges_before = H.edges(data=True)
  for edge in edges_before:
    weight = edge[2]["weight"]
    if weight < 0.2: 
      H.remove_edge(edge[0], edge[1])
  part_after = community.best_partition(H)
  num_comm_after = len(set([x[1] for x in part_after.iteritems()]))
  mod_after = community.modularity(part_after, H)
  print("after thresholding, #-communities=%d, modularity=%f" % 
    (num_comm_after, mod_after))

## Find best german translation for english word coil (e_coil).
## From the data, e_coil is node id 2, so we list all labels that
## start with g_ (for german) that are in the same partition.
def q5():
  print "[5] german translation of english word coil (e_coil)"
  G = nx.read_gexf("../../data/network-analysis/words.gexf")
  H = G.to_undirected()
  part = community.best_partition(H)
  part_id = part["2"]
  nodes_in_part = [x[0] for x in part.iteritems() 
                        if x[0] != "2" and x[1] == part_id]
  for node in nodes_in_part:
    label = G.node[node]["label"]
    if label.startswith("g_"): print "...", label

# wikipedia network analysis
def opa3():
  # [1] size of largest clique in wikipedia network (27/5/13/22)
  # [2] largest k-core any vertex in network belongs to (46/8/3/21)
  # [3] fast greedy community finding algo. Find percentage of graph
  #     covered by the 4 largest communities (20/50/10/70)
  # [4] infomap community finding algo, compare with fast greedy
  # [5] compare modularity between 2 algos.
  G = ig.read("../../data/network-analysis/wikipedia.gml")
  G.to_undirected()
  cliques = G.maximal_cliques()
  largest_clique = max([len(x) for x in cliques])
  print "[OPA3:1] size of largest clique =", largest_clique
  largest_kcores = []
  for clique in cliques:
    S = G.induced_subgraph(clique)
    largest_kcores.append(max(S.degree()))
  largest_kcore = max(largest_kcores)
  print "[OPA3:2] size of largest K-core =", largest_kcore
  comm_fg = G.community_fastgreedy()
  num_nodes = G.vcount()
  num_nodes_subgraphs = []
  subgraphs_fg = comm_fg.as_clustering().subgraphs():
  for S in subgraphs_fg:
    num_nodes_subgraphs.append(len(S.vcount()))
  pc_coverage = \
    sum(sorted(num_nodes_subgraphs, reverse=True)[0:4]) * 100 / G.vcount()
  print "[OPA3:3] percent coverage by 4 largest communities =", pc_coverage
  print "[OPA3:4] # communities via FG =", len(subgraphs_fg)
  print "[OPA3:4] average nodes via FG =", \
    sum(num_nodes_subgraphs) / len(subgraphs_fg)
  comm_im = G.community_infomap()
  subgraphs_im = comm_im.subgraphs()
  print "[OPA3:4] # communities via IM =", len(subgraphs_im)
  num_nodes_subgraphs = []
  for S in subgraphs_im:
    num_nodes_subgraphs.append(len(S.vcount()))
  print "[OPA3:4] average nodes via IM =", \
    sum(num_nodes_subgraphs) / len(subgraphs_im)
  mod_fg = G.modularity(comm_fg.as_clustering())
  print "[OPA3:5] modularity (FG) =", mod_fg
  mod_im = G.modularity(comm_im)
  print "[OPA3:5] modularity (IM) =", mod_im

def main():
  q1()
  q2()
  q3()
  q5()
  opa3()

if __name__ == "__main__":
  main()
