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

# getting Names and IDs of the player (For now only a sample dataframe, later this will come from the database)
players = pd.DataFrame(data={'Name': ['Ozzie Albies', 'Xander Bogaerts', 'Didi Gregorius'], 'ID':[645277, 593428, 544369]})
players

# https://statsapi.mlb.com/api/v1/people?personIds=645277,593428,544369&hydrate=stats(group=[hitting,fielding,pitching],type=[yearByYear])

# transforming the IDs to a comma seperated string in order to serve as a parameter later on
playerIDs = ""
for playerID in players['ID']:
    playerIDs = playerIDs + str(playerID) + ","
playerIDs

# retrieving all career data
careerParams = {'personIds':playerIDs, 'hydrate':'stats(group=[hitting,fielding,pitching],type=[yearByYear])'}
careerStats = statsapi.get('people',careerParams)
careerStats

df = pd.DataFrame.from_dict(careerStats)
df

for player in careerStats['people']:
    # print('Name:', player['fullName'])
    name = player['fullName']
    # print('ID:', player['id'])
    thisPlayersID = player['id']
    for stat in player['stats']:
        # print('statGroupe:',stat['group']['displayName'])
        statGroupe = stat['group']['displayName']
        for split in stat['splits']:
            print('ID', thisPlayersID)
            print('statGroupe', statGroupe)
            print('season',split['season'])
            print('Name', name)
            #print('stats', split['stat'])
            for seasonStat in split['stat']:
                print(seasonStat,split['stat'][seasonStat])
            print('team:', split['team']['name'])
            print('league: ', split['league']['name'])
            print('sport:', split['sport']['abbreviation'])
            print('gameType:', split['gameType'])
            print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')


# TO do:
# what about general Player information?
# Waht about position information?


# sample request and printing of the data 
splitParams = {'personIds':playerIDs, 'hydrate':'stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc],season=2019)'}
people = statsapi.get('people',splitParams)
people

for person in people['people']:
    print('{}'.format(person['fullName']))
    for stat in person['stats']:
        if len(stat['splits']): print('  {}'.format(stat['group']['displayName']))
        for split in stat['splits']:
            print('    {} {}:'.format(split['season'], split['split']['description']))
            for split_stat,split_stat_value in split['stat'].items():
                print('      {}: {}'.format(split_stat, split_stat_value))
            print('\n')