from __future__ import division
import networkx as nx
import igraph as ig
import operator
import numpy as np
import re

# Q2: Continuing with the diseasome network, which of the following genes
# has highest degree centrality?
# (x) TP53 id=350
# ( ) BARD1 id=1040
# ( ) LEPR id=1386
# ( ) FOXE3 id=743
def q2():
  #G_in = nx.read_gexf("../../data/network-analysis/diseasome.gexf")
  #nx.write_gml(G)
  # The supplied file is malformed, had many problems converting gexf
  # into gml. nx.read_gml() doesn't read the label, we do this manually
  G = nx.read_gml("../../data/network-analysis/diseasome.gml")
  dcs = nx.centrality.degree_centrality(G)
  dcs_ourgenes = sorted([x for x in dcs.iteritems() 
                         if x[0] in set([350,1040,1386,743])], 
                         key=operator.itemgetter(1), reverse=True)
  print dcs_ourgenes

def build_id_sex_map(gml_file):
  id_pattern = re.compile(r"id\s(\d?)")
  sex_pattern = re.compile(r"sex\s\"(\w+)\"")
  id_sex_map = {}
  f = open(gml_file, 'rb')
  for line in f:
    line = line.strip()
    if line.startswith("id"):
      dolphin_id = int(re.sub(id_pattern, "\\1", line))
    elif line.startswith("sex"):
      dolphin_sex = re.sub(sex_pattern, "\\1", line)
      id_sex_map[dolphin_id] = dolphin_sex
      dolphin_id = None
      dolphin_sex = None
  f.close()
  return id_sex_map

def count_sex_interactions(G, id_sex_map):
  same_sex = 0
  opp_sex = 0
  for edge in G.edges():
    n1_sex = id_sex_map[edge[0]]
    n2_sex = id_sex_map[edge[1]]
    if n1_sex == n2_sex:
      same_sex += 1
    else:
      opp_sex += 1
  return (same_sex, opp_sex)

# Q3: Check all that apply
# [ ] the clustering coefficient is no higher than it would be for an 
#     equivalent Erdos Renyi random graph.
# [x] the average degree is higher than it would be in an ER random 
#     graph with the same number of nodes and edges
# [ ] the network is assortative on sex: same sex interactions occur 
#     more often than they would if the network were rewired at random
def q3():
  G_dolphins = nx.read_gml("../../data/network-analysis/dolphins.gml")
  num_nodes = G_dolphins.number_of_nodes()
  num_edges = G_dolphins.number_of_edges()
  # option 1
  cc_dolphins = np.mean(nx.clustering(G_dolphins).values())
  ecp = (2 * num_edges) / (num_nodes * (num_nodes - 1))
  dolphins = 0
  ergs = 0
  for i in range(0, 11):
    G_erg = nx.erdos_renyi_graph(num_nodes, ecp)
    cc_erg = np.mean(nx.clustering(G_erg).values())
    if cc_dolphins > cc_erg:
      dolphins += 1
    else:
      ergs += 1
  print("Clustering Coeff (dolphins = %d, erdos-renyi = %d)" % (dolphins, ergs))
  # option 2
  dolphins = 0
  ergs = 0
  deg_dolphins = np.mean(nx.degree(G_dolphins).values())
  for i in range(0, 11):
    G_erg = nx.erdos_renyi_graph(num_nodes, ecp)
    deg_erg = np.mean(nx.clustering(G_erg).values())
    if deg_dolphins > deg_erg:
      dolphins += 1
    else:
      ergs += 1
  print("Average Degree (dolphins = %d, erdos-renyi = %d)" % (dolphins, ergs))
  # option 3
  # NetworkX refuses to extract additional properties from gml files 
  # with read_gml, so we must do it ourselves. We manually parse
  # (TODO: learn pyparsing) the dolphins.gml file to generate a mapping
  # of {node.id => node.sex}.
  dolphins = 0
  ergs = 0
  id_sex = build_id_sex_map("../../data/network-analysis/dolphins.gml")
  si_dolphins = count_sex_interactions(G_dolphins, id_sex)
  for i in range(0, 11):
    G_erg = nx.erdos_renyi_graph(num_nodes, ecp)
    si_erg = count_sex_interactions(G_erg, id_sex)
    if si_dolphins[0] > si_erg[0]:
      dolphins += 1
    else:
      ergs += 1
  print("Same sex interactions (dolphins = %d, erdos-renyi = %d)" % 
    (dolphins, ergs))

