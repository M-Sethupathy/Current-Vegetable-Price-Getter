# Packages for Fetching and parsing web data
from bs4 import BeautifulSoup as bs
import requests

# Packages for time management
from datetime import datetime as dati
from pytz import timezone

# Packages for creating Graphs
from matplotlib import pyplot
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Package for file operation
import os

# Package for prettify print
import pprint


# Create Data folder if not exists
destinationfoldername = 'data/'
if not os.path.exists(destinationfoldername):
    os.makedirs(destinationfoldername)

# Main link to Scrape
maindomainlink = 'https://www.livechennai.com/'

# Initialize Basic variables needed for this operation
vegdata = []
contenttowrite = ''
count1 = 0
to_test_files = []


# Dictionary to store historical data of a vegetable
fulldata = {}

# Initializing Scraper
scraper1 = requests.Session()
scraper1.trust_env = False

# Requesting and parsing main link
url12 = scraper1.get("https://www.livechennai.com/Vegetable_price_chennai.asp").text
mainsoup = bs(url12)

# Parsing misshaped data that is the code for table
soup_ins = mainsoup.find_all('ins',attrs={'class':'adsbygoogle'})[-1].contents[0]
soup_ins = soup_ins.replace('   ','')
soup_ins = soup_ins.replace('\r','')
soup_ins = soup_ins.replace('&gt;','>')
soup_ins = [i for i in soup_ins.split('\n') if i.lstrip() != '']

# For storing outputs
output = []

# Iterating through each img tags and complete parsing
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

# Parsing corrected html code using BeautifulSoup
mainsoup = BeautifulSoup('\n'.join(output))

# Capturing the table code
tabledata = mainsoup.find('table',attrs={'class':'table-price1'})

# Capturing all rows in that row
rows = tabledata.find_all('tr',attrs={'style':None})

# Total number of rows in table
totalnoofvegetables = len(rows)

# Iterating through each row and getting 
# each vegetable name and it's price
for a in rows:
  vegname = a.find('td',attrs={'align':None}).text
  vegname = vegname[:vegname.rfind(')')+1]
  vegrate = int(a.find('td',attrs={'align':'right'}).text.replace('.00',''))
  vegdata.append([vegname,vegrate])


# Function to return second lement of that list that is vegetable price
# This function is used for sorting the vegdata with respecto to price
def sortvegdata(item1):
  return item1[1]
vegdata.sort(key=sortvegdata)
print(vegdata)


# Iterating through each vegetable detail 
for item in vegdata:
  count1 += 1
  
  # Check if last vegetable is reached 
  if count1 == totalnoofvegetables :
    contenttowrite = contenttowrite + item[0] + ',' + str(item[1])
  else:
  # Process every element except last element
    contenttowrite = contenttowrite + item[0] + ',' + str(item[1]) + '\n'

# Creating csv filename with today format
filename = dati.now().strftime("%Y-%m-%d") +".csv"

# Writing content to file
with open(destinationfoldername + filename,'w',encoding='utf-8') as f2 :
  f2.write(contenttowrite)


# Traversing through each csv file in directory to get csv content
for path, subdirs, files in os.walk(destinationfoldername):
    for file in files:
      if '.csv' in file:
        to_test_files.append(file)

# Looping through collected data
for i in to_test_files:
  dateofdata = i[:-4]
  
  # Reading all previous CSVs
  with open(destinationfoldername + i,'r') as f1:
    tempcontent1 = f1.read().splitlines()
  
  # Reading every single line in CSVs
  for line in tempcontent1:
    if line:
      vegname, vegrate = line.split(',')
      
      # Historical data to dictionary
      if vegname not in fulldata:
        fulldata[vegname] = {}
        fulldata[vegname][dateofdata] = vegrate
      else:
        if dateofdata not in fulldata[vegname]:
          fulldata[vegname][dateofdata] = vegrate

print(fulldata)


open('1.txt', 'w')

# Writing All collected historical data to a file
with open(destinationfoldername + 'Fulldata.txt','w') as f2:
  f2.write(pprint.pformat(fulldata))

# Output folder for graphs and creating it if not exists
graphpath = dati.now(timezone('Asia/Kolkata')).strftime('%Y-%m-%d_%H-%M-%S') + ' Graph/'
if not os.path.exists(graphpath):
  os.makedirs(graphpath)

# Creating graphs for each vegetable with the help of data from historical data
for vegs in fulldata.keys():
  
  # Output graph name
  graphimagename = graphpath + vegs + '.png'
  xaxisvalues = []
  yaxisvalues = []
  
  # Plotting x, y coordinates
  for dates in fulldata[vegs].keys():
    xaxisvalues.append(dates)
    yaxisvalues.append(int(fulldata[vegs][dates]))
    
  # Sorting both axes
  xaxisvalues, yaxisvalues = zip(*sorted(zip(xaxisvalues, yaxisvalues)))
  
  # Assiging graph size
  plt.figure(figsize=(10,10))
  
  # Plotting graph
  _ =plt.plot(xaxisvalues,yaxisvalues,label='Last Value = '+str(yaxisvalues[-1]))
  
  # Assiging graph title
  plt.title(vegs)
  
  # Assiging x, y labels
  plt.xlabel('Date')
  plt.ylabel('Amount In Rupee')
  
  # Setting graph to change dateformat
  plt.gcf().autofmt_xdate()
  plt.axis('tight')
  
  # Drawing legend
  plt.legend()
  
  # Showing grid
  plt.grid()
  
  # Saving graph to file
  plt.savefig(graphimagename)
  
  
  # plt.show()
  # plt.close()
