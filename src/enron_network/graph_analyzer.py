import igraph as ig
import matplotlib.pyplot as plt
import operator
import pandas as pd

KNOWN_GUILTY = set([7682, 49535, 8324, 12433, 60113, 43955, 
                    47466, 4820, 10960, 47384, 49213, 64249])

def cumulative_hits(nodes, metric, n, filter_nodes):
  pairs = zip(nodes, metric)
  if filter_nodes is not None:
    pairs = [p for p in pairs if p[0] in filter_nodes]
  sorted_metric = sorted(pairs, key=operator.itemgetter(1), 
    reverse=True)[0:n]
  top_nodes = [x[0] for x in sorted_metric]
  cum_hits = []
  for i in range(0, len(top_nodes)):
    top_node_set = set(top_nodes[0:i])
    match_set = top_node_set.intersection(KNOWN_GUILTY)
    cum_hits.append(len(match_set))
  return cum_hits

def run_all_hypotheses(G, topn, filter_nodes):
  df = pd.DataFrame(index=range(0,topn))
  nodes = [v.index for v in G.vs]
  df["Degree_Centrality"] = cumulative_hits(
    nodes, G.degree(), topn, filter_nodes)
  df["Closeness_Centrality"] = cumulative_hits(
    nodes, G.closeness(cutoff=3), topn, filter_nodes)
  df["Betweenness_Centrality"] = cumulative_hits(
    nodes, G.betweenness(cutoff=3), topn, filter_nodes)
  df["Eigenvector_Centrality"] = cumulative_hits(
    nodes, G.eigenvector_centrality(), topn, filter_nodes)
  df["PageRank"] = cumulative_hits(
    nodes, G.pagerank(directed=True, damping=0.85), topn, filter_nodes)
  df["HITS_Authority"] = cumulative_hits(
    nodes, G.authority_score(), topn, filter_nodes)
  df.plot()
  plt.show()

def prune_enron_only(G):
  enron = set([v.index for v in G.vs if v["label"].endswith("@enron.com")])
  return enron

def prune_with_nonenron_collaborators_only(G):
  # find list of non enron nodes
  not_enron = set([v.index for v in G.vs 
    if not v["label"].endswith("@enron.com")])
  # find nodes with non enron collaborators
  nnecs = set()
  for v in G.vs:
    if v["label"].endswith("@enron.com"):
      nvs = set([int(nv["id"]) for nv in v.neighbors()])
      if len(nvs.intersection(not_enron)) > 0:
        nnecs.add(v.index)
  return nnecs

def main():
  G = ig.read("enron.gml")
  run_all_hypotheses(G, 1000, None)
  run_all_hypotheses(G, 1000, prune_enron_only(G))
  run_all_hypotheses(G, 1000, prune_with_nonenron_collaborators_only(G))

if __name__ == "__main__":
  main()
