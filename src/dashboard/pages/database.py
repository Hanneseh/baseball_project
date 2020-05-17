# imports
import pandas as pd
from pymongo import MongoClient

# database connection
client = MongoClient("localhost:27017")
db=client['baseballmd']

playerInformation = db.players
careerTable = db.careerTable
careerStats = db.careerStats
splitStats = db.splitStats
metaData = db.metaData

# return db refresh info
def getDBRefreshInfo():
    docs = list(metaData.find({},{"_id" : 0}))
    seq = [x['fetchCycle'] for x in docs]
    fetchNumberMax = max(seq)
    mostRecentUpdateInfo = ''
    updateTime = ''
    for document in docs:
        if document['fetchCycle'] == fetchNumberMax:
            updateTime = document['fetchEndTime']
    mostRecentUpdateInfo = 'Last refresh ' + updateTime
    return mostRecentUpdateInfo


# return general player information
def getPlayerInformation():
    return pd.DataFrame(list(playerInformation.find({},{"_id" : 0})))

def getPlayerID(playerName):
    rawData = getPlayerInformation()
    myData = rawData.loc[rawData['fullName'] == playerName]
    playerId = myData['id'].iloc[0]
    return playerId


# return Data for basic table
def getSummedCareerStats(statGroup):
    df = pd.DataFrame(list(careerTable.find({"statGroupe" : statGroup},{"_id" : 0})))
    if statGroup == 'hitting':
        cleanedColumns = df.reindex(columns=['fullName', 'type', 'gamesPlayed', 'atBats', 'runs','hits','totalBases', 'doubles','triples', 'homeRuns', 'rbi', 'baseOnBalls', 'intentionalWalks','strikeOuts','stolenBases','caughtStealing', 'avg', 'obp','slg', 'ops','groundOutsToAirouts','plateAppearances', 'hitByPitch', 'sacBunts', 'sacFlies', 'babip','groundIntoDoublePlay','numberOfPitches','leftOnBase', 'ISO'])
        cleanedColumns.rename(columns={'fullName': 'Name', 'type':'Career', 'gamesPlayed':'G', 'atBats':'AB', 'runs':'R','hits':'H','totalBases':'TB', 'doubles':'2B','triples':'3B', 'homeRuns':'HR', 'rbi':'RBI', 'baseOnBalls':'BB', 'intentionalWalks':'IBB','strikeOuts':'SO','stolenBases':'SB','caughtStealing':'CS', 'avg':'AVG', 'obp':'OBP','slg':'SLG', 'ops':'OPS','groundOutsToAirouts':'GO/GA','plateAppearances':'PA', 'hitByPitch':'HBP', 'sacBunts':'SAC', 'sacFlies':'SF', 'babip':'BABIP','groundIntoDoublePlay':'GIDP','numberOfPitches':'NP','leftOnBase':'LOB'}, inplace=True)
        cleanedColumns.sort_values(by=['Name'], inplace=True)
    if statGroup == 'fielding':
        cleanedColumns = df.reindex(columns=['fullName', 'type', 'position','games','gamesStarted', 'innings','chances','putOuts','assists','errors','doublePlays', 'rangeFactorPerGame', 'fielding'])
        cleanedColumns.rename(columns={'fullName':'Name', 'type':'Career', 'position':'POS','games':'G','gamesStarted':'GS', 'innings':'INN','chances':'TC','putOuts':'PO','assists':'A','errors':'E','doublePlays':'DP', 'rangeFactorPerGame':'RF', 'fielding':'FPCT'}, inplace=True)
        cleanedColumns.sort_values(by=['Name'], inplace=True)
    if statGroup == 'pitching':
        cleanedColumns = df.reindex(columns=['fullName', 'type', 'wins','losses','era','gamesPlayed', 'gamesStarted', 'completeGames', 'shutouts','holds','saves','saveOpportunities','inningsPitched','hits','runs','earnedRuns','homeRuns','numberOfPitches','hitBatsmen','baseOnBalls', 'intentionalWalks','strikeOuts', 'avg','whip','groundOutsToAirouts'])
        cleanedColumns.rename(columns={'fullName':'Name', 'type':'Career','wins':'W','losses':'L','era':'ERA','gamesPlayed':'G', 'gamesStarted':'GS', 'completeGames':'CG', 'shutouts':'SHO','holds':'HLD','saves':'SV','saveOpportunities':'SVO','inningsPitched':'IP','hits':'H','runs':'R','earnedRuns':'ER','homeRuns':'HR','numberOfPitches':'NP','hitBatsmen':'HB','baseOnBalls':'BB', 'intentionalWalks':'IBB','strikeOuts':'SO', 'avg':'AVG','whip':'WHIP','groundOutsToAirouts':'GO/AO'}, inplace=True)
        cleanedColumns.sort_values(by=['Name'], inplace=True)
    return cleanedColumns




