# imports
import pandas as pd
from pymongo import MongoClient

# database connection
client = MongoClient("localhost:27017")
db=client['baseballmd']

playerInformation = db.players
careerTable = db.careerTable
careerStats = db.careerStats

# return general player information
def getPlayerInformation():
    return pd.DataFrame(list(playerInformation.find({},{"_id" : 0})))

# return Data for basic table
def getSummedCareerStats(statGroup):
    df = pd.DataFrame(list(careerTable.find({"statGroupe" : statGroup},{"_id" : 0})))
    if statGroup == 'hitting':
        cleanedColumns = df.loc[:,('fullName', 'type', 'gamesPlayed', 'atBats', 'runs','hits','totalBases', 'doubles','triples', 'homeRuns', 'rbi', 'baseOnBalls', 'intentionalWalks','strikeOuts','stolenBases','caughtStealing', 'avg', 'obp','slg', 'ops','groundOutsToAirouts','plateAppearances', 'hitByPitch', 'sacBunts', 'sacFlies', 'babip','groundIntoDoublePlay','numberOfPitches','leftOnBase')]
        cleanedColumns.rename(columns={'fullName': 'Name', 'type':'Career', 'gamesPlayed':'G', 'atBats':'AB', 'runs':'R','hits':'H','totalBases':'TB', 'doubles':'2B','triples':'3B', 'homeRuns':'HR', 'rbi':'RBI', 'baseOnBalls':'BB', 'intentionalWalks':'IBB','strikeOuts':'SO','stolenBases':'SB','caughtStealing':'CS', 'avg':'AVG', 'obp':'OBP','slg':'SLG', 'ops':'OPS','groundOutsToAirouts':'GO/GA','plateAppearances':'PA', 'hitByPitch':'HBP', 'sacBunts':'SAC', 'sacFlies':'SF', 'babip':'BABIP','groundIntoDoublePlay':'GIDP','numberOfPitches':'NP','leftOnBase':'LOB'}, inplace=True)
        cleanedColumns.sort_values(by=['Name'], inplace=True, ignore_index=True)
    if statGroup == 'fielding':
        cleanedColumns = df.loc[:,('fullName', 'type', 'position','games','gamesStarted', 'innings','chances','putOuts','assists','errors','doublePlays', 'rangeFactorPerGame', 'fielding')]
        cleanedColumns.rename(columns={'fullName':'Name', 'type':'Career', 'position':'POS','games':'G','gamesStarted':'GS', 'innings':'INN','chances':'TC','putOuts':'PO','assists':'A','errors':'E','doublePlays':'DP', 'rangeFactorPerGame':'RF', 'fielding':'FPCT'}, inplace=True)
        cleanedColumns.sort_values(by=['Name'], inplace=True, ignore_index=True)
    if statGroup == 'pitching':
        cleanedColumns = df.loc[:,('fullName', 'type', 'wins','losses','era','gamesPlayed', 'gamesStarted', 'completeGames', 'shutouts','holds','saves','saveOpportunities','inningsPitched','hits','runs','earnedRuns','homeRuns','numberOfPitches','hitBatsmen','baseOnBalls', 'intentionalWalks','strikeOuts', 'avg','whip','groundOutsToAirouts')]
        cleanedColumns.rename(columns={'fullName':'Name', 'type':'Career','wins':'W','losses':'L','era':'ERA','gamesPlayed':'G', 'gamesStarted':'GS', 'completeGames':'CG', 'shutouts':'SHO','holds':'HLD','saves':'SV','saveOpportunities':'SVO','inningsPitched':'IP','hits':'H','runs':'R','earnedRuns':'ER','homeRuns':'HR','numberOfPitches':'NP','hitBatsmen':'HB','baseOnBalls':'BB', 'intentionalWalks':'IBB','strikeOuts':'SO', 'avg':'AVG','whip':'WHIP','groundOutsToAirouts':'GO/AO'}, inplace=True)
        cleanedColumns.sort_values(by=['Name'], inplace=True, ignore_index=True)
    return cleanedColumns




{'sacFlies':'SF', 'babip':'BABIP','groundIntoDoublePlay':'GIDP','numberOfPitches':'NP','leftOnBase':'LOB'}
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
            {'label': 'On-Base Percentage', 'value': 'OPS'},
            {'label': 'Ground Outs/Air Outs', 'value': 'GO/GA'},
            {'label': 'Plate Appearances', 'value': 'PA'},
            {'label': 'Hit By Pitch', 'value': 'HBP'},
            {'label': 'Sacrifice Bunts', 'value': 'SAC'},
            {'label': 'Sacrifice Flys', 'value': 'SF'},
            {'label': 'Batting Average on Balls in Play', 'value': 'BABIP'},
            {'label': 'Grounded into Double Plays', 'value': 'GIDP'},
            {'label': 'Number of Pitches seen', 'value': 'NP'},
            {'label': 'Left On Base', 'value': 'LOB'},
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


