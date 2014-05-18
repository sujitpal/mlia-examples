fin = open("../../data/network_analysis/wikipedia.gml", 'rb')
fout = open("../../data/network_analysis/wikipedia-compact.gml", 'wb')
for line in fin:
  sline = line.strip()
  if sline.startswith("wikiid") or sline.startswith("label"):
    continue
  fout.write(line)
fout.close()
fin.close()
