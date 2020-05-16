# imports
import statsapi
import pandas as pd
import re
from pymongo import MongoClient
import datetime
import requests
import numbers

# Database Connection
client = MongoClient('localhost', 27017)
db = client['baseballmd']

# getting the Ids of all players and transforming them to a string
cursor = db.players.find({})
playerIDs = ""
for document in cursor:
    playerIDs = playerIDs + str(document['id']) + ","
playerIDs

# relevant leagues ['AAA', 'AA', 'A(Adv)', 'A(Full)', 'ROK']
allSports = [{'abbreviation':'MLB','id':1},{'abbreviation':'AAA','id':11},{'abbreviation':'AA','id':12},{'abbreviation':'A(Adv)','id':13},{'abbreviation':'A(Full)','id':14},{'abbreviation':'ROK','id':16}]

# getting an arry of past seasons from now back to 2017
currentYear = int(datetime.datetime.today().year)
difference = currentYear - 2016
seasons = []
for i in range(0, difference):
    seasons.append(2017 + i)

def retrieveCareerData(rawData, sportAbbreviation):
    for player in rawData['people']:
        if 'stats' in player:
            for stat in player['stats']:
                for split in stat['splits']:
                    careerDict = {}
                    careerDict['id'] = player['id']
                    careerDict['fullName'] = player['fullName']
                    careerDict['type'] = stat['type']['displayName']
                    careerDict['statGroupe'] = stat['group']['displayName']
                    if 'season' in split:
                        if '.' in split['season']:
                            careerDict['season'] = int(split['season'][0:4])
                        else:
                            careerDict['season'] = int(split['season'])
                    else:
                        careerDict['season'] = 0
                    for seasonStat in split['stat']:
                        if stat['group']['displayName'] == 'fielding' and seasonStat == 'position':
                            careerDict[seasonStat] = split['stat'][seasonStat]['abbreviation']
                        else:
                            if isinstance(split['stat'][seasonStat], str) and re.search(r"\d{1}", split['stat'][seasonStat]):
                                careerDict[seasonStat] = float(split['stat'][seasonStat])
                            if split['stat'][seasonStat] == '-.--' or split['stat'][seasonStat]=='.---' or split['stat'][seasonStat]=='*.**':
                                careerDict[seasonStat] = ''
                            else:
                                careerDict[seasonStat] = split['stat'][seasonStat]
                    if 'team' in split and 'league' in split:
                        careerDict['team'] = split['team']['name']
                        careerDict['league'] = split['league']['name']
                    else:
                        careerDict['team'] = 'No Info'
                        careerDict['league'] = 'No Info'
                    careerDict['sport'] = sportAbbreviation
                    careerDict['gameType'] = split['gameType']

                    # calculating ISO
                    if careerDict['statGroupe'] == 'hitting' and isinstance(careerDict['slg'], numbers.Number) and isinstance(careerDict['avg'], numbers.Number):
                        careerDict['ISO'] = round(careerDict['slg'] - careerDict['avg'], 3)

                    # cleaning stats which always cause anwanted update behavior
                    if careerDict['statGroupe']=='pitching' and 'slg' in careerDict and 'ops' in careerDict:
                        careerDict['slg'] = 0
                        careerDict['ops'] = 0
                    if ('groundOuts' in careerDict and 'airOuts' in careerDict) and (careerDict['groundOuts'] == 0 or careerDict['airOuts'] == 0):
                        careerDict['groundOutsToAirouts'] = ''

                    careerDict.pop('_id', None)
                    # writing to database    
                    alreadyExisting = []
                    if careerDict['statGroupe'] == 'fielding':
                        for i in db["careerStats"].find({"id": careerDict['id'], "type" : careerDict['type'], "statGroupe" : careerDict['statGroupe'], 'season':careerDict['season'], "sport": careerDict['sport'], "position": careerDict['position'], "team": careerDict['team'], "league": careerDict['league'], "gameType": careerDict['gameType'], }, { "_id": 0}):
                            alreadyExisting.append(i)
                    else:
                        for i in db["careerStats"].find({"id": careerDict['id'], "type" : careerDict['type'], "statGroupe" : careerDict['statGroupe'], 'season':careerDict['season'], "sport": careerDict['sport'], "team": careerDict['team'], "league": careerDict['league'], "gameType": careerDict['gameType'], }, { "_id": 0}):
                            alreadyExisting.append(i)
                    if len(alreadyExisting) > 0:
                        if alreadyExisting[0] != careerDict:
                            db['careerStats'].delete_one(alreadyExisting[0])
                            db['careerStats'].insert_one(careerDict)
                    else:
                        # print('Inserting YearByYear')
                        db['careerStats'].insert_one(careerDict)



