import networkx as nx
import collections

TUPLE_FILE = "from_to.txt"

def to_ascii(s):
  return unicode(s, "ascii", "ignore")

# collect all nodes from tuples
vertices = set()
fin = open(TUPLE_FILE, 'rb')
for line in fin:
  from_email, to_email = line.strip().split("\t")
  vertices.add(to_ascii(from_email))
  vertices.add(to_ascii(to_email))
fin.close()
print "#-vertices:", len(vertices)

# collect all edges as vertex index tuples
vertex_idx = {x[1] : x[0] for x in enumerate(vertices)}
edges = collections.defaultdict(int)
fin = open(TUPLE_FILE, 'rb')
for line in fin:
  from_email, to_email = line.strip().split("\t")
  edge = (vertex_idx[to_ascii(from_email)], vertex_idx[to_ascii(to_email)])
  edges[edge] += 1
fin.close()
print "#-edges:", len(edges)

# build graph and write as GML file
G = nx.DiGraph()
for vertex in vertices:
  G.add_node(vertex_idx[vertex], label=vertex)
for edge in edges.keys():
  G.add_edge(edge[0], edge[1], weight=edges[edge])
nx.write_gml(G, "enron.gml")

# generate list of test node ids
known_guilty = ["kenneth.lay@enron.com", "jeff.skilling@enron.com",
    "andrew.fastow@enron.com", "richard.causey@enron.com",
    "michael.kopper@enron.com", "smiley@flash.net", "ben.glisan@enron.com",
    "greg.whalley@enron.com", "mark.koenig@enron.com", "lou.pai@enron.com",
    "ken.rice@enron.com", "rebecca.mark@enron.com"]
known_guilty_vertices = [vertex_idx[to_ascii(x)] for x in known_guilty]
print known_guilty_vertices

  
