import requests 
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re
import statsapi
from pymongo import MongoClient

#Database connection
client = MongoClient("localhost:27017")
db = client.baseballmd
client.list_database_names()

weburl = urllib.request.urlopen('https://www.honkbalsite.com/profhonkballers/')
data = weburl.read()
soup = BeautifulSoup(data, 'html.parser')

milbLinks = soup.findAll("a", href=re.compile("milb"))
mlbLinks = soup.findAll("a", href=re.compile("mlb"))
allLinks = milbLinks + mlbLinks

playersid = pd.DataFrame(columns=['Name', 'Id', 'birthdate', 'Age', 'Height', 'Weight', 'Active status', 'Position'])
playersid
i = 0
for players in allLinks:
    name = players.contents[0]
    linkplayer = players.get('href')
    playerid = re.search(r"\d{6}", linkplayer).group(0)
    playerid = int(playerid)
    rawdata = statsapi.get('person', {'personId':playerid})
    
    for people in rawdata['people']:
        birthdate = people['birthDate']
        currentAge = people['currentAge']
        height = people['height']
        weight = people['weight']
        active = people['active']
        abbreviation = people['primaryPosition']['abbreviation']

    playersid.loc[i] = [name] + [playerid] + [birthdate] + [currentAge] + [height] + [weight] + [active] + [abbreviation]
    i += 1
    
playersid

db.baseballmd.insert_many(playersid.to_dict('records'))

