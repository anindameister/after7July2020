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

t1=time.time()

url_list = []

#?action=query&list=search&srsearch=haswbstatement:P180=Q7378&srnamespace=6&format=json
URL = "https://commons.wikimedia.org/w/api.php"

# defining a params dict for the parameters to be sent to the API
PARAMS = {
    'action' :'query',
    'list': 'search',
    'srsearch': 'haswbstatement:P180=Q1144312',
    'srnamespace': '6',
    'format': 'json',
    }

# sending get request and saving the response as response object
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

getTheUrl=time.time()

downloadingThePhotos1=time.time()
sList=[]
fileName=[]
for url in url_list:
    filename = url.split('/')[-1]
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

    try:
        os.chdir(r"F:\yolov3-master\test")
        a=urllib.request.urlretrieve(s, filename)
        fileName.append(filename)
  

    except OSError as oserr:
      if oserr.errno ==36:
        pass
      else:
        raise

    sList.append(s)
print(sList)
