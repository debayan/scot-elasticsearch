from elasticsearch import Elasticsearch
from elasticsearch import helpers
import sys, os, json
from collections import Counter

es = Elasticsearch()

##Simple search for a particular word, returns only  10 results by default
res = es.search(index="scotindex1", body={"query": {"match": {"words": {"query": "Blues#PROPN"}}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for idx,hit in enumerate(res['hits']['hits']):
    print(idx,hit["_source"])

##Search for a particular word, returns top 100 results
res = es.search(index="scotindex1", body={"size":100, "query": {"match": {"words": {"query": "Blues#PROPN"}}}})
print("Got %d Hits:" % res['hits']['total']['value'])
for idx,hit in enumerate(res['hits']['hits']):
    print(idx, hit["_source"])

##Search for a particular word, return all results (use the scroll feature of ES)
data = es.search(index="scotindex1", scroll='2m', body={"query": {"match": {"words": {"query": "Blues#PROPN"}}}})
print("Got %d Hits:" % res['hits']['total']['value'])

sid = data['_scroll_id']
scroll_size = len(data['hits']['hits'])
count = 0
while scroll_size > 0:
    "Scrolling..."
    # Before scroll, process current batch of hits
    for idx,hit in enumerate(data['hits']['hits']):
        print(count, hit['_source'])
        count += 1
    data = es.scroll(scroll_id=sid, scroll='2m')
    # Update the scroll ID
    sid = data['_scroll_id']
    # Get the number of results that returned in the last scroll
    scroll_size = len(data['hits']['hits'])

##Search for 2 words, and find their common co-occurring words
counts = {} #dict to maintain co-occurence counts
data = es.search(index="scotindex1", scroll='2m', body={"query": {"match": {"words": {"query": "Blues#PROPN"}}}}) #1st word
print("Got %d Hits:" % data['hits']['total']['value'])

sid = data['_scroll_id']
scroll_size = len(data['hits']['hits'])
count = 0
while scroll_size > 0:
    "Scrolling..."
    # Before scroll, process current batch of hits
    for idx,hit in enumerate(data['hits']['hits']):
        #print(count, hit['_source'])
        words = hit['_source']['words'].split(',')
        for word in words:
            counts[word] = counts.get(word, 0) + 1
        count += 1
    data = es.scroll(scroll_id=sid, scroll='2m')
    # Update the scroll ID
    sid = data['_scroll_id']
    # Get the number of results that returned in the last scroll
    scroll_size = len(data['hits']['hits'])


data = es.search(index="scotindex1", scroll='2m', body={"query": {"match": {"words": {"query": "world#PROPN"}}}}) #2nd word
print("Got %d Hits:" % data['hits']['total']['value'])

sid = data['_scroll_id']
scroll_size = len(data['hits']['hits'])
count = 0
while scroll_size > 0:
    "Scrolling..."
    # Before scroll, process current batch of hits
    for idx,hit in enumerate(data['hits']['hits']):
        #print(count, hit['_source'])
        words = hit['_source']['words'].split(',')
        for word in words:
            counts[word] = counts.get(word, 0) + 1
        count += 1
    data = es.scroll(scroll_id=sid, scroll='2m')
    # Update the scroll ID
    sid = data['_scroll_id']
    # Get the number of results that returned in the last scroll
    scroll_size = len(data['hits']['hits'])

C = Counter(counts)
print(C.most_common(3))

