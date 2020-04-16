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

# Database Connection
client = MongoClient('localhost', 27017)
db = client['baseballmd']
collection = db['careerStats']

# getting Names and IDs of the player (For now only a sample dataframe, later this will come from the database)
players = pd.DataFrame(data={'Name': [
                       'Ozzie Albies', 'Xander Bogaerts', 'Didi Gregorius'], 'ID': [645277, 593428, 544369]})
players


# transforming the IDs to a comma seperated string in order to serve as a parameter later on
playerIDs = ""
for playerID in players['ID']:
    playerIDs = playerIDs + str(playerID) + ","
playerIDs

# https://statsapi.mlb.com/api/v1/people?personIds=645277,593428,544369&hydrate=stats(group=[hitting,fielding,pitching],type=[yearByYear])
# retrieving career data (Year by Year)
careerParams = {'personIds': playerIDs,'hydrate': 'stats(group=[hitting,fielding,pitching],type=[yearByYear])'}
careerStats = statsapi.get('people', careerParams)
careerStats

for player in careerStats['people']:
    careerDict = {}
    careerDict['fullName'] = player['fullName']
    careerDict['Id'] = player['id']
    for stat in player['stats']:
        careerDict['statGroupe'] = stat['group']['displayName']
        for split in stat['splits']:
            careerDict['season'] = int(split['season'])
            for seasonStat in split['stat']:
                if stat['group']['displayName'] == 'fielding' and seasonStat == 'position':
                   careerDict[seasonStat] = split['stat'][seasonStat]['abbreviation']
                else:
                    if isinstance(split['stat'][seasonStat], str) and re.search(r"\d{1}", split['stat'][seasonStat]):
                        fStat = float(split['stat'][seasonStat])
                        careerDict[seasonStat] = fStat
                    else:
                        careerDict[seasonStat] = split['stat'][seasonStat]
            careerDict['team'] = split['team']['name']
            careerDict['league'] = split['league']['name']
            careerDict['sport'] = split['sport']['abbreviation']
            careerDict['gameType'] = split['gameType']
            careerDict.pop('_id', None)
            collection.insert(careerDict)

# https://statsapi.mlb.com/api/v1/people?personIds=645277,593428,544369&hydrate=stats(group=[hitting,fielding,pitching],type=[career])
# retrieving career data (summary)
careerSummaryParams = {'personIds': playerIDs,'hydrate': 'stats(group=[hitting,fielding,pitching],type=[career])'}
careerSummaryStats = statsapi.get('people', careerSummaryParams)
careerSummaryStats

counter = 0
for player in careerSummaryStats['people']:
    careerSummaryDict = {}
    careerSummaryDict['fullName'] = player['fullName']
    careerSummaryDict['Id'] = player['id']
    for stat in player['stats']:
        careerSummaryDict['statGroupe'] = stat['type']['displayName']
        for split in stat['splits']:
            for careerSummaryStat in split['stat']:
# WTF?








                if stat['group']['displayName'] == 'fielding' and seasonStat == 'position':
                   careerDict[seasonStat] = split['stat'][seasonStat]['abbreviation']
                else:
                    if isinstance(split['stat'][seasonStat], str) and re.search(r"\d{1}", split['stat'][seasonStat]):
                        fStat = float(split['stat'][seasonStat])
                        careerDict[seasonStat] = fStat
                    else:
                        careerDict[seasonStat] = split['stat'][seasonStat]
            careerDict['team'] = split['team']['name']
            careerDict['league'] = split['league']['name']
            careerDict['sport'] = split['sport']['abbreviation']
            careerDict['gameType'] = split['gameType']
            careerDict.pop('_id', None)
            #collection.insert(careerDict)
            counter += 1
            print(counter)
