# imports
import numbers
import statistics
import pandas as pd
from pymongo import MongoClient

client = MongoClient("localhost:27017")
db=client['baseballmd']

# getting the Ids of all players and transforming them to a string
cursor = db.players.find({})
playerIDs = []
for document in cursor:
    playerIDs.append((document['id']))


careerStats = db.careerStats
rawData = pd.DataFrame(list(careerStats.find({"type" : "career", "statGroupe" : "hitting"}, { "_id": 0})))


listOfRelevantLeagues = ['AAA', 'AA', 'A(Adv)', 'A(Full)', 'ROK']
countValues = ['gamesPlayed', 'groundOuts','airOuts','runs', 'doubles', 'triples' , 'homeRuns' , 'strikeOuts' , 'baseOnBalls','intentionalWalks', 'hits', 'hitByPitch', 'atBats', 'caughtStealing', 'stolenBases', 'groundIntoDoublePlay', 'numberOfPitches', 'plateAppearances', 'totalBases', 'rbi', 'leftOnBase', 'sacBunts', 'sacFlies']
averageValues = ['avg', 'obp', 'slg', 'ops', 'stolenBasePercentage', 'babip', 'groundOutsToAirouts', 'atBatsPerHomeRun']


allresults = []
for playerId in playerIDs:
    print(playerId)
    playerDocuments = rawData.loc[lambda df: df['id'] == playerId]
    if 'MLB' in playerDocuments['sport'].unique():
        mlbRow = playerDocuments.loc[playerDocuments['sport'] == 'MLB']
        mlb = mlbRow.to_dict(orient='records')
        mlbDict = mlb[0]
        mlbDict['type'] = 'MLB Career'
        mlbDict.pop('_id', None)
        allresults.append(mlbDict)
        #db['careerTable'].insert(mlbDict)
        print('Yei')
    else:
        print('nei')
        intermediateResults = pd.DataFrame()
        calculatedRow = {}
        for league in listOfRelevantLeagues:
            onlyRelevantLeague = playerDocuments.loc[playerDocuments['sport'] == league]
            intermediateResults = intermediateResults.append(onlyRelevantLeague)
        print(len(intermediateResults.index))
        for column in intermediateResults.columns:
            if column in countValues:
                sumValues = []
                for value in intermediateResults[column]:
                    if isinstance(value, numbers.Number):
                        sumValues.append(value)
                if len(sumValues) > 0:
                    columnSum = sum(sumValues)
                    calculatedRow[column] = float(columnSum)

            if column in averageValues:
                meanValues = []
                for value in intermediateResults[column]:
                    if isinstance(value, numbers.Number):
                        meanValues.append(value)
                if len(meanValues) > 0:
                    columnMean = round(statistics.mean(meanValues), 3)
                    calculatedRow[column] = float(columnMean)
            if column == 'sport':
                calculatedRow[column] = 'MiLB'
            if column == 'type':
                calculatedRow[column] = 'MiLB Career'
            if column == 'id':
                calculatedRow[column] = int(intermediateResults[column].iloc[0])
            else:
                calculatedRow[column] = intermediateResults[column].iloc[0]
        calculatedRow.pop('_id', None)
        allresults.append(calculatedRow)

        #db['careerTable'].insert(calculatedRow)


len(allresults)

intermediateResults['fullName']