# return options for basic table
def getOptionsBasicTable(statGroup):
    if statGroup == 'hitting':
        options=[
            {'label': 'Name', 'value': 'Name'},
            {'label': 'Career', 'value': 'Career'},
            {'label': 'Games Played', 'value': 'G'},
            {'label': 'At Bats', 'value': 'AB'},
            {'label': 'Runs', 'value': 'R'},
            {'label': 'Hits', 'value': 'H'},
            {'label': 'Total Bases', 'value': 'TB'},
            {'label': 'Douples', 'value': '2B'},
            {'label': 'Triples', 'value': '3B'},
            {'label': 'Home Runs', 'value': 'HR'},
            {'label': 'Runs Batted In', 'value': 'RBI'},
            {'label': 'Bases On Balls', 'value': 'BB'},
            {'label': 'Intentional Walks', 'value': 'IBB'},
            {'label': 'Strikeouts', 'value': 'SO'},
            {'label': 'Stolen Bases', 'value': 'SB'},
            {'label': 'Caught Stealing', 'value': 'CS'},
            {'label': 'Batting Average', 'value': 'AVG'},
            {'label': 'On-Base Percentage', 'value': 'OBP'},
            {'label': 'Slugging Percentage', 'value': 'SLG'},
            {'label': 'On-base plus slugging', 'value': 'OPS'},
            {'label': 'Ground Outs/Air Outs', 'value': 'GO/GA'},
            {'label': 'Plate Appearances', 'value': 'PA'},
            {'label': 'Hit By Pitch', 'value': 'HBP'},
            {'label': 'Sacrifice Bunts', 'value': 'SAC'},
            {'label': 'Sacrifice Flys', 'value': 'SF'},
            {'label': 'Batting Average on Balls in Play', 'value': 'BABIP'},
            {'label': 'Grounded into Double Plays', 'value': 'GIDP'},
            {'label': 'Number of Pitches seen', 'value': 'NP'},
            {'label': 'Left On Base', 'value': 'LOB'},
            {'label': 'ISO', 'value': 'ISO'},
        ]
    if statGroup == 'fielding':
        options=[
            {'label': 'Name', 'value': 'Name'},
            {'label': 'Career', 'value': 'Career'},
            {'label': 'Position', 'value': 'POS'},
            {'label': 'Games', 'value': 'G'},
            {'label': 'Games Started', 'value': 'GS'},
            {'label': 'Innings At This Position', 'value': 'INN'},
            {'label': 'Total Chances (assists plus putouts plus errors)', 'value': 'TC'},
            {'label': 'Putouts', 'value': 'PO'},
            {'label': 'Assists', 'value': 'A'},
            {'label': 'Errors', 'value': 'E'},
            {'label': 'Double Plays', 'value': 'DP'},
            {'label': 'Range Factor', 'value': 'RF'},
            {'label': 'Fielding Percentage', 'value': 'FPCT'},
        ]
    if statGroup == 'pitching':
        options=[
            {'label': 'Name', 'value': 'Name'},
            {'label': 'Career', 'value': 'Career'},
            {'label': 'Wins', 'value': 'W'},
            {'label': 'Losses', 'value': 'L'},
            {'label': 'Earned Run Average', 'value': 'ERA'},
            {'label': 'Games', 'value': 'G'},
            {'label': 'Games Started', 'value': 'GS'},
            {'label': 'Complete Games', 'value': 'CG'},
            {'label': 'Shutouts', 'value': 'SHO'},
            {'label': 'Hold', 'value': 'HLD'},
            {'label': 'Saves', 'value': 'SV'},
            {'label': 'Save Opportunities', 'value': 'SVO'},
            {'label': 'Innings Pitched', 'value': 'IP'},
            {'label': 'Hits', 'value': 'H'},
            {'label': 'Runs', 'value': 'R'},
            {'label': 'Earned Runs', 'value': 'ER'},
            {'label': 'Home Runs', 'value': 'HR'},
            {'label': 'Number of Pitches Thrown', 'value': 'NP'},
            {'label': 'Hit Batsmen', 'value': 'HB'},
            {'label': 'Walks', 'value': 'BB'},
            {'label': 'Intentional Walks', 'value': 'IBB'},
            {'label': 'Strikeouts', 'value': 'SO'},
            {'label': 'Batting Average', 'value': 'AVG'},
            {'label': 'Walks + Hits/Innings Pitched', 'value': 'WHIP'},
            {'label': 'Ground Outs/Air Outs', 'value': 'GO/AO'},
        ]
    return options