def retrieveSplitsData(rawData, sportAbbreviation):
    for player in rawData['people']:
        if 'stats' in player:
            for stat in player['stats']:
                if 'splits' in stat:
                    for split in stat['splits']:
                        splitsDict = {}
                        if 'split' in split:
                            splitsDict['split'] = split['split']['description']
                        else:
                            splitsDict['split'] = 'No Info'
                        splitsDict['id'] = player['id']
                        splitsDict['fullName'] = player['fullName']
                        splitsDict['type'] = stat['type']['displayName']
                        splitsDict['statGroupe'] = stat['group']['displayName']
                        splitsDict['season'] = int(split['season'])
                        if 'team' in split:
                            splitsDict['team'] = split['team']['name']
                        else: 
                            splitsDict['team'] = 'No Info'
                        splitsDict['gameType'] = split['gameType']
                        splitsDict['sport'] = sportAbbreviation
                        for splitsSplitStat in split['stat']:
                            if isinstance(split['stat'][splitsSplitStat], str) and re.search(r"\d{1}", split['stat'][splitsSplitStat]):
                                splitsDict[splitsSplitStat] = float(split['stat'][splitsSplitStat])
                            else:
                                splitsDict[splitsSplitStat] = split['stat'][splitsSplitStat]
                        splitsDict.pop('_id', None)
                        
                        # writing to the database
                        alreadyExisting = []
                        for i in db["splitStats"].find({"id": splitsDict['id'], "type" : splitsDict['type'], "statGroupe" : splitsDict['statGroupe'], "sport": splitsDict['sport'], "split": splitsDict['split'], "season": splitsDict['season'],"team": splitsDict['team'],"gameType": splitsDict['gameType'],}, { "_id": 0}):
                            alreadyExisting.append(i)
                        if len(alreadyExisting) > 0:
                            if alreadyExisting[0] != splitsDict:
                                db['splitStats'].delete_one(alreadyExisting[0])
                                db['splitStats'].insert_one(splitsDict)
                        else:
                            # print('Inserting Splits')
                            db['splitStats'].insert_one(splitsDict)


# retirving all data and storing it
for sport in allSports:
    sportId = sport['id']
    sportAbbreviation = sport['abbreviation']
    print(sportAbbreviation, sportId)

    # https://statsapi.mlb.com/api/v1/people?personIds=642720&hydrate=stats(group=[hitting,fielding,pitching],type=[yearByYear],sportId=16)
    # retrieving career data (type yearByYear)
    careerYearByYearParams = {'personIds': playerIDs,'hydrate': 'stats(group=[hitting,fielding,pitching],type=[yearByYear],sportId={})'.format(sportId)}
    careerYearByYearStats = statsapi.get('people', careerYearByYearParams)
    retrieveCareerData(careerYearByYearStats, sportAbbreviation)

    # https://statsapi.mlb.com/api/v1/people?personIds=642720&hydrate=stats(group=[hitting,fielding,pitching],type=[career],sportId=13)
    # retrieving career data (type career)
    careerCareerParams = {'personIds': playerIDs,'hydrate': 'stats(group=[hitting,fielding,pitching],type=[career],sportId={})'.format(sportId)}
    careerCareerStats = statsapi.get('people', careerCareerParams)
    retrieveCareerData(careerCareerStats, sportAbbreviation)

    # retriving splits data
    for season in seasons:
        # https://statsapi.mlb.com/api/v1/people?personIds=642720&hydrate=stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc],season=2019,sportId=12)
        # retrieving splits data (type: statSplits)
        splitsStatSplitsParams = {'personIds': playerIDs,'hydrate': 'stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc],season={},sportId={})'.format(season,sportId)}
        splitsStatSplitsStats = statsapi.get('people', splitsStatSplitsParams)
        retrieveSplitsData(splitsStatSplitsStats, sportAbbreviation)


        # https://statsapi.mlb.com/api/v1/people?personIds=642720&hydrate=stats(type=[season],season=2019,sportId=12)
        # retrieving splits data (type: season)
        splitsSeasonParams = {'personIds': playerIDs,'hydrate': 'stats(type=[season],season={},sportId={})'.format(season,sportId)}
        splitsSeasonStats = statsapi.get('people', splitsSeasonParams)
        retrieveSplitsData(splitsSeasonStats, sportAbbreviation)
