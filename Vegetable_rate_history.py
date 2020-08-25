from bs4 import BeautifulSoup as bs
import requests
import datetime
from datetime import datetime as dati
from pytz import timezone
from matplotlib import pyplot
import os
import pprint

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

destinationfoldername = 'data/'
if not os.path.exists(destinationfoldername):
    os.makedirs(destinationfoldername)
vegdata = []
maindomainlink = 'https://www.livechennai.com/'
contenttowrite = ''
count1 = 0
scraper1 = requests.Session()
scraper1.trust_env = False

url12 = scraper1.get("https://www.livechennai.com/Vegetable_price_chennai.asp").text
mainsoup = bs(url12)

soup_ins = mainsoup.find_all('ins',attrs={'class':'adsbygoogle'})[-1].contents[0]
soup_ins = soup_ins.replace('   ','')
soup_ins = soup_ins.replace('\r','')
soup_ins = soup_ins.replace('&gt;','>')
soup_ins = [i for i in soup_ins.split('\n') if i.lstrip() != '']

output = []
for i in soup_ins:
  if 'img' in i:
    i = i.replace(' img ',' <img ')
    i = i.replace('!--img','<!--img')
    
  if '/' in i:
    if '/tr' in i:
      i = i.replace('/tr','</tr')
    if '/td>' in i:
      i = i.replace('/td>','</td>')
  if i[0]=='}':
    i = i
  else:
    i = '<' + i
  output.append(i)
mainsoup = BeautifulSoup('\n'.join(output))

tabledata = mainsoup.find('table',attrs={'class':'table-price1'})
rows = tabledata.find_all('tr',attrs={'style':None})
totalnoofvegetables = len(rows)

for a in rows:
  vegname = a.find('td',attrs={'align':None}).text
  vegname = vegname[:vegname.rfind(')')+1]
  vegrate = int(a.find('td',attrs={'align':'right'}).text.replace('.00',''))
  vegdata.append([vegname,vegrate])

def sortvegdata(item1):
  return item1[1]
vegdata.sort(key=sortvegdata)
print(vegdata)

for item in vegdata:
  count1 += 1
  if count1 == totalnoofvegetables :
    contenttowrite = contenttowrite + item[0] + ',' + str(item[1])
  else:
    contenttowrite = contenttowrite + item[0] + ',' + str(item[1]) + '\n'

filename = datetime.date.today().strftime("%Y-%m-%d") +".csv"
with open(destinationfoldername + filename,'w',encoding='utf-8') as f2 :
  f2.write(contenttowrite)

fulldata = {}
to_test_files = []

for path, subdirs, files in os.walk(destinationfoldername):
    for file in files:
      if '.csv' in file:
        to_test_files.append(file)

for i in to_test_files:
  dateofdata = i[:-4]
  with open(destinationfoldername + i,'r') as f1:
    tempcontent1 = f1.read().splitlines()
  for line in tempcontent1:
    if line:
      vegname, vegrate = line.split(',')
      if vegname not in fulldata:
        fulldata[vegname] = {}
        fulldata[vegname][dateofdata] = vegrate
      else:
        if dateofdata not in fulldata[vegname]:
          fulldata[vegname][dateofdata] = vegrate

print(fulldata)
with open(destinationfoldername + 'Fulldata.txt','w') as f2:
  f2.write(pprint.pformat(fulldata))

graphpath = dati.now(timezone('Asia/Kolkata')).strftime('%Y-%m-%d_%H-%M-%S') + ' Graph/'

if not os.path.exists(graphpath):
  os.makedirs(graphpath)

# !rm -rf 1

for vegs in fulldata.keys():
  graphimagename = graphpath + vegs + '.png'
  xaxisvalues = []
  yaxisvalues = []
  for dates in fulldata[vegs].keys():
    xaxisvalues.append(dates)
    yaxisvalues.append(int(fulldata[vegs][dates]))

  xaxisvalues, yaxisvalues = zip(*sorted(zip(xaxisvalues, yaxisvalues)))
  plt.figure(figsize=(10,10))
  _ =plt.plot(xaxisvalues,yaxisvalues,label='Last Value = '+str(yaxisvalues[-1]))
  plt.title(vegs)
  plt.xlabel('Date')
  plt.ylabel('Amount In Rupee')
  plt.gcf().autofmt_xdate()
  plt.axis('tight')
  plt.legend()
  plt.grid()
  plt.savefig(graphimagename)
  # plt.show()
  # plt.close()