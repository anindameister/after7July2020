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
    if url.ok:
        filename = url.split('/')[-1]
        if url.exists():
            filename = url.split('/')[-1]
        else:
            url.touch()
            filename = url.split('/')[-1]
    os.chdir(r"F:\yolov3-master\test")
    a=urllib.request.urlretrieve(s, filename)
    fileName.append(filename)

downloadingThePhotos2=time.time()

af=pd.DataFrame(data={"URLs":url_list,"Image name":fileName})
af.to_csv("F:\\yolov3-master\\excels\\urlsFilenames.csv",sep=',',index=False)

doingYolo1=time.time()

os.chdir(r"F:\yolov3-master")
# subprocess.run('dir', shell=True)
# subprocess.run('python detect.py --cfg cfg\yolov3.cfg --weights weights\yolov3.pt --source test --save-txt', shell=True)
subprocess.run('python detect.py --cfg cfg\yolov3.cfg --weights weights\yolov3.pt --source test --save-txt --conf-thres 0.8', shell=True)
doingYolo2=time.time()

imageDimentionList=[]
ImageFilenameList=[]

images = glob.glob("output/*.*")
imagess = images.copy()
for i in imagess:
    if i.endswith(".txt") or i.endswith(".svg"):
        print(i)
        images.remove(i)
print("ok")
for image in images:
    with open(image, 'rb') as file:
        img = Image.open(file)
        imageSize=img.size
        imageDimentionList.append(imageSize)
        image=image[7:]
        ImageFilenameList.append(image)


lengthDimention = [item[1] for item in imageDimentionList]
breadthDimention=[item[0] for item in imageDimentionList]
wikiDimention = {'dimention': imageDimentionList,'Image name': ImageFilenameList, 'Y-Image Dimentions':lengthDimention, 'X-Image Dimentions':breadthDimention}

df = pd.DataFrame(wikiDimention , columns= ['dimention', 'Image name', 'Y-Image Dimentions', 'X-Image Dimentions'])

print (df)
df.to_csv('F:\\yolov3-master\\excels\\output.csv', encoding='utf-8', index=False)
print(ImageFilenameList,imageDimentionList)

dir_path = 'F:\\yolov3-master\\output'
os.chdir(dir_path)
src_files = os.listdir(dir_path)
for file_name in src_files:
    if file_name.endswith(".txt"):
        full_file_name = os.path.join(dir_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, 'F:\\yolov3-master\\texts')

dir_path = 'F:\\yolov3-master\\texts'  # Put the path to the texts directory here
os.chdir(dir_path)
file_name = []
for f in os.listdir():
    f_name,f_ext=os.path.splitext(f)
    file_name.append(f_name)

file_content = {
    'X1': [],
    'Y1': [],
    'X2': [],
    'Y2': [],
    'object name': [],
    'Image name': []
}


for i in os.listdir():
    f_name,f_ext=os.path.splitext(i)
    file1 = open(i, "r+")
    txt = file1.readlines()

    for line in txt:
        l = line.split(' ')
        if l[-1] == '\n':
            l = l[:-1]
        file_content['X1'].append(l[0])
        file_content['Y1'].append(l[1])
        file_content['X2'].append(l[2])
        file_content['Y2'].append(l[3])
        file_content['object name'].append(l[4])
        a=np.array(file_content['X1'], dtype=np.float)
        b=np.array(file_content['X2'], dtype=np.float)
        c=np.array(file_content['Y1'], dtype=np.float)
        d=np.array(file_content['Y2'], dtype=np.float)
        file_content['X-centre']=((a+b)/2)
        file_content['Y-centre']=((c+d)/2)
        file_content['Image name'].append(f_name)

df = DataFrame(data=file_content)
print(df)
df.to_csv('F:\\yolov3-master\\excels\\imageNameBoundingBoxesObjectNameXYcenter.csv',index=False) 



df1 = pd.read_csv('F:\\yolov3-master\\excels\\imageNameBoundingBoxesObjectNameXYcenter.csv')

df2 = pd.read_csv('F:\\yolov3-master\\excels\\urlsFilenames.csv')

df3=df1.merge(df2, on='Image name', how='left')

df3.to_csv('F:\\yolov3-master\\excels\\imageNameBoundingBoxesObjectNameXYcenterURL.csv', encoding='utf-8', index=False)

df4 = pd.read_csv('F:\\yolov3-master\\excels\\imageNameBoundingBoxesObjectNameXYcenterURL.csv')

df5 = pd.read_csv('F:\\yolov3-master\\excels\\output.csv')

df6=df4.merge(df5, on='Image name', how='left')

df6.to_csv('F:\\yolov3-master\\excels\\imageNameBoundingBoxesObjectNameXYcenterURLImageDim.csv', encoding='utf-8', index=False)


dddf = pd.read_csv('F:\yolov3-master\excels\imageNameBoundingBoxesObjectNameXYcenterURLImageDim.csv')