#myData = getIndividualCareerStats(593428, 'hitting')


# return Data of individual career stats
def getIndividualCareerStats(playerID, statGroup):
    playerID = int(playerID)
    df = pd.DataFrame(list(careerStats.find({"id": playerID,"statGroupe" : statGroup},{"_id" : 0})))

    if careerStats.find({"id": playerID,"statGroupe" : statGroup},{"_id" : 0}).count() > 0:
        if statGroup == 'hitting':
            indexNames = df[(df['type'] == 'career') | (df['league'] == 'No Info')].index
            df.drop(indexNames, inplace=True)
            df.drop(columns=['type'], inplace=True)
            df = df.astype({'season': 'int32'})
            cleanedColumns = df.reindex(columns=['fullName', 'season', 'gamesPlayed', 'runs', 'doubles', 'triples', 'homeRuns','strikeOuts', 'baseOnBalls', 'intentionalWalks', 'hits', 'hitByPitch','avg', 'atBats', 'obp', 'slg', 'ops', 'caughtStealing', 'stolenBases', 'groundIntoDoublePlay', 'numberOfPitches','plateAppearances', 'totalBases', 'rbi', 'leftOnBase', 'sacBunts','sacFlies', 'babip', 'groundOutsToAirouts', 'team','league', 'sport','ISO'])
            cleanedColumns.rename(columns={'fullName': 'Name', 'season':'Season', 'gamesPlayed':'G', 'atBats':'AB', 'runs':'R','hits':'H','totalBases':'TB', 'doubles':'2B','triples':'3B', 'homeRuns':'HR', 'rbi':'RBI', 'baseOnBalls':'BB', 'intentionalWalks':'IBB','strikeOuts':'SO','stolenBases':'SB','caughtStealing':'CS', 'avg':'AVG', 'obp':'OBP','slg':'SLG', 'ops':'OPS','groundOutsToAirouts':'GO/GA','plateAppearances':'PA', 'hitByPitch':'HBP', 'sacBunts':'SAC', 'sacFlies':'SF', 'babip':'BABIP','team':'Team','league':'League', 'sport':'Level', 'groundIntoDoublePlay':'GIDP','numberOfPitches':'NP','leftOnBase':'LOB'}, inplace=True)
            cleanedColumns.sort_values(by=['Season'],ascending=False, inplace=True)

        if statGroup == 'fielding':
            indexNames = df[(df['type'] == 'career') | (df['league'] == 'No Info')].index
            df.drop(indexNames, inplace=True)
            df.drop(columns=['type'], inplace=True)
            df = df.astype({'season': 'int32'})
            cleanedColumns = df.reindex(columns=['fullName', 'season', 'position','games','gamesStarted', 'innings','chances','putOuts','assists','errors','doublePlays', 'rangeFactorPerGame', 'fielding', 'team','league', 'sport'])
            cleanedColumns.rename(columns={'fullName':'Name', 'season':'Season', 'position':'POS','games':'G','gamesStarted':'GS', 'innings':'INN','chances':'TC','putOuts':'PO','assists':'A','errors':'E','doublePlays':'DP', 'rangeFactorPerGame':'RF', 'fielding':'FPCT','team':'Team','league':'League', 'sport':'Level'}, inplace=True)
            cleanedColumns.sort_values(by=['Season'], ascending=False,inplace=True)


        if statGroup == 'pitching':
            indexNames = df[(df['type'] == 'career') | (df['league'] == 'No Info')].index
            df.drop(indexNames, inplace=True)
            df.drop(columns=['type'], inplace=True)
            df = df.astype({'season': 'int32'})
            cleanedColumns = df.reindex(columns=['fullName','season', 'wins','losses','era','gamesPlayed', 'gamesStarted', 'completeGames', 'shutouts','holds','saves','saveOpportunities','inningsPitched','hits','runs','earnedRuns','homeRuns','numberOfPitches','hitBatsmen','baseOnBalls', 'intentionalWalks','strikeOuts', 'avg','whip','groundOutsToAirouts','team','league', 'sport'])
            cleanedColumns.rename(columns={'fullName':'Name', 'season':'Season', 'wins':'W','losses':'L','era':'ERA','gamesPlayed':'G', 'gamesStarted':'GS', 'completeGames':'CG', 'shutouts':'SHO','holds':'HLD','saves':'SV','saveOpportunities':'SVO','inningsPitched':'IP','hits':'H','runs':'R','earnedRuns':'ER','homeRuns':'HR','numberOfPitches':'NP','hitBatsmen':'HB','baseOnBalls':'BB', 'intentionalWalks':'IBB','strikeOuts':'SO', 'avg':'AVG','whip':'WHIP','groundOutsToAirouts':'GO/AO','team':'Team','league':'League', 'sport':'Level'}, inplace=True)
            cleanedColumns.sort_values(by=['Season'], ascending=False,inplace=True)
        return cleanedColumns
    else:
        return "This player does not have " + statGroup + " data"

