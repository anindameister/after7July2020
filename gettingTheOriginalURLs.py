import argparse
import subprocess
import numpy as np
import os
import io
#download2yolo2excel
import requests
from rdflib import Graph
import urllib.request

import glob
from PIL import Image
import numpy as np
import pandas as pd
import time
import math
import os
import shutil
from pandas import DataFrame, read_excel, merge
from pandas import DataFrame
url_list=[]
URL = "https://commons.wikimedia.org/w/api.php"
PARAMS = {
    'action' :'query',
    'list': 'search',
    'srsearch': 'haswbstatement:P180=Q7378',
    'srnamespace': '6',
    'format': 'json',
    }
r = requests.get(url = URL, params = PARAMS)
        
for image in r.json()['query']['search']:
        # print(image['pageid'])
    URL = 'https://commons.wikimedia.org/wiki/Special:EntityData/M'+str(image['pageid'])+'.ttl'
    r = requests.get(url=URL)
        # # print(r.content)

    g = Graph()
        # # print(io.StringIO(r.content.decode("utf-8") ))
    g.parse(io.StringIO(r.content.decode("utf-8") ), format="ttl")

        # # print(len(g))  # prints 2

    import pprint

    for stmt in g:
        if 'http://schema.org/contentUrl' == str(stmt[1]):
            imageURL = (stmt[2])
            url_list.append(imageURL)

# print(url_list)
getTheUrl=time.time()
print(getTheUrl)

fileName=[]
for url in url_list:
    newUrlAttempt=url.split('/')[-3:]
    newUrlAttempt1=newUrlAttempt.insert(0, 'thumb') 
    newUrlAttempt2=url.split('/')[0:-3]
    
    # newUrl=newUrlAttempt2[0]+newUrlAttempt2[2]+newUrlAttempt2[3]+newUrlAttempt2[4]+newUrlAttempt1
    newUrlAttempt3=url.split('/')
    newUrlAttempt3.insert(5, 'thumb') 
    newUrlAttempt3.insert(len(newUrlAttempt3),'200px-')
    newUrlAttempt3[-1]=newUrlAttempt3[-2]
    newUrlAttempt3.insert(len(newUrlAttempt3)-1,'200px-')
    newUrlAttempt3[9 : 11] = [''.join(newUrlAttempt3[9 : 11])] 
    s = "/"
    s = s.join(newUrlAttempt3) 
    
    print(s)

# thislist = ["apple", "banana", "cherry"]
# thislist[1] = "blackcurrant"
# print(thislist)
    # +'/200px-'+url.split('/')[-1]

# https://upload.wikimedia.org/wikipedia/commons
# /thumb/d/dc/20080804_freight_bicycle_Shanghai_2383.jpg/200px-20080804_freight_bicycle_Shanghai_2383.jpg

# https://upload.wikimedia.org/wikipedia/commons/3/37/African_Bush_Elephant.jpg
# https://upload.wikimedia.org/wikipedia/commons/d/dc/20080804_freight_bicycle_Shanghai_2383.jpg
# https://www.geeksforgeeks.org/python-perform-append-at-beginning-of-list/
# https://www.geeksforgeeks.org/join-function-python/
# https://stackoverflow.com/questions/30212447/how-to-add-element-in-python-to-the-end-of-list-using-list-insert