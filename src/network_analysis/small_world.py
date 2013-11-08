from __future__ import division
import networkx as nx
import numpy as np

def print_stats(G, name):
  G = G.to_undirected()
  num_nodes = G.number_of_nodes()
  num_edges = G.number_of_edges()
  # network clustering coeff is given by watts and strogatz as the 
  # average of the local clustering coeffs of all the vertices.
  cluster_coeff = np.mean(nx.clustering(G).values())
  # the graph is disconnected, so we compute average shortest path
  # as the average of the average shortest path of all its subgraphs
  shortest_paths = []
  subgraphs = nx.connected_component_subgraphs(G)
  for g in subgraphs:
    try:
      shortest_paths.append(nx.average_shortest_path_length(g))
    except ZeroDivisionError: continue
  avg_shortest_path = np.mean(shortest_paths)
  print("Graph: %s" % (name))
  print("...                 #-nodes: %d" % (num_nodes))
  print("...                 #-edges: %d" % (num_edges))
  print("...           cluster coeff: %f" % (cluster_coeff))
  print("...  #-connected components: %d" % (len(subgraphs)))
  print("...avg shortest path length: %f" % (avg_shortest_path))

# based on: e = n * (n - 1) * p / 2
def compute_edge_creation_probability(n, e):
  return 2 * e / (n * (n - 1))

# based on GDF specs: http://guess.wikispot.org/The_GUESS_.gdf_format
# this is specific to the gnutella2.gdf file (ie not general). 
def read_gdf(filename):
  G = nx.Graph()
  fin = open(filename, 'rb')
  in_what = None
  for line in fin:
    if line.startswith("nodedef>"):
      in_what = "node"
    elif line.startswith("edgedef>"):
      in_what = "edge"
    else:
      if in_what == "node":
        node = line.split(",")[0]
        G.add_node(node)
      elif in_what == "edge":
        nodes = line.split(",")[0:2]
        G.add_edge(nodes[0], nodes[1])
      else:
        continue
  fin.close()
  return G

def q1():
  lada = nx.read_gml("../../data/network-analysis/LadaFacebookAnon.gml")
  print_stats(lada, "LadaFacebookAnon")
  p = compute_edge_creation_probability(
    lada.number_of_nodes(), lada.number_of_edges())
  erg = nx.erdos_renyi_graph(lada.number_of_nodes(), p)
  print_stats(erg, "Erdos-Renyi Random")

def q2():
  gnutella = read_gdf("../../data/network-analysis/gnutella2.gdf")
  print_stats(gnutella, "Gnutella")
  p = compute_edge_creation_probability(
    gnutella.number_of_nodes(), gnutella.number_of_edges())
  erg = nx.erdos_renyi_graph(gnutella.number_of_nodes(), p)
  print_stats(erg, "Erdos-Renyi Random")

def q3():
  lada = nx.read_gml("../../data/network-analysis/LadaFacebookAnon.gml")
  # lada's FB graph doesn't contain her name, but since we know its
  # "her" graph, this would be a node that is connected to every node
  # in the graph, so we add one of these, then calculate the clustering
  # coefficient for that node.
  lada.add_node("lada")
  for node in lada.nodes():
    lada.add_edge(node, "lada")
  print("Lada's clustering coeff: %f" % (nx.clustering(lada)["lada"]))

def main():
  q1()
  q2()
  q3()

if __name__ == "__main__":
  main()