# return options for basic table
def getOptionsIndividualCareerStatsTable(statGroup):
    if statGroup == 'hitting':
        options=[
            {'label': 'Name', 'value': 'Name'},
            {'label': 'Season', 'value': 'Season'},
            {'label': 'Team', 'value': 'Team'},
            {'label': 'League', 'value': 'League'},
            {'label': 'Level', 'value': 'Level'},
            {'label': 'Games Played', 'value': 'G'},
            {'label': 'At Bats', 'value': 'AB'},
            {'label': 'Runs', 'value': 'R'},
            {'label': 'Hits', 'value': 'H'},
            {'label': 'Total Bases', 'value': 'TB'},
            {'label': 'Douples', 'value': '2B'},
            {'label': 'Triples', 'value': '3B'},
            {'label': 'Home Runs', 'value': 'HR'},
            {'label': 'Runs Batted In', 'value': 'RBI'},
            {'label': 'Bases On Balls', 'value': 'BB'},
            {'label': 'Intentional Walks', 'value': 'IBB'},
            {'label': 'Strikeouts', 'value': 'SO'},
            {'label': 'Stolen Bases', 'value': 'SB'},
            {'label': 'Caught Stealing', 'value': 'CS'},
            {'label': 'Batting Average', 'value': 'AVG'},
            {'label': 'On-Base Percentage', 'value': 'OBP'},
            {'label': 'Slugging Percentage', 'value': 'SLG'},
            {'label': 'On-base plus slugging', 'value': 'OPS'},
            {'label': 'Ground Outs/Air Outs', 'value': 'GO/GA'},
            {'label': 'Plate Appearances', 'value': 'PA'},
            {'label': 'Hit By Pitch', 'value': 'HBP'},
            {'label': 'Sacrifice Bunts', 'value': 'SAC'},
            {'label': 'Sacrifice Flys', 'value': 'SF'},
            {'label': 'Batting Average on Balls in Play', 'value': 'BABIP'},
            {'label': 'Grounded into Double Plays', 'value': 'GIDP'},
            {'label': 'Number of Pitches seen', 'value': 'NP'},
            {'label': 'Left On Base', 'value': 'LOB'},
            {'label': 'ISO', 'value': 'ISO'},
        ]
    if statGroup == 'fielding':
        options=[
            {'label': 'Name', 'value': 'Name'},
            {'label': 'Season', 'value': 'Season'},
            {'label': 'Team', 'value': 'Team'},
            {'label': 'League', 'value': 'League'},
            {'label': 'Position', 'value': 'POS'},
            {'label': 'Games', 'value': 'G'},
            {'label': 'Games Started', 'value': 'GS'},
            {'label': 'Innings At This Position', 'value': 'INN'},
            {'label': 'Total Chances (assists plus putouts plus errors)', 'value': 'TC'},
            {'label': 'Putouts', 'value': 'PO'},
            {'label': 'Assists', 'value': 'A'},
            {'label': 'Errors', 'value': 'E'},
            {'label': 'Double Plays', 'value': 'DP'},
            {'label': 'Range Factor', 'value': 'RF'},
            {'label': 'Fielding Percentage', 'value': 'FPCT'},
        ]
    if statGroup == 'pitching':
        options=[
            {'label': 'Name', 'value': 'Name'},
            {'label': 'Season', 'value': 'Season'},
            {'label': 'Team', 'value': 'Team'},
            {'label': 'League', 'value': 'League'},
            {'label': 'Wins', 'value': 'W'},
            {'label': 'Losses', 'value': 'L'},
            {'label': 'Earned Run Average', 'value': 'ERA'},
            {'label': 'Games', 'value': 'G'},
            {'label': 'Games Started', 'value': 'GS'},
            {'label': 'Complete Games', 'value': 'CG'},
            {'label': 'Shutouts', 'value': 'SHO'},
            {'label': 'Hold', 'value': 'HLD'},
            {'label': 'Saves', 'value': 'SV'},
            {'label': 'Save Opportunities', 'value': 'SVO'},
            {'label': 'Innings Pitched', 'value': 'IP'},
            {'label': 'Hits', 'value': 'H'},
            {'label': 'Runs', 'value': 'R'},
            {'label': 'Earned Runs', 'value': 'ER'},
            {'label': 'Home Runs', 'value': 'HR'},
            {'label': 'Number of Pitches Thrown', 'value': 'NP'},
            {'label': 'Hit Batsmen', 'value': 'HB'},
            {'label': 'Walks', 'value': 'BB'},
            {'label': 'Intentional Walks', 'value': 'IBB'},
            {'label': 'Strikeouts', 'value': 'SO'},
            {'label': 'Batting Average', 'value': 'AVG'},
            {'label': 'Walks + Hits/Innings Pitched', 'value': 'WHIP'},
            {'label': 'Ground Outs/Air Outs', 'value': 'GO/AO'},
        ]
    return options

