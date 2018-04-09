import numpy
import pandas as pd
import matplotlib.pyplot as plt
import sys
from bs4 import BeautifulSoup
import re
import urllib.request
import json
from mpl_toolkits.basemap import Basemap
from io import BytesIO
import PIL.Image as Image
path = sys.argv[1] + "/html/security.htm"
print("opening: "+path)
with open(path) as fp:
    soup = BeautifulSoup(fp, 'lxml')
list_ips = []
list_locs = []
x = []
y = []
IPs = soup.findAll(text = re.compile("IP Address"))
for IP in IPs:
    if "." in IP:
        if IP[12:] not in list_ips:
            list_ips.append(IP[12:])
for IP in list_ips:
    url = 'http://ipinfo.io/'+IP+'/json'
    response = urllib.request.urlopen(url)
    data = json.load(response)
    loc = data['loc']
    if loc not in list_locs:
        list_locs.append(loc)
        print(loc)
map = Basemap(projection='mill',lon_0=0)
map.drawcoastlines()
map.drawparallels(numpy.arange(-90,90,30),labels=[1,0,0,0])
map.drawmeridians(numpy.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])
lat = []
lon = []
for loc in list_locs:
    lat.append(float(loc[:loc.index(",")]))
    lon.append(float(loc[loc.index(",")+1:]))
x,y = map(lon, lat)
map.plot(x, y, 'bo', markersize=3)
plt.show()
path = sys.argv[1] + "/html/ads.htm"
print("opening: "+path)
with open(path) as fp:
    soup = BeautifulSoup(fp, 'lxml')
advertisers_with_your_contact_info = soup.find('h2',text='Advertisers with your contact info')
companies = advertisers_with_your_contact_info.next_sibling
w=10
h=10
fig=plt.figure(figsize=(8, 8))
columns = 4
rows = 5
i = 1

for company in companies:
    name = company.text
    if "(" not in name and "（" not in name:
        name = name.replace(" ","")
        print(name + ".com")
        url = "https://logo.clearbit.com/" + name + ".com"
        try:
            file = BytesIO(urllib.request.urlopen(url).read())
            img = Image.open(file)
            fig.add_subplot(rows, columns, i)
            plt.imshow(img)
            plt.axis('off')
        except urllib.error.HTTPError as e:
            print("couldn't find company image for url")
    i = i + 1
plt.suptitle('Advertisers with your contact information', fontsize=14, fontweight='bold')
plt.show()