import networkx as nx
import operator

# your GML file
filename = 'LadaFacebookAnon.gml'

# read in the graph using networkX
G = nx.read_gml(filename, relabel=True)

# for example to get the number of nodes:
num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()
ccs = nx.connected_components(G)
szLargestComp = max([len(cc) for cc in ccs])
# degree_centrality yields list of tuples ((node, fraction of nodes it is
# connected to)), so max degree is the largest fraction multiplied by
# the number of nodes.
dc = nx.degree_centrality(G)
max_degree = int(sorted(dc.iteritems(), key=operator.itemgetter(1), 
  reverse=True)[0][1] * num_nodes)
print "number of nodes: %d" % (num_nodes)
print "number of edges: %d" % (num_edges)
print "number of connected components: %d" % (len(ccs))
print "size of largest connected component: %d" % (szLargestComp)
print "maximum degree: %d" % (max_degree)