# get level Options
def getLevelOptions(playerID, season):
    playerID = int(playerID)
    df = pd.DataFrame(list(splitStats.find({"id": playerID, "season": season},{"_id" : 0})))
    levelOptions = []
    for value in df['sport'].unique():
        levelOptions.append(value)
    levelOptions.sort()
    return levelOptions

# get Season options
def getSeasonOptions(playerID):
    playerID = int(playerID)
    df = pd.DataFrame(list(splitStats.find({"id": playerID},{"_id" : 0})))
    seasonOptions = []
    for value in df['season'].unique():
        seasonOptions.append(value)
    seasonOptions.sort()
    return seasonOptions

# return Data for splits table
def getSplitStats(playerID, season, level):
    playerID = int(playerID)
    season = int(season)
    level = str(level)
    df = pd.DataFrame(list(splitStats.find({"id": playerID, "season": season, 'sport':level},{"_id" : 0})))
    cleanedColumns = df.reindex(columns=['split', 'team', 'gamesPlayed', 'atBats', 'runs','hits','doubles', 'triples', 'homeRuns','rbi','baseOnBalls','intentionalWalks','strikeOuts', 'stolenBases', 'caughtStealing','avg',  'obp', 'slg','ops', 'hitByPitch','groundIntoDoublePlay', 'plateAppearances', 'totalBases','sacBunts', 'sacFlies', 'babip', 'groundOutsToAirouts', 'ISO'])
    cleanedColumns.rename(columns={'split': 'Split','gamesPlayed':'G', 'atBats':'AB', 'runs':'R','hits':'H','totalBases':'TB', 'doubles':'2B','triples':'3B', 'homeRuns':'HR', 'rbi':'RBI', 'baseOnBalls':'BB', 'intentionalWalks':'IBB','strikeOuts':'SO','stolenBases':'SB','caughtStealing':'CS', 'avg':'AVG', 'obp':'OBP','slg':'SLG', 'ops':'OPS','groundOutsToAirouts':'GO/GA','plateAppearances':'PA', 'hitByPitch':'HBP', 'sacBunts':'SAC', 'sacFlies':'SF', 'babip':'BABIP','team':'Team','groundIntoDoublePlay':'GIDP'}, inplace=True)
    cleanedColumns['Split'] = cleanedColumns['Split'].replace({'No Info':'Season'})
    return cleanedColumns


