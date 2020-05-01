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

# getting all sportIds
r = requests.get('http://statsapi.mlb.com/api/v1/sports/').json()
allSports = []
for sport in r['sports']:
    sportAndId = {}
    sportAndId['abbreviation'] = sport['abbreviation']
    sportAndId['id'] = sport['id']
    allSports.append(sportAndId)

# getting an arry of past seasons from now back to 2017
currentYear = int(datetime.datetime.today().year)
difference = currentYear - 2016
seasons = []
for i in range(0, difference):
    seasons.append(2017 + i)

# retirving all data and storing it
for sport in allSports:
    sportId = sport['id']
    sportAbbreviation = sport['abbreviation']
    #print(sportAbbreviation, sportId)

    # https://statsapi.mlb.com/api/v1/people?personIds=642720&hydrate=stats(group=[hitting,fielding,pitching],type=[yearByYear],sportId=16)
    # retrieving career data (type yearByYear)
    careerYearByYearParams = {'personIds': playerIDs,'hydrate': 'stats(group=[hitting,fielding,pitching],type=[yearByYear],sportId={})'.format(sportId)}
    careerYearByYearStats = statsapi.get('people', careerYearByYearParams)

    for player in careerYearByYearStats['people']:
        try:
            careerYearByYearDict = {}
            careerYearByYearDict['fullName'] = player['fullName']
            careerYearByYearDict['id'] = player['id']
            for stat in player['stats']:
                try:
                    careerYearByYearDict['type'] = stat['type']['displayName']
                    careerYearByYearDict['statGroupe'] = stat['group']['displayName']
                    for split in stat['splits']:
                        try:
                            try:
                                careerYearByYearDict['season'] = int(split['season'])
                            except ValueError:
                                careerYearByYearDict['season'] = split['season']
                                continue
                            for seasonStat in split['stat']:
                                try:
                                    if stat['group']['displayName'] == 'fielding' and seasonStat == 'position':
                                        careerYearByYearDict[seasonStat] = split['stat'][seasonStat]['abbreviation']
                                    else:
                                        if isinstance(split['stat'][seasonStat], str) and re.search(r"\d{1}", split['stat'][seasonStat]):
                                            careerYearByYearDict[seasonStat] = float(split['stat'][seasonStat])
                                        else:
                                            careerYearByYearDict[seasonStat] = split['stat'][seasonStat]
                                except KeyError:
                                    continue
                            careerYearByYearDict['team'] = split['team']['name']
                            careerYearByYearDict['league'] = split['league']['name']
                            careerYearByYearDict['sport'] = sportAbbreviation
                            careerYearByYearDict['gameType'] = split['gameType']

                            if careerYearByYearDict['statGroupe'] == 'hitting' and isinstance(careerYearByYearDict['slg'], numbers.Number) and isinstance(careerYearByYearDict['avg'], numbers.Number):
                                careerYearByYearDict['ISO'] = round(careerYearByYearDict['slg'] - careerYearByYearDict['avg'], 3)

                            careerYearByYearDict.pop('_id', None)
                            # writing to database    
                            alreadyExisting = []
                            if careerYearByYearDict['statGroupe'] == 'fielding':
                                for i in db["careerStats"].find({"id": careerYearByYearDict['id'], "type" : careerYearByYearDict['type'], "statGroupe" : careerYearByYearDict['statGroupe'], 'season':careerYearByYearDict['season'], "sport": careerYearByYearDict['sport'], "position": careerYearByYearDict['position'], "team": careerYearByYearDict['team'], "league": careerYearByYearDict['league'], "gameType": careerYearByYearDict['gameType'], }, { "_id": 0}):
                                    alreadyExisting.append(i)
                            else:
                                for i in db["careerStats"].find({"id": careerYearByYearDict['id'], "type" : careerYearByYearDict['type'], "statGroupe" : careerYearByYearDict['statGroupe'], 'season':careerYearByYearDict['season'], "sport": careerYearByYearDict['sport'], "team": careerYearByYearDict['team'], "league": careerYearByYearDict['league'], "gameType": careerYearByYearDict['gameType'], }, { "_id": 0}):
                                    alreadyExisting.append(i)
                            if len(alreadyExisting) > 0:
                                if alreadyExisting[0] != careerYearByYearDict:
                                    db['careerStats'].delete_one(alreadyExisting[0])
                                    db['careerStats'].insert(careerYearByYearDict)
                            else:
                                print('Inserting YearByYear')
                                db['careerStats'].insert(careerYearByYearDict)
                        except KeyError:
                            continue
                except KeyError:
                    continue
        except KeyError:
            continue

    # https://statsapi.mlb.com/api/v1/people?personIds=642720&hydrate=stats(group=[hitting,fielding,pitching],type=[career],sportId=13)
    # retrieving career data (type career)
    careerCareerParams = {'personIds': playerIDs,'hydrate': 'stats(group=[hitting,fielding,pitching],type=[career],sportId={})'.format(sportId)}
    careerCareerStats = statsapi.get('people', careerCareerParams)

    for player in careerCareerStats['people']:
        try:
            for stat in player['stats']:
                try:
                    careerCareerDict = {}
                    careerCareerDict['fullName'] = player['fullName']
                    careerCareerDict['id'] = player['id']
                    careerCareerDict['type'] = stat['type']['displayName']
                    careerCareerDict['statGroupe'] = stat['group']['displayName']
                    for split in stat['splits']:
                        try:
                            for careerCareerStat in split['stat']:
                                try:
                                    if stat['group']['displayName'] == 'fielding' and careerCareerStat == 'position':
                                        careerCareerDict[careerCareerStat] = split['stat'][careerCareerStat]['abbreviation']
                                    else:
                                        if isinstance(split['stat'][careerCareerStat], str) and re.search(r"\d{1}", split['stat'][careerCareerStat]):
                                            careerCareerDict[careerCareerStat] = float(split['stat'][careerCareerStat])
                                        else:
                                            careerCareerDict[careerCareerStat] = split['stat'][careerCareerStat]
                                except KeyError:
                                    continue
                            careerCareerDict['sport'] = sportAbbreviation
                            careerCareerDict['gameType'] = split['gameType']

                            if careerCareerDict['statGroupe'] == 'hitting' and isinstance(careerCareerDict['slg'], numbers.Number) and isinstance(careerCareerDict['avg'], numbers.Number):
                                careerCareerDict['ISO'] = round(careerCareerDict['slg'] - careerCareerDict['avg'], 3)

                            careerCareerDict.pop('_id', None)
                            # writing to the database
                            alreadyExisting = []
                            if careerCareerDict['statGroupe'] == 'fielding':
                                for i in db["careerStats"].find({"id": careerCareerDict['id'], "type" : careerCareerDict['type'], "statGroupe" : careerCareerDict['statGroupe'], "sport": careerCareerDict['sport'], "gameType": careerCareerDict['gameType'], "position": careerCareerDict['position']}, { "_id": 0}):
                                    alreadyExisting.append(i)
                            else:
                                for i in db["careerStats"].find({"id": careerCareerDict['id'], "type" : careerCareerDict['type'], "statGroupe" : careerCareerDict['statGroupe'], "sport": careerCareerDict['sport'], "gameType": careerCareerDict['gameType']}, { "_id": 0}):
                                    alreadyExisting.append(i)
                            if len(alreadyExisting) > 0:
                                if alreadyExisting[0] != careerCareerDict:
                                    db['careerStats'].delete_one(alreadyExisting[0])
                                    db['careerStats'].insert(careerCareerDict)
                            else:
                                print('Inserting YearByYear')
                                db['careerStats'].insert(careerCareerDict)
                        except KeyError:
                            continue
                except KeyError:
                    continue
        except KeyError:
            continue

    # retriving splits data
    for season in seasons:
        # https://statsapi.mlb.com/api/v1/people?personIds=642720&hydrate=stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc],season=2019,sportId=12)
        # retrieving splits data (type: statSplits)
        splitsStatSplitsParams = {'personIds': playerIDs,'hydrate': 'stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc],season={},sportId={})'.format(season,sportId)}
        splitsStatSplitsStats = statsapi.get('people', splitsStatSplitsParams)

        for player in splitsStatSplitsStats['people']:
            try:
                for stat in player['stats']:
                    try:
                        splitsStatSplitsDict = {}
                        splitsStatSplitsDict['fullName'] = player['fullName']
                        splitsStatSplitsDict['id'] = player['id']
                        splitsStatSplitsDict['type'] = stat['type']['displayName']
                        splitsStatSplitsDict['statGroupe'] = stat['group']['displayName']
                        for split in stat['splits']:
                            try:
                                try:
                                    splitsStatSplitsDict['season'] = int(split['season'])
                                except ValueError:
                                    splitsStatSplitsDict['season'] = split['season']
                                    continue
                                splitsStatSplitsDict['split'] = split['split']['description']
                                splitsStatSplitsDict['team'] = split['team']['name']
                                splitsStatSplitsDict['gameType'] = split['gameType']
                                splitsStatSplitsDict['sport'] = sportAbbreviation
                                for splitsSplitStat in split['stat']:
                                    try:
                                        if isinstance(split['stat'][splitsSplitStat], str) and re.search(r"\d{1}", split['stat'][splitsSplitStat]):
                                            splitsStatSplitsDict[splitsSplitStat] = float(split['stat'][splitsSplitStat])
                                        else:
                                            splitsStatSplitsDict[splitsSplitStat] = split['stat'][splitsSplitStat]
                                    except KeyError:
                                        continue
                                splitsStatSplitsDict.pop('_id', None)
                                
                                # writing to the database
                                alreadyExisting = []
                                for i in db["splitStats"].find({"id": splitsStatSplitsDict['id'], "type" : splitsStatSplitsDict['type'], "statGroupe" : splitsStatSplitsDict['statGroupe'], "sport": splitsStatSplitsDict['sport'], "split": splitsStatSplitsDict['split'], "season": splitsStatSplitsDict['season'],"team": splitsStatSplitsDict['team'],"gameType": splitsStatSplitsDict['gameType'],}, { "_id": 0}):
                                    alreadyExisting.append(i)
                                if len(alreadyExisting) > 0:
                                    if alreadyExisting[0] != splitsStatSplitsDict:
                                        db['splitStats'].delete_one(alreadyExisting[0])
                                        db['splitStats'].insert(splitsStatSplitsDict)
                                else:
                                    print('Inserting Splits')
                                    db['splitStats'].insert(splitsStatSplitsDict)
                            except KeyError:
                                continue
                    except KeyError:
                        continue
            except KeyError:
                continue

        # https://statsapi.mlb.com/api/v1/people?personIds=642720&hydrate=stats(type=[season],season=2019,sportId=12)
        # retrieving splits data (type: season)
        splitsSeasonParams = {'personIds': playerIDs,'hydrate': 'stats(type=[season],season={},,sportId={})'.format(season,sportId)}
        splitsSeasonStats = statsapi.get('people', splitsSeasonParams)

        for player in splitsSeasonStats['people']:
            try:
                for stat in player['stats']:
                    try:
                        splitsSeasonDict = {}
                        splitsSeasonDict['fullName'] = player['fullName']
                        splitsSeasonDict['id'] = player['id']
                        splitsSeasonDict['type'] = stat['type']['displayName']
                        splitsSeasonDict['statGroupe'] = stat['group']['displayName']
                        for split in stat['splits']:
                            try:
                                try:
                                    splitsSeasonDict['season'] = int(split['season'])
                                except ValueError:
                                    splitsSeasonDict['season'] = split['season']
                                    continue
                                splitsSeasonDict['team'] = split['team']['name']
                                splitsSeasonDict['league'] = split['league']['name']
                                splitsSeasonDict['gameType'] = split['gameType']
                                splitsStatSplitsDict['sport'] = sportAbbreviation
                                for splitsSeasonStat in split['stat']:
                                    try:
                                        if isinstance(split['stat'][splitsSeasonStat], str) and re.search(r"\d{1}", split['stat'][splitsSeasonStat]):
                                            splitsSeasonDict[splitsSeasonStat] = float(split['stat'][splitsSeasonStat])
                                        else:
                                            splitsSeasonDict[splitsSeasonStat] = split['stat'][splitsSeasonStat]
                                    except KeyError:
                                        continue
                                splitsSeasonDict.pop('_id', None)

                                # writing to the database
                                alreadyExisting = []
                                for i in db["splitStats"].find({"id": splitsSeasonDict['id'], "type" : splitsSeasonDict['type'], "statGroupe" : splitsSeasonDict['statGroupe'], "sport": splitsSeasonDict['sport'], "season": splitsSeasonDict['season'],"team": splitsSeasonDict['team'],"league": splitsSeasonDict['league'],"gameType": splitsSeasonDict['gameType'],}, { "_id": 0}):
                                    alreadyExisting.append(i)
                                if len(alreadyExisting) > 0:
                                    if alreadyExisting[0] != splitsSeasonDict:
                                        db['splitStats'].delete_one(alreadyExisting[0])
                                        db['splitStats'].insert(splitsSeasonDict)
                                else:
                                    print('Inserting Splits')
                                    db['splitStats'].insert(splitsSeasonDict)
                            except KeyError:
                                continue
                    except KeyError:
                        continue
            except KeyError:
                continue

