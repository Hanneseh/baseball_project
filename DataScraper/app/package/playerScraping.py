import requests 
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import re
import statsapi
from app.config import getDB

client = getDB()
db = client['baseballmd']

documentsChange = {"inserts":0,"updates":0}

def getPlayerInfo():
    print('get player info started')

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

        weburl = urllib.request.urlopen(str(linkplayer))
        mlbSite = weburl.read()
        mlbSoup = BeautifulSoup(mlbSite, 'html.parser')

        if re.search('mlb', linkplayer):
            imgDiv = mlbSoup.findAll("div", class_='player-header__container')
            imgTag = imgDiv[0].findAll("img", class_='player-headshot')
            imgSrcLink = imgTag[0].get("src")
            playerDict['imageLink'] = str(imgSrcLink)

        if re.search('milb', linkplayer):
            imgDiv = mlbSoup.findAll("div", id='main_image')
            imgTag = imgDiv[0].findAll("img")
            imgSrcLink = imgTag[0].get("src")
            playerDict['imageLink'] = 'http://www.milb.com' + str(imgSrcLink)

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
        
        # writing to the data base
        alreadyExisting = []
        for i in db["players"].find({"id": playerDict['id']}, { "_id": 0}):
            alreadyExisting.append(i)
        if len(alreadyExisting) > 0:
            if alreadyExisting[0] != playerDict:
                documentsChange['updates'] = documentsChange['updates'] + 1
                db['players'].delete_one(alreadyExisting[0])
                db['players'].insert(playerDict)
        else:
            documentsChange['inserts'] = documentsChange['inserts'] + 1
            db['players'].insert(playerDict)

    print('get player info ended')
    return documentsChange