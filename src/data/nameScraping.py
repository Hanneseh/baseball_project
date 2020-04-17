import requests 
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re
import statsapi
from pymongo import MongoClient

#Database connection
client = MongoClient('localhost', 27017)
db = client['baseballmd']

weburl = urllib.request.urlopen('https://www.honkbalsite.com/profhonkballers/')
data = weburl.read()
soup = BeautifulSoup(data, 'html.parser')

milbLinks = soup.findAll("a", href=re.compile("milb"))
mlbLinks = soup.findAll("a", href=re.compile("mlb"))
allLinks = milbLinks + mlbLinks

for player in allLinks:
    playerDict = {}
    linkplayer = player.get('href')
    playerDict['id'] = int(re.search(r"\d{6}", linkplayer).group(0))
    rawdata = statsapi.get('person', {'personId':playerDict['id']})
    for people in rawdata['people']:
        playerDict['fullName'] = people['fullName']
        playerDict['birthDate'] = people['birthDate']
        playerDict['currentAge'] = people['currentAge']
        playerDict['height'] = people['height']
        playerDict['weight'] = people['weight']
        playerDict['active'] = people['active']
        playerDict['position'] = people['primaryPosition']['abbreviation']
    playerDict.pop('_id', None)
    db['players'].insert(playerDict)