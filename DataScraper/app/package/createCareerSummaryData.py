# imports
import numbers
import statistics
import pandas as pd
from pymongo import MongoClient
from app.config import getDB

client = getDB()
db = client['baseballmd']
careerStats = db.careerStats

documentsChange = {"inserts":0,"updates":0}

def getCareerSummaryData():
    print('get career Summary started')
    # getting the Ids of all players and transforming them to a string
    cursor = db.players.find({})
    playerIDs = []
    for document in cursor:
        playerIDs.append((document['id']))

    listOfRelevantLeagues = ['AAA', 'AA', 'A(Adv)', 'A(Full)', 'ROK']

    # summerizing career hitting stats
    rawData = pd.DataFrame(list(careerStats.find({"type" : "career", "statGroupe" : "hitting"}, { "_id": 0})))
    rawData = rawData.fillna(0)

    countValues = ['gamesPlayed', 'atBats', 'runs', 'hits', 'totalBases', 'doubles', 'triples' , 'homeRuns', 'rbi', 'baseOnBalls', 'intentionalWalks', 'strikeOuts', 'stolenBases', 'caughtStealing', 'hitByPitch', 'groundIntoDoublePlay', 'numberOfPitches', 'plateAppearances', 'leftOnBase', 'sacBunts', 'sacFlies']
    averageValues = ['avg', 'obp', 'slg', 'ops', 'groundOutsToAirouts', 'stolenBasePercentage', 'babip', 'atBatsPerHomeRun', 'ISO']

    for playerId in playerIDs:
        playerDocuments = rawData.loc[lambda df: df['id'] == playerId]
        if 'MLB' in playerDocuments['sport'].unique():
            mlbRow = playerDocuments.loc[playerDocuments['sport'] == 'MLB']
            mlb = mlbRow.to_dict(orient='records')
            mlbDict = mlb[0]
            mlbDict['type'] = 'MLB Career'
            mlbDict.pop('_id', None)

            # writing to the database /checking if updating, inserting or going to next document
            alreadyExisting = []
            for i in db["careerTable"].find({"id": mlbDict['id'], "type": mlbDict['type'],"statGroupe": mlbDict['statGroupe'], "sport": mlbDict['sport']}, { "_id": 0}):
                alreadyExisting.append(i)
            if len(alreadyExisting) > 0:
                if alreadyExisting[0] != mlbDict:
                    documentsChange['updates'] = documentsChange['updates'] + 1
                    db['careerTable'].delete_one(alreadyExisting[0])
                    db['careerTable'].insert_one(mlbDict)
            else:
                documentsChange['inserts'] = documentsChange['inserts'] + 1
                db['careerTable'].insert_one(mlbDict)
        else:
            intermediateResults = pd.DataFrame()
            calculatedRow = {}
            for league in listOfRelevantLeagues:
                onlyRelevantLeague = playerDocuments.loc[playerDocuments['sport'] == league]
                intermediateResults = intermediateResults.append(onlyRelevantLeague)
            if len(intermediateResults.index) > 0:
                for column in intermediateResults.columns:
                    if column == 'id':
                        calculatedRow[column] = int(intermediateResults[column].iloc[0])
                    if column == 'fullName':
                        calculatedRow[column] = str(intermediateResults[column].iloc[0])
                    if column == 'statGroupe':
                        calculatedRow[column] = str(intermediateResults[column].iloc[0])
                    if column == 'sport':
                        calculatedRow[column] = 'MiLB'
                    if column == 'type':
                        calculatedRow[column] = 'MiLB Career'
                    if column in countValues:
                        sumValues = []
                        for value in intermediateResults[column]:
                            if isinstance(value, numbers.Number):
                                sumValues.append(value)
                        if len(sumValues) > 0:
                            columnSum = sum(sumValues)
                            calculatedRow[column] = int(columnSum)

                    if column in averageValues:
                        meanValues = []
                        for value in intermediateResults[column]:
                            if isinstance(value, numbers.Number):
                                meanValues.append(value)
                        if len(meanValues) > 0:
                            columnMean = round(statistics.mean(meanValues), 3)
                            calculatedRow[column] = float(columnMean)
                calculatedRow.pop('_id', None)

                # writing to the database /checking if updating, inserting or going to next document
                alreadyExisting = []
                for i in db["careerTable"].find({"id": calculatedRow['id'], "type": calculatedRow['type'],"statGroupe": calculatedRow['statGroupe'], "sport": calculatedRow['sport']}, { "_id": 0}):
                    alreadyExisting.append(i)
                if len(alreadyExisting) > 0:
                    if alreadyExisting[0] != calculatedRow:
                        documentsChange['updates'] = documentsChange['updates'] + 1
                        db['careerTable'].delete_one(alreadyExisting[0])
                        db['careerTable'].insert_one(calculatedRow)
                else:
                    documentsChange['inserts'] = documentsChange['inserts'] + 1
                    db['careerTable'].insert_one(calculatedRow)


    #summerizing career filding stats
    rawData = pd.DataFrame(list(careerStats.find({"type" : "career", "statGroupe" : "fielding"}, { "_id": 0})))
    rawData = rawData.fillna(0)

    countValues = ['games', 'gamesStarted', 'innings', 'chances', 'putOuts', 'assists', 'errors', 'doublePlays']
    averageValues = ['rangeFactorPerGame', 'fielding']

    for playerId in playerIDs:
        playerDocuments = rawData.loc[lambda df: df['id'] == playerId]
        if 'MLB' in playerDocuments['sport'].unique():
            mlbRow = playerDocuments.loc[playerDocuments['sport'] == 'MLB']
            mlb = mlbRow.to_dict(orient='records')
            mlbDict = mlb[0]
            mlbDict['type'] = 'MLB Career'
            mlbDict.pop('_id', None)

            # writing to the database /checking if updating, inserting or going to next document
            alreadyExisting = []
            for i in db["careerTable"].find({"id": mlbDict['id'], "type": mlbDict['type'],"statGroupe": mlbDict['statGroupe'], "sport": mlbDict['sport'], "position": mlbDict['position']}, { "_id": 0}):
                alreadyExisting.append(i)
            if len(alreadyExisting) > 0:
                if alreadyExisting[0] != mlbDict:
                    documentsChange['updates'] = documentsChange['updates'] + 1
                    db['careerTable'].delete_one(alreadyExisting[0])
                    db['careerTable'].insert_one(mlbDict)
            else:
                documentsChange['inserts'] = documentsChange['inserts'] + 1
                db['careerTable'].insert_one(mlbDict)
        else:
            intermediateResults = pd.DataFrame()
            for league in listOfRelevantLeagues:
                onlyRelevantLeague = playerDocuments.loc[playerDocuments['sport'] == league]
                intermediateResults = intermediateResults.append(onlyRelevantLeague)
            if len(intermediateResults.index) > 0:
                groupedPos = list()
                for position in intermediateResults['position'].unique():
                    posResults = pd.DataFrame()
                    oneEntry = intermediateResults.loc[intermediateResults['position'] == position]
                    posResults = posResults.append(oneEntry)
                    groupedPos.append(posResults)
                for item in groupedPos:
                    calculatedRow = {}
                    for column in item.columns:
                        if column == 'id':
                            calculatedRow[column] = int(item[column].iloc[0])
                        if column == 'fullName':
                            calculatedRow[column] = str(item[column].iloc[0])
                        if column == 'statGroupe':
                            calculatedRow[column] = str(item[column].iloc[0])
                        if column == 'sport':
                            calculatedRow[column] = 'MiLB'
                        if column == 'type':
                            calculatedRow[column] = 'MiLB Career'
                        if column == 'position':
                            calculatedRow[column] = str(item[column].iloc[0])
                        if column in countValues:
                            sumValues = []
                            for value in item[column]:
                                if isinstance(value, numbers.Number):
                                    sumValues.append(value)
                            if len(sumValues) > 0:
                                columnSum = sum(sumValues)
                                calculatedRow[column] = int(columnSum)
                        if column in averageValues:
                            meanValues = []
                            for value in item[column]:
                                if isinstance(value, numbers.Number):
                                    meanValues.append(value)
                            if len(meanValues) > 0:
                                columnMean = round(statistics.mean(meanValues), 3)
                                calculatedRow[column] = float(columnMean)
                    calculatedRow.pop('_id', None)

                    # writing to the data base
                    alreadyExisting = []
                    for i in db["careerTable"].find({"id": calculatedRow['id'], "type": calculatedRow['type'],"statGroupe": calculatedRow['statGroupe'], "sport": calculatedRow['sport'], "position": calculatedRow['position']}, { "_id": 0}):
                        alreadyExisting.append(i)
                    if len(alreadyExisting) > 0:
                        if alreadyExisting[0] != calculatedRow:
                            documentsChange['updates'] = documentsChange['updates'] + 1
                            db['careerTable'].delete_one(alreadyExisting[0])
                            db['careerTable'].insert_one(calculatedRow)
                    else:
                        documentsChange['inserts'] = documentsChange['inserts'] + 1
                        db['careerTable'].insert_one(calculatedRow)


    #summerizing career pitching stats
    rawData = pd.DataFrame(list(careerStats.find({"type" : "career", "statGroupe" : "pitching"}, { "_id": 0})))
    rawData = rawData.fillna(0)

    countValues = ['wins', 'losses', 'gamesPlayed', 'gamesStarted', 'completeGames', 'shutouts', 'saves', 'saveOpportunities', 'inningsPitched', 'hits', 'runs', 'earnedRuns', 'homeRuns', 'hitBatsmen', 'baseOnBalls', 'intentionalWalks', 'strikeOuts',]
    averageValues = ['era', 'avg', 'whip', 'groundOutsToAirouts']

    for playerId in playerIDs:
        playerDocuments = rawData.loc[lambda df: df['id'] == playerId]
        if 'MLB' in playerDocuments['sport'].unique():
            mlbRow = playerDocuments.loc[playerDocuments['sport'] == 'MLB']
            mlb = mlbRow.to_dict(orient='records')
            mlbDict = mlb[0]
            mlbDict['type'] = 'MLB Career'
            mlbDict.pop('_id', None)

            # writing to the database / checking if updating, inserting or going to next document
            alreadyExisting = []
            for i in db["careerTable"].find({"id": mlbDict['id'], "type": mlbDict['type'],"statGroupe": mlbDict['statGroupe'], "sport": mlbDict['sport']}, { "_id": 0}):
                alreadyExisting.append(i)
            if len(alreadyExisting) > 0:
                if alreadyExisting[0] != mlbDict:
                    documentsChange['updates'] = documentsChange['updates'] + 1
                    db['careerTable'].delete_one(alreadyExisting[0])
                    db['careerTable'].insert_one(mlbDict)
            else:
                documentsChange['inserts'] = documentsChange['inserts'] + 1
                db['careerTable'].insert_one(mlbDict)
        else:
            intermediateResults = pd.DataFrame()
            calculatedRow = {}
            for league in listOfRelevantLeagues:
                onlyRelevantLeague = playerDocuments.loc[playerDocuments['sport'] == league]
                intermediateResults = intermediateResults.append(onlyRelevantLeague)
            if len(intermediateResults.index) > 0:
                for column in intermediateResults.columns:
                    if column == 'id':
                        calculatedRow[column] = int(intermediateResults[column].iloc[0])
                    if column == 'fullName':
                        calculatedRow[column] = str(intermediateResults[column].iloc[0])
                    if column == 'statGroupe':
                        calculatedRow[column] = str(intermediateResults[column].iloc[0])
                    if column == 'sport':
                        calculatedRow[column] = 'MiLB'
                    if column == 'type':
                        calculatedRow[column] = 'MiLB Career'
                    if column in countValues:
                        sumValues = []
                        for value in intermediateResults[column]:
                            if isinstance(value, numbers.Number):
                                sumValues.append(value)
                        if len(sumValues) > 0:
                            columnSum = sum(sumValues)
                            calculatedRow[column] = int(columnSum)

                    if column in averageValues:
                        meanValues = []
                        for value in intermediateResults[column]:
                            if isinstance(value, numbers.Number):
                                meanValues.append(value)
                        if len(meanValues) > 0:
                            columnMean = round(statistics.mean(meanValues), 3)
                            calculatedRow[column] = float(columnMean)
                calculatedRow.pop('_id', None)

                # writing to the data base / checking if updating, inserting or going to next document
                alreadyExisting = []
                for i in db["careerTable"].find({"id": calculatedRow['id'], "type": calculatedRow['type'],"statGroupe": calculatedRow['statGroupe'], "sport": calculatedRow['sport']}, { "_id": 0}):
                    alreadyExisting.append(i)
                if len(alreadyExisting) > 0:
                    if alreadyExisting[0] != calculatedRow:
                        documentsChange['updates'] = documentsChange['updates'] + 1
                        db['careerTable'].delete_one(alreadyExisting[0])
                        db['careerTable'].insert_one(calculatedRow)
                else:
                    documentsChange['inserts'] = documentsChange['inserts'] + 1
                    db['careerTable'].insert_one(calculatedRow)

    print('get career Summary ended')
    return documentsChange

