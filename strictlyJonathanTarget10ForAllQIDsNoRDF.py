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

readingTheTextFile = open("H:\\report&demoPaper\\class number class name QID.txt", "r")
allQIDs=[]
for contentsLineByLine in readingTheTextFile:
#   print(contentsLineByLine)
  attemptingContentModification = contentsLineByLine.split('-')
  justWantQIDs=attemptingContentModification[1]
  justWantQIDs=justWantQIDs.split('\n')
  QIDs=justWantQIDs[0]
  allQIDs.append(QIDs)
downloadingThePhotos1=time.time()
url_list = []
sList=[]
fileName=[]
endpoint = "https://commons.wikimedia.org/w/api.php"
PARAMS = {
    'action': 'query',
    'list': 'search',
    'srlimit': '10',
    'srnamespace': '6',
    'format': 'json',
    'continue': '-||'
}
dest_folder="F:\\yolov3-master\\test"
for individualQID in allQIDs:
    if __name__=='__main__':
        i = 10
        while i <= 10:
            i += 10
            PARAMS['srsearch'] = 'haswbstatement:P180=' + individualQID
            PARAMS['sroffset'] = i
            r = requests.get(url=endpoint, params=PARAMS)
            if r.ok:
                for image in r.json()['query']['search']:
                    URL = 'https://commons.wikimedia.org/wiki/Special:EntityData/M' + str(image['pageid']) + '.ttl'
                    r = requests.get(url=URL)
                    g = Graph()
                    g.parse(io.StringIO(r.content.decode("utf-8")), format="ttl")
                    for row in g.query("SELECT DISTINCT ?o1 WHERE { ?s1 <http://schema.org/contentUrl> ?o1. }"):
                        # print(row[0])
                        url_list.append(row[0].__str__())
        print(len(url_list))
        
        for url in url_list:
            print(url)

            
            newUrlAttempt=url.split('/')[-3:]
            newUrlAttempt1=newUrlAttempt.insert(0, 'thumb') 
            newUrlAttempt2=url.split('/')[0:-3]

            newUrlAttempt3=url.split('/')
            newUrlAttempt3.insert(5, 'thumb') 
            newUrlAttempt3.insert(len(newUrlAttempt3),'200px-')
            newUrlAttempt3[-1]=newUrlAttempt3[-2]
            newUrlAttempt3.insert(len(newUrlAttempt3)-1,'200px-')
            newUrlAttempt3[9 : 11] = [''.join(newUrlAttempt3[9 : 11])] 
            s = "/"
            newUrl = s.join(newUrlAttempt3) 
            filename=url.split('/')[-1]
            file_path = os.path.join(dest_folder, filename)
            r = requests.get(newUrl)
            if r.ok:
                with open(file_path, "wb") as f:
                    f.write(r.content)
