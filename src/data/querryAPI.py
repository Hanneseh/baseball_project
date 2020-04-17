###### Requests to get all data of one player (The requests work for multiple player IDs at the same time) ########

# CAREER DATA: all rows, except the summery rows for the "MLB Career" in hiting and fielding
# https://statsapi.mlb.com/api/v1/people?personIds=593428&hydrate=stats(group=[hitting,fielding,pitching],type=[yearByYear])

# CAREER DATA: the summery rows "MLB Career" in hitting and fielding: Remaining Question: How to get minor Carrer stats? Is it relevant?
# https://statsapi.mlb.com/api/v1/people?personIds=593428&hydrate=stats(group=[hitting,fielding,pitching],type=[career])

# SPLITS DATA: All the rows of the splits data table on the website, except the last row (Season summary) for one season
# https://statsapi.mlb.com/api/v1/people?personIds=593428&hydrate=stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc],season=2019)
# request must be repeated for all relevant seasons

# SPLITS DATA: Season summary row for one season
# https://statsapi.mlb.com/api/v1/people?personIds=593428&hydrate=stats(type=[season],season=2019)
# request must be repeated for all relevant seasons

###### Start of the algorithm to get all the data from the API in a database ########

# imports
import statsapi
import pandas as pd
import re
from pymongo import MongoClient
import datetime

# Database Connection
client = MongoClient('localhost', 27017)
db = client['baseballmd']

# getting the Ids of all players and transforming them to a string
cursor = db.players.find({})
playerIDs = ""
for document in cursor:
    playerIDs = playerIDs + str(document['id']) + ","
playerIDs

# https://statsapi.mlb.com/api/v1/people?personIds=645277,593428,544369&hydrate=stats(group=[hitting,fielding,pitching],type=[yearByYear])
# retrieving career data (type yearByYear)
careerYearByYearParams = {'personIds': playerIDs,'hydrate': 'stats(group=[hitting,fielding,pitching],type=[yearByYear])'}
careerYearByYearStats = statsapi.get('people', careerYearByYearParams)

counter = 0
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
                        careerYearByYearDict['season'] = int(split['season'])
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
                        careerYearByYearDict['sport'] = split['sport']['abbreviation']
                        careerYearByYearDict['gameType'] = split['gameType']
                        careerYearByYearDict.pop('_id', None)
                        db['careerStats'].insert(careerYearByYearDict)
                        counter += 1
                    except KeyError:
                        continue
            except KeyError:
                continue
    except KeyError:
        continue
print(counter)

# https://statsapi.mlb.com/api/v1/people?personIds=645277,593428,544369&hydrate=stats(group=[hitting,fielding,pitching],type=[career])
# retrieving career data (type career)
careerCareerParams = {'personIds': playerIDs,'hydrate': 'stats(group=[hitting,fielding,pitching],type=[career])'}
careerCareerStats = statsapi.get('people', careerCareerParams)

counter = 0
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
                        careerCareerDict['sport'] = split['sport']['abbreviation']
                        careerCareerDict['gameType'] = split['gameType']
                        careerCareerDict.pop('_id', None)
                        db['careerStats'].insert(careerCareerDict)
                        counter += 1
                    except KeyError:
                        continue
            except KeyError:
                continue
    except KeyError:
        continue
print(counter)


# getting an arry of past seasons from now back to 2017
currentYear = int(datetime.datetime.today().year)
difference = currentYear - 2016
seasons = []
for i in range(0, difference):
    seasons.append(2017 + i)

for season in seasons:
    # https://statsapi.mlb.com/api/v1/people?personIds=645277,593428,544369&hydrate=stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc],season=2019)
    # retrieving splits data (type: statSplits)
    hydrateParamsStatSplits = 'stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc],season=' + str(season) + ')'
    splitsStatSplitsParams = {'personIds': playerIDs,'hydrate': hydrateParamsStatSplits}
    splitsStatSplitsStats = statsapi.get('people', splitsStatSplitsParams)

    counter = 0
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
                            splitsStatSplitsDict['season'] = int(split['season'])
                            splitsStatSplitsDict['split'] = split['split']['description']
                            splitsStatSplitsDict['team'] = split['team']['name']
                            splitsStatSplitsDict['gameType'] = split['gameType']
                            for splitsSplitStat in split['stat']:
                                try:
                                    if isinstance(split['stat'][splitsSplitStat], str) and re.search(r"\d{1}", split['stat'][splitsSplitStat]):
                                        splitsStatSplitsDict[splitsSplitStat] = float(split['stat'][splitsSplitStat])
                                    else:
                                        splitsStatSplitsDict[splitsSplitStat] = split['stat'][splitsSplitStat]
                                except KeyError:
                                    continue
                            splitsStatSplitsDict.pop('_id', None)
                            db['splitStats'].insert(splitsStatSplitsDict)
                            counter += 1
                        except KeyError:
                            continue
                except KeyError:
                    continue
        except KeyError:
            continue
    print(counter)

    # https://statsapi.mlb.com/api/v1/people?personIds=645277,593428,544369&hydrate=stats(type=[season],season=2020)
    # retrieving splits data (type: season)
    hydrateParamsSeason = 'stats(type=[season],season=' + str(season) + ')'
    splitsSeasonParams = {'personIds': playerIDs,'hydrate': hydrateParamsSeason}
    splitsSeasonStats = statsapi.get('people', splitsSeasonParams)

    counter = 0
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
                            splitsSeasonDict['season'] = int(split['season'])
                            splitsSeasonDict['team'] = split['team']['name']
                            splitsSeasonDict['league'] = split['league']['name']
                            splitsSeasonDict['gameType'] = split['gameType']
                            for splitsSeasonStat in split['stat']:
                                try:
                                    if isinstance(split['stat'][splitsSeasonStat], str) and re.search(r"\d{1}", split['stat'][splitsSeasonStat]):
                                        splitsSeasonDict[splitsSeasonStat] = float(split['stat'][splitsSeasonStat])
                                    else:
                                        splitsSeasonDict[splitsSeasonStat] = split['stat'][splitsSeasonStat]
                                except KeyError:
                                    continue
                            splitsSeasonDict.pop('_id', None)
                            db['splitStats'].insert(splitsSeasonDict)
                            counter += 1
                        except KeyError:
                            continue
                except KeyError:
                    continue
        except KeyError:
            continue
    print(counter)

