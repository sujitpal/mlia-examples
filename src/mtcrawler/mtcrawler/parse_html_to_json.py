# -*- coding: utf-8 -*-
import re
import os
import urllib
import json
import md5
from scrapy.selector import Selector

DATA_DIR = "/home/sujit/Projects/mlia-examples/data/mtcrawler"
DISCLAIMER_TEXT = "anything else to real world is purely incidental"

blob_pattern = re.compile(r"<b[.*?>]*>[A-Z0-9:() ]+</b>")

def load_url_map():
    url_map = dict()
    fin = open(os.path.join(DATA_DIR, "urls.csv"), 'rb')
    for line in fin:
        key, value = line.strip().split("\t")
        url_map[key] = value
    fin.close()
    return url_map
    
def normalize(s):
    return urllib.unquote_plus(s)

def get_candidate_blob(line, sel):
    line = line.strip()
    # check for the obvious (in this case) <b>HEADING:</b> pattern
    m = re.search(blob_pattern, line)
    if m is not None:
        # return the matched block
        return line
    # some of the blobs are enclosed in a multi-line div block
    div_text = None
    for div in sel.xpath("//div[@style]"):
        style = div.xpath("@style").extract()[0]
        if "text-align" in style:
            div_text = div.xpath("text()").extract()[0]
            div_text = div_text.replace("\n", " ")
            div_text = re.sub(r"\s+", " ", div_text).strip()
            break
    if div_text is not None and DISCLAIMER_TEXT not in div_text:
        return div_text
    # finally drop down to just returning a long line (> 1000 chars)
    # This can probably be more sophisticated by checking for the 
    # density of the line instead
    if len(line) > 700 and DISCLAIMER_TEXT not in line:
        return line
    return None
    
def to_plain_text(text):
    if text is None:
        return text
    # convert br tags to newline
    text = re.sub("<[/]*br[/]*>", "\n", text)
    # remove html tags
    text = re.sub("<.*?[^>]>", "", text)
    return text

def md5_hash(s):
    m = md5.new()
    m.update(s)
    return m.hexdigest()

def add_json(json_obj, json_fid):
    print "Add JSON for: %s :: %s" % (json_obj["category"], json_obj["sample"])
    json_fname = "%04d.json" % (json_fid)
    fout = open(os.path.join(json_dir, json_fname), 'wb')        
    json.dump(json_obj, fout)
    fout.close()

def merge_lists(list1, list2):
    merged_set = set(list1).union(set(list2))
    return list(merged_set)
    
def update_json(json_obj, json_fid):
    print "Update JSON %s.json for: %s :: %s" % (json_fid, json_obj["category"], 
                                                 json_obj["sample"])
    json_fname = "%04d.json" % (json_fid)
    fin = open(os.path.join(json_dir, json_fname), 'rb')
    orig_json_obj = json.load(fin)
    fin.close()
    cats = merge_lists(orig_json_obj["category"], json_obj["category"])
    orig_json_obj["category"] = cats
    keywords = merge_lists(orig_json_obj["keywords"], json_obj["keywords"])
    orig_json_obj["keywords"] = keywords
    fout = open(os.path.join(json_dir, json_fname), 'wb')
    json.dump(orig_json_obj, fout)
    fout.close()


url_map = load_url_map()
rawhtml_dir = os.path.join(DATA_DIR, "raw_htmls")
json_dir = os.path.join(DATA_DIR, "jsons")
os.makedirs(json_dir)
json_fid = 0
doc_digests = dict()
for root, dirnames, filenames in os.walk(rawhtml_dir):
    for filename in filenames:
        in_path = os.path.join(root, filename)
        fin = open(in_path, 'rb')
        text = fin.read()        
        fin.close()
        json_obj = {}
        # extract URL from map
        json_obj["url"] = url_map[md5_hash(text)]
        # extract metadata from directory structure
        json_obj["sample"] = normalize(in_path.split("/")[-1].replace(".html", ""))
        json_obj["category"] = [normalize(in_path.split("/")[-2])]
        # extract metadata from specific tags in HTML
        sel = Selector(text=text, type="html")
        json_obj["title"] = sel.xpath("//title/text()").extract()[0]
        json_obj["keywords"] = [x.strip() for x in 
          sel.xpath('//meta[contains(@name, "keywords")]/@content').
          extract()[0].split(",") 
          if len(x.strip()) > 0]
        json_obj["description"] = sel.xpath(
          '//meta[contains(@name, "description")]/@content').extract()[0]
        # extract dynamic text blob from text using regex
        for line in text.split("\n"):
            text_blob = get_candidate_blob(line, sel)
            if text_blob is not None:
                break
        if text_blob is None:
            print "=====", in_path
            continue
        plain_text = to_plain_text(text_blob)
        plaintext_hash = md5_hash(plain_text)
        json_obj["text"] = plain_text
        if doc_digests.has_key(plaintext_hash):
            update_json(json_obj, doc_digests[plaintext_hash])
        else:
            add_json(json_obj, json_fid)
            doc_digests[plaintext_hash] = json_fid            
        json_fid += 1
print "# unique docs:", len(doc_digests)
