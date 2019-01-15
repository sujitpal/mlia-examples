import igraph as ig
import matplotlib.pyplot as plt
import collections
import operator

known_guilty = set([7682, 49535, 8324, 12433, 60113, 43955,
                    47466, 4820, 10960, 47384, 49213, 64249])

def plot_degree_distrib(G):
  dcutoff = 100
  fd = collections.defaultdict(int)
  for d in G.degree():
    if d < dcutoff: continue
    fd[d] += 1
  xvals = [x[0] for x in fd.items()]
  yvals = [x[1] for x in fd.items()]
  plt.title("Degree Distribution (degree > %d)" % (dcutoff))
  plt.xlabel("Degree")
  plt.ylabel("Count")
  plt.plot(xvals, yvals, color="red")
  plt.show()

def partition(lst, n):
  q, r = divmod(len(lst), n)
  indices = [q*i + min(i, r) for i in xrange(n+1)]
  partitions = [lst[indices[i]:indices[i+1]] for i in xrange(n)]
  return [(min(x), max(x)) for x in partitions]

def vertex_size(s, ps):
  for idx, (rmin, rmax) in enumerate(ps):
    if s >= rmin and s <= rmax:
      return (idx + 1) * 5
  return 5

def plot_pruned_graph(G, dcutoff):
  # docs: http://python-igraph.readthedocs.org/en/latest/tutorial.html
  # only keep the top 1000 degree centrality vertices
  degs = G.degree()
  partitions = partition(degs, 10)
  delete_verts = [x[0] for x in 
    sorted(zip(G.vs, degs), key=operator.itemgetter(1), 
    reverse=True)[100:]]
  G.delete_vertices(delete_verts)
  for v in G.vs:
    if int(v["id"]) in known_guilty:
      v["color"] = "#FF0000"
    else:
      v["color"] = "#0000FF"
    v["size"] = vertex_size(G.degree(v), partitions)
    try:
      del v["label"]
    except KeyError: pass
  #ig.write(G, "enron_pruned.gml")
  layout = G.layout("kk")
  ig.plot(G, layout=layout, target="enron_viz.png")
  
def main():
  G = ig.read("enron.gml")
  #plot_degree_distrib(G)
  plot_pruned_graph(G, 250)

if __name__ == "__main__":
  main()
