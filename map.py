#! python3
import glob
import yaml
import time
import lxml.etree
import sys
import os
import requests


def download(url, filename):
    with open(filename, 'wb') as f:
        response = requests.get(url, stream=True)
        total = response.headers.get('content-length')
        sys.stdout.write('binfile size = ')
        sys.stdout.write(total)
        sys.stdout.write('\n')
        if total is None:
            f.write(response.content)
        else:
            downloaded = 0
            total = int(total)
            for data in response.iter_content(chunk_size=max(int(total/1000), 1024*1024)):
                downloaded += len(data)
                f.write(data)
                pct = 100 * downloaded / total
                sys.stdout.write(str(pct))
                sys.stdout.write(' %\n')
#                done = int(50*downloaded/total)
#                sys.stdout.write('\r[{}{}]'.format('X' * done, '.' * (50-done)))
#                sys.stdout.flush()
    sys.stdout.write('\n')



tests=[]
first = 1
for filename in glob.glob('*.yaml'):
    f = open(filename)
    dataMap = yaml.safe_load(f)
    f.close()
    print ("")
    print ("Reading "+filename+" : "+str(dataMap['from']['lat']) + "," + str(dataMap['from']['lng']) +" to "+str(dataMap['to']['lat']) + "," + str(dataMap['to']['lng']))
    bottom = dataMap['from']['lat']
    left = dataMap['from']['lng']
    top = dataMap['to']['lat']
    right = dataMap['to']['lng']
    print ("bottom = " + str(bottom) + " left = " + str(left) +" top = " + str(top) + " right = " + str(right))
    if (bottom > top):
        bottom = dataMap['to']['lat']
        top = dataMap['from']['lat']
        print ("swapped bottom and top")
    if (left > right):
        left = dataMap['to']['lng']
        right = dataMap['from']['lng']
        print ("swapped left and right")
    print ("bottom = " + str(bottom) + " left = " + str(left) +" top = " + str(top) + " right = " + str(right))
    if (first == 1):
        first = 0
        mapbottom = bottom
        mapleft = left
        maptop = top
        mapright = right
    else:
        if (bottom < mapbottom):
            mapbottom = bottom
            print ("expanded bottom")
        if (left < mapleft):
            mapleft = left
            print ("expanded left")
        if (top > maptop):
            maptop = top
            print ("expanded top")
        if (right > mapright):
            mapright = right
            print ("expanded right")
    print ("mapbottom = " + str(mapbottom) + " mapleft = " + str(mapleft) +" maptop = " + str(maptop) + " mapright = " + str(mapright))
mapbottom = round(mapbottom - 0.15 , 1)
mapleft = round(mapleft - 0.15 , 1)
maptop = round(maptop + 0.15 , 1)
mapright = round(mapright + 0.15 , 1)
print("")
print("after rounding")
print ("mapbottom = " + str(mapbottom) + " mapleft = " + str(mapleft) +" maptop = " + str(maptop) + " mapright = " + str(mapright))
url = "http://maps.navit-project.org/api/map/?bbox=" + str(mapleft) + "," + str(mapbottom) + "," + str(mapright) + "," + str(maptop) + ".bin"
print ("url = ")
print (url)
download(url, 'navit/bin/navit/maps/custommap.bin')  
