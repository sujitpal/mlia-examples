import igraph as ig
import operator
import matplotlib.pyplot as plt

max_nodes_to_consider = 1000

known_guilty = set([7732, 49524, 8359, 12472, 60077, 
                    43961, 73597, 4872, 10973, 47362, 
                    49212, 64246])

def email_address(G, nid):
  return G.vs[nid]["label"]

def nodes(G):
  return [v.index for v in G.vs]

def compute_top_vertices(G, metric, n):
  sorted_metric = sorted(zip(nodes(G), metric), key=operator.itemgetter(1), 
    reverse=True)[0:n]
  return [x[0] for x in sorted_metric]

def plot_intersection(vs, title, G):
  xs = []
  ys = []
  match_set = set()
  for i in range(0, len(vs)):
    top_set = set(vs[0:i])
    match_set = top_set.intersection(known_guilty)
    #print "At %d, matched=%d" % (i, len(match_set))
    xs.append(i)
    ys.append(len(match_set))
  print title
  print [email_address(G, nid) for nid in match_set]
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.set_title(title)
  ax.set_xlabel("#-vertices")
  ax.set_ylabel("#-matched")
  ax.plot(xs, ys)
  plt.show()

def test_degree_centrality_hypothesis(G):
  dc = G.degree()
  top_vertices = compute_top_vertices(G, dc, max_nodes_to_consider)
  plot_intersection(top_vertices, "Degree Centrality", G)
  
def test_closeness_centrality_hypothesis(G):
  cl = G.closeness(cutoff=3)
  top_vertices = compute_top_vertices(G, cl, max_nodes_to_consider)
  plot_intersection(top_vertices, "Closeness Centrality", G)

def test_betweenness_centrality_hypothesis(G):
  bc = G.betweenness(cutoff=3)
  top_vertices = compute_top_vertices(G, bc, max_nodes_to_consider)
  plot_intersection(top_vertices, "Betweenness Centrality", G)

def test_eigenvector_centrality_hypothesis(G):
  ec = G.eigenvector_centrality()
  top_vertices = compute_top_vertices(G, ec, max_nodes_to_consider)
  plot_intersection(top_vertices, "Eigenvector Centrality", G)

def test_pagerank_hypothesis(G):
  pr = G.pagerank(directed=True, damping=0.85)
  top_vertices = compute_top_vertices(G, pr, max_nodes_to_consider)
  plot_intersection(top_vertices, "Pagerank Centrality", G)

def test_hits_authority_hypothesis(G):
  ats = G.authority_score()
  top_vertices = compute_top_vertices(G, ats, max_nodes_to_consider)
  plot_intersection(top_vertices, "HITS Authority Scores", G)

def main():
  G = ig.read("enron.gml")
  test_degree_centrality_hypothesis(G)
  test_closeness_centrality_hypothesis(G)
  test_betweenness_centrality_hypothesis(G)
  test_eigenvector_centrality_hypothesis(G)
  test_pagerank_hypothesis(G)
  test_hits_authority_hypothesis(G)

if __name__ == "__main__":
  main()