# automationUrl2downloadPhoto2yolo2ioRel&ooRelexcel

hasinthecenter = []
def center_object(image , object, x_dim, y_dim, x_centre, y_centre):
    if x_centre>0.3*x_dim and x_centre<0.66*x_dim and y_centre>0.3*y_dim and y_centre<0.66*y_dim:
        hasinthecenter.append(object)
    else:
        hasinthecenter.append('na')


for _,row in dddf.iterrows():

    center_object(row['Image name'], row['object name'], row['X-Image Dimentions'], row['Y-Image Dimentions'], row['X-centre'], row['Y-centre'])
        

hasintheleft = []
def center_object(image , object, x_dim, y_dim, x_centre, y_centre):
    if x_centre<0.3*x_dim:
        hasintheleft.append(object)
    else:
        hasintheleft.append('na')


for _,row in dddf.iterrows():

    center_object(row['Image name'], row['object name'], row['X-Image Dimentions'], row['Y-Image Dimentions'], row['X-centre'], row['Y-centre'])

hasinthetop= []
def center_object(image , object, x_dim, y_dim, x_centre, y_centre):
    if y_centre<0.3*y_dim:
        hasinthetop.append(object)
    else:
        hasinthetop.append('na')


for _,row in dddf.iterrows():

    center_object(row['Image name'], row['object name'], row['X-Image Dimentions'], row['Y-Image Dimentions'], row['X-centre'], row['Y-centre'])

hasintheright = []
def center_object(image , object, x_dim, y_dim, x_centre, y_centre):
    if x_centre>0.66*x_dim:
        hasintheright.append(object)
    else:
        hasintheright.append('na')



for _,row in dddf.iterrows():

    center_object(row['Image name'], row['object name'], row['X-Image Dimentions'], row['Y-Image Dimentions'], row['X-centre'], row['Y-centre'])

hasinthebottom = []
def center_object(image , object, x_dim, y_dim, x_centre, y_centre):
    if y_centre>0.66*y_dim:
        hasinthebottom.append(object)
    else:
        hasinthebottom.append('na')



for _,row in dddf.iterrows():

    center_object(row['Image name'], row['object name'], row['X-Image Dimentions'], row['Y-Image Dimentions'], row['X-centre'], row['Y-centre'])


ddf=dddf.assign(has_on_the_left=hasintheleft,has_on_the_right=hasintheright,has_on_the_top=hasinthetop,has_on_the_bottom=hasinthebottom,has_in_the_center=hasinthecenter)


ddf.columns = [c.replace('_', ' ') for c in ddf.columns]
print(ddf)

# excel_parameters={'has on the left':hasintheleft,"has on the right":hasintheright,"has on the top":hasinthetop,"has on the bottom":hasinthebottom,"has in the center":hasinthecenter}
# ddf=dddf.assign(excel_parameters, columns=['has on the left','has on the right','has on the top','has on the bottom','has in the center'])
ddf.to_csv("F:\\data2rdf-master\\src\\main\\resources\\imageHasOnLeftRightCenterTopBottom.csv",sep=',',index=False)
ddf.to_csv("F:\\yolov3-master\\excels\\imageHasOnLeftRightCenterTopBottom.csv",sep=',',index=False)
# F:\data2rdf-master\src\main\resources
dir_path = 'F:\\data2rdf-master'
# F:\data2rdf-master
os.chdir(dir_path)
subprocess.run('mvn clean install', shell=True)

dir_path = 'F:\\data2rdf-master\\target'
# F:\data2rdf-master
os.chdir(dir_path)
subprocess.run('java -jar data2rdf-1.0-SNAPSHOT.jar -f eu.qanswer.data2rdf.mappings.imageannotation.ObjectPosition -o outputfile.nt', shell=True)
dir_path = 'F:\\data2rdf-master\\target'
# F:\data2rdf-master
os.chdir(dir_path)


f=open("outputfile.nt", "rb")  
f1=open('ObjectPositionOutput.nt','ab')
for x in f.readlines():
    f1.write(x)
f.close()
f1.close()

f2=open("outputfile.nt_ontology", "rb")  
f3=open('ObjectPositionOutput.nt','ab')
for y in f2.readlines():
    f3.write(y)
f2.close()
f3.close()
t2=time.time()

print("we got the URLs in",getTheUrl-t1,"seconds which is",(getTheUrl-t1)/60,"minutes")
print("we got the uncompressed photos downloaded from the urls in",downloadingThePhotos2-downloadingThePhotos1,"seconds which is",((downloadingThePhotos2-downloadingThePhotos1)/60),"minutes")
print("we got the yolo implemented in",doingYolo2-doingYolo1,"seconds which is",((doingYolo2-doingYolo1)/60),"minutes")
print("completed the program in",t2-t1,"seconds")
print("completed the program in",((t2-t1)/60),"minutes")