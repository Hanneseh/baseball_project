# imports
import pandas as pd
from pymongo import MongoClient

client = MongoClient("localhost:27017")
db=client['baseballmd']

# getting the Ids of all players and transforming them to a string
cursor = db.players.find({})
playerIDs = []
for document in cursor:
    playerIDs.append((document['id']))

{"type" : "career", "statGroupe" : "hitting", "id":642720}

# this goes in the function
collection = db.careerStats

rawData = pd.DataFrame(list(collection.find({"type" : "career", "statGroupe" : "hitting"}, { "_id": 0})))
rawData


listOfRelevantLeagues = ['AAA', 'AA', 'A(Adv)', 'A(Full)', 'ROK']

for playerId in playerIDs:
    resultDf = pd.DataFrame()
    playerDocuments = rawData.loc[lambda df: df['id'] == playerId]
    for sport in playerDocuments['sport']:
        if sport == 'MLB':
            foundIt = playerDocuments.loc[playerDocuments['sport'] == 'MLB']
            resultDf = resultDf.append(foundIt)
        else:
            intermediateResults = pd.DataFrame()
            for league in listOfRelevantLeagues:
                onlyRelevantLeagues = playerDocuments.loc[playerDocuments['sport'] == league]
                intermediateResults = intermediateResults.append(onlyRelevantLeagues)
            #print(intermediateResults)
            for column in intermediateResults.columns:
                intermediateResults.loc[intermediateResults[column]]
                rawPlayerData.loc[rawPlayerData['fullName']

                
                data['imageLink'].iloc[0])

                
                if isinstance(intermediateResults[column][0], object) and re.search(r"\d{.}", intermediateResults[column][0]):
                    print(column, intermediateResults[column][0])
                                        #     careerYearByYearDict[seasonStat] = float(split['stat'][seasonStat])
                                        # else:
                                        #     careerYearByYearDict[seasonStat] = split['stat'][seasonStat]
            #     intermediateResults[column][0]
            #     print(column, intermediateResults[column].dtypes)
            break
    break


resultDf

for player in rawData.iterrows():
    print('hello')
    print(player)
    #player['fullName']


a_row = pd.Series([1, 2])
df = pd.DataFrame([[3, 4], [5, 6]])

row_df = pd.DataFrame([a_row])
df = pd.concat([row_df, df], ignore_index=True)

rawPlayerData.loc[rawPlayerData['fullName']