# return options for basic table
def getOptionsSplitsTable():
    options=[
        {'label': 'Split', 'value': 'Split'},
        {'label': 'Team', 'value': 'Team'},
        {'label': 'Games Played', 'value': 'G'},
        {'label': 'At Bats', 'value': 'AB'},
        {'label': 'Runs', 'value': 'R'},
        {'label': 'Hits', 'value': 'H'},
        {'label': 'Douples', 'value': '2B'},
        {'label': 'Triples', 'value': '3B'},
        {'label': 'Home Runs', 'value': 'HR'},
        {'label': 'Runs Batted In', 'value': 'RBI'},
        {'label': 'Bases On Balls', 'value': 'BB'},
        {'label': 'Intentional Walks', 'value': 'IBB'},
        {'label': 'Strikeouts', 'value': 'SO'},
        {'label': 'Stolen Bases', 'value': 'SB'},
        {'label': 'Caught Stealing', 'value': 'CS'},
        {'label': 'Batting Average', 'value': 'AVG'},
        {'label': 'On-Base Percentage', 'value': 'OBP'},
        {'label': 'Slugging Percentage', 'value': 'SLG'},
        {'label': 'ISO', 'value': 'ISO'},
        {'label': 'On-base plus slugging', 'value': 'OPS'},
        {'label': 'Hit By Pitch', 'value': 'HBP'},
        {'label': 'Grounded into Double Plays', 'value': 'GIDP'},
        {'label': 'Plate Appearances', 'value': 'PA'},
        {'label': 'Total Bases', 'value': 'TB'},
        {'label': 'Sacrifice Bunts', 'value': 'SAC'},
        {'label': 'Sacrifice Flys', 'value': 'SF'},
        {'label': 'Batting Average on Balls in Play', 'value': 'BABIP'},
        {'label': 'Ground Outs/Air Outs', 'value': 'GO/GA'},
    ]
    return options

# return Data for compare table
def returnCompareDate(playerID1, playerID2, statGroup):
    playerData1 = getIndividualCareerStats(playerID1, statGroup)
    playerData2 = getIndividualCareerStats(playerID2, statGroup)
    playerData1 = playerData1.append(playerData2)
    playerData1.sort_values(by=['Season'], ascending=False,inplace=True)
    seasonOptions = playerData1['Season'].unique()
    levelOptions = playerData1['Level'].unique()
    leagueOptions = playerData1['League'].unique()
    returnValues = list(playerData1, seasonOptions, levelOptions, levelOptions)
    return returnValues

returnCompareDate(465668, 636072, 'hitting')