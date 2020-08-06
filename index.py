from elasticsearch import Elasticsearch
from elasticsearch import helpers
import sys, os, json

es = Elasticsearch()
actions = []
count = 0
with open("fin_dep_jobimstext.tsv") as infile:
    for line in infile:
        words,wordfeatures,url,text,year = line.split('\t')
        #print(words,wordfeatures,url,text,year)
        doc = {
            'words': words,
            'wordfeatures': wordfeatures,
            'uri': url,
            'text': text,
            'year': year
        }
        mdoc = {"_index": 'scotindex1',
                "_source": doc}
        actions.append(mdoc)
        if len(actions) % 10000 == 0 and len(actions) > 1:
            count += len(actions)
            res = helpers.bulk(es, actions)
            print(count,res)
            actions = []
res = helpers.bulk(es, actions)
print(count + len(actions),res)
