# -*- coding: utf-8 -*-
import json
import re
import md5
import os
import urllib

DATA_DIR = "/home/sujit/Projects/mlia-examples/data/mtcrawler"
JSON_FILE = "mtsamples.json"

p = re.compile(r"\d+-(.*)")

def remove_leading_number(s):
    m = re.search(p, s)
    if m is None:
        return s
    else:
        return m.group(1)

def normalize(s):
    return urllib.quote_plus(s)
    
def get_md5(s):
    m = md5.new()
    m.update(s)
    return m.hexdigest()

md5_url_map = dict()
fin = open(os.path.join(DATA_DIR, JSON_FILE), 'rb')
jobj = json.load(fin)
fin.close()
print "#-records:", len(jobj[0])
unique_recs = set()
rawhtml_dir = os.path.join(DATA_DIR, "raw_htmls")
os.makedirs(rawhtml_dir)
for rec in jobj[0]:
    type_name = remove_leading_number(normalize(rec["type_name"]))
    sample_name = remove_leading_number(normalize(rec["sample_name"]))
    body = rec["body"].encode("utf-8")
    md5_body = get_md5(body)
    if not md5_url_map.has_key(md5_body):
        # record md5 to link (first link only) for multiple docs
        md5_url_map[md5_body] = rec["link"]
    print "%s/%s.html" % (type_name, sample_name)
    unique_recs.add(md5_body)
    dir_name = os.path.join(rawhtml_dir, type_name)
    try:    
        os.makedirs(dir_name)
    except OSError:
        # directory already made just use it
        pass
    fout = open(os.path.join(dir_name, sample_name) + ".html", 'wb')
    fout.write(body)
    fout.close()
# write out md5 to URL value, will be used to put the link back into the final
# JSON files
furls = open(os.path.join(DATA_DIR, "urls.csv"), 'wb')
for key, value in md5_url_map.items():
    furls.write("%s\t%s\n" % (key, value))
furls.close()

print "# unique records:", len(unique_recs)