# Q4: The dolphins were followed for a period of years. At one point, one 
# individual disappeared and the dolphins split up into two separate groups. 
# When the individual reappeared, they again formed one social network. 
# Coincidentally this individual has highest betweenness in the network. 
# Who is it?
# ( ) Zig
# ( ) Quasi
# (x) SN100
# ( ) Vau
def q4():
  G = ig.read("../../data/network-analysis/dolphins.gml")
  nodes = [int(v["id"]) for v in G.vs]
  bcs = G.betweenness()
  it = sorted(zip(nodes, bcs), key=operator.itemgetter(1), reverse=True)[0][0]
  print "Dolphin with highest betweenness =", G.vs[it]["label"]

def read_gdf(gdf_file):
  G = nx.Graph()
  f = open(gdf_file, 'rb')
  in_nodedef = False
  colnames = []
  for line in f:
    line = line.strip()
    if line.startswith("nodedef>"):
      line = line.replace("nodedef>", "")
      line = line.replace(" ", "")
      line = re.sub(r"[A-Z]+", "", line) # remove UPPERCASE col types
      colnames = line.split(",")
      in_nodedef = True
    elif line.startswith("edgedef>"):
      line = line.replace("edgedef>", "")
      line = line.replace(" ", "")
      line = re.sub(r"[A-Z]+", "", line) # remove UPPERCASE col types
      colnames = line.split(",")
      in_nodedef = False
    else: 
      colvals = line.split(",")
      if in_nodedef:
        node_attrs = {}
        for i in range(1, len(colvals)):
          if colvals[i].replace(",", "").isdigit():
            if colvals[i].find(".") > -1:
              node_attrs[colnames[i]] = float(colvals[i])
            else:
              node_attrs[colnames[i]] = int(colvals[i])
          else:
            if colvals[i].find("\"") > -1:
              node_attrs[colnames[i]] = colvals[i].replace("\"", "")
            else:
              node_attrs[colnames[i]] = colvals[i]
        G.add_node(colvals[0], attr_dict=node_attrs)
      else:
        edge_attrs = {}
        src_node = colvals[0]
        target_node = colvals[1]
        for i in range(2, len(colvals)):
          if colvals[i].replace(",", "").isdigit():
            if colvals[i].find(".") > -1:
              edge_attrs[colnames[i]] = float(colvals[i])
            else:
              edge_attrs[colnames[i]] = int(colvals[i])
          else:
            if colvals[i].find("\"") > -1:
              edge_attrs[colnames[i]] = colvals[i].replace("\"", "")
            else:
              edge_attrs[colnames[i]] = colvals[i]
        G.add_edge(src_node, target_node, attr_dict = edge_attrs)
  f.close()
  print G.nodes()
  print G.edges()
  return G

# Q7: Load the network of Middle Eastern ingredients. Calculate betweenness 
# for all nodes. A high betweenness ingredient in Middle Eastern cuisine is
# (x) coriander
# ( ) garlic
# ( ) walnut
# ( ) dill
def q7():
  G = read_gdf("../../data/network-analysis/MiddleEastern.gdf")
  nx.write_gml(G, "/tmp/MiddleEastern.gml")
  G = ig.read("/tmp/MiddleEastern.gml")
  bcs = G.betweenness()
  labels = [v["label"] for v in G.vs()]
  label_bcs = sorted(zip(labels, bcs), key=operator.itemgetter(1), reverse=True)
  ingredient_set = set(["coriander", "garlic", "walnut", "dill"])
  print [x for x in label_bcs if x[0] in ingredient_set]

def main():
  #q1()
  #q2()
  #q3()
  #q4()
  q7()

if __name__ == "__main__":
  main()
