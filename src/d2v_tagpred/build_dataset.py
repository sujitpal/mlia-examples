# -*- coding: utf-8 -*-
import json
import requests

OMDB_URL = "http://www.omdbapi.com/?i=tt%s&plot=full&r=json"

movie_tags = {}
ftag = open("../data/tags.csv", 'rb')
for line in ftag:
    if line.startswith("userId"):
        continue
    _, mid, tag, _ = line.strip().split(",")
    if movie_tags.has_key(mid):
        movie_tags[mid].add(tag)
    else:
        movie_tags[mid] = set([tag])
ftag.close()

fdata = open("../data/tagged_plots.csv", 'wb')
flink = open("../data/links.csv", 'rb')
for line in flink:
    if line.startswith("movieId"):
        continue
    mid, imdb_id, _ = line.strip().split(",")
    if not movie_tags.has_key(mid):
        continue
    resp = requests.get(OMDB_URL % (imdb_id))
    resp_json = json.loads(resp.text)
    plot = resp_json["Plot"].encode("ascii", "ignore")
    fdata.write("%s\t%s\t%s\n" % (mid, plot, "::".join(list(movie_tags[mid]))))
flink.close()
fdata.close()