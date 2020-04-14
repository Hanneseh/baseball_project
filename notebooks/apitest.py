'''
This file was written to explore the official MLB API. 
https://appac.github.io/mlb-data-api-docs/
https://statsapi.mlb.com/api/v1/sports

The API is accessed through a wrapper which as availabe on github:
https://github.com/toddrob99/MLB-StatsAPI/wiki

It can be installed via pip
pip install MLB-StatsAPI

The goal of this file is to check, whether it is possible to retrieve all the 
data of a player which is asked for by the sports data valley lab
'''


# importing the api wrapper
import statsapi

'''
Testing some basic functions and see what they return:
'''

# get general information about player by id 
# https://github.com/toddrob99/MLB-StatsAPI/wiki/Function:-get
statsapi.get('person', {'personId':645277})

# retriving player stats by Function: player_stats_data 
# https://github.com/toddrob99/MLB-StatsAPI/wiki/Function:-player_stat_data
statsapi.player_stat_data(593428, group="[hitting,pitching,fielding]", type="career")

# retriving player stats by Function: player_data 
# https://github.com/toddrob99/MLB-StatsAPI/wiki/Function:-player_stats
print(statsapi.player_stats(593428, group="[hitting,pitching,fielding]", type="career"))

# an example how to use player_data to make a more complex requests
# https://github.com/toddrob99/MLB-StatsAPI/wiki/Function:-player_stats
print( statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',
{'season':2008,'gameType':'W'})['people'] if x['fullName']=='Chase Utley'), 'hitting', 'career') )

# retriving player stats by Function: get (gives the most data): 
# https://github.com/toddrob99/MLB-StatsAPI/wiki/Function:-get
statsapi.get('person_stats', {'personId':593428, 'gamePk':"current"})

'''
Here I went more in deph how we could utilitize the API:
'''

# Making a sample scrap by using player_stats_data
stats1 = statsapi.player_stat_data(593428, group="[hitting,pitching,fielding]", type="career")
stats1
'''
This command seems to return a very large python dictionary with stats data of the player
Maybe this can be used later on to get very specifc numbers. However the command tested below
seems to be more promesing right now.
'''

#############################################################################################
# Making a sample scrap by using complex player_data
stats2 = statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2019,'gameType':'R'})['people'] if x['fullName']=='Xander Bogaerts'), 'hitting', 'career')
print(stats2)
stats2.dtype()

'''
The function above returns a single string, which diplays most relevant data pretty nicely when printed.
The parameters in the function can be altered in such a way, that they display all relevant career and split data

to prove this, I made a comparison by hand below, which shows the output of the function 
in camparison with the stats on the website: 
https://www.mlb.com/player/xander-bogaerts-593428?stats=career-r-hitting-mlb&year=2019
'''

# the comparision (just for us to read, no actual code for the program later on)
'''
Xander "X-Man" Bogaerts, SS (2013-)

Career Hitting        
gamesPlayed: 914                on website: G:914 
groundOuts: 1001                on website: not available BUT: GO/AO: 1.10 which is the same numbers just devided
airOuts: 913                    on website: not available: GO/AO: 1.10 which is the same numbers just devided
runs: 542                       on website: R: 542
doubles: 228                    on website: 2B: 228
triples: 14                     on website: 3B: 14
homeRuns: 107                   on website: H4: 107
strikeOuts: 715                 on website: SO: 715
baseOnBalls: 321                on website: BB: 321
intentionalWalks: 14            on website: IBB: 14
hits: 1022                      on website: H: 1022
hitByPitch: 31                  on website: HBP: 31
avg: .288                       on website: AVG: .288
atBats: 3545                    on website: AB: 3545
obp: .350                       on website: OBP: .350
slg: .451                       on website: SLG: .451
ops: .801                       on website: OPS: .801
caughtStealing: 14              on website: CS: 14
stolenBases: 53                 on website: SB: 53
stolenBasePercentage: .791      on website: Not available
groundIntoDoublePlay: 84        on website: GIDP: 84
numberOfPitches: 15802          on website: NP: 15802
plateAppearances: 3930          on website: PA 3930
totalBases: 1599                on website: TB 1599
rbi: 503                        on website: RBI 503
leftOnBase: 1483                on website: LOB 1483
sacBunts: 5                     on website: SAC 5
sacFlies: 28                    on website: SAC 28
babip: .333                     on website: BABIP: .333
groundOutsToAirouts: 1.10       on website: GO/AO 1.10
atBatsPerHomeRun: 33.13         on website: Not Available
'''

# results:
'''
It seems like, that we get mix of the "Career stats" and the "Advanced Career Stats" 
I think we get all the data we need. By altering the command for each season year, we can srape 
the entire table.
The nice thing is, that we basicly only need the name of the player which we can scrape from
the https://www.honkbalsite.com/profhonkballers/ site
However, it would be interesting to check the "stats1" variable in depth, to see if thats
an easier way to retrieve the relevant data
'''

# checking if filding data can be retrieved: it works like this
print(statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2019,'gameType':'R'})['people'] if x['fullName']=='Xander Bogaerts'), 'fielding', 'career'))

# checking if split data can be retrieved: this does not work like this
# request probalby can be adjusted following this docu:
# https://appac.github.io/mlb-data-api-docs/
print(statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',{'season':2019,'gameType':'R'})['people'] if x['fullName']=='Xander Bogaerts'), 'splits'))

#############################################################
# making a csv file with the career stats of Xander Bogaerts and Ozzie Albies in order 
# to display there data in the dashboard. The stats are onle retrieved for hitting and season 2019
# filding and other season stats can be added later

xanderBog = statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',
{'season':2019,'gameType':'R'})['people'] if x['fullName']=='Xander Bogaerts'), 'hitting', 'career')
ozzieAlbies = statsapi.player_stats(next(x['id'] for x in statsapi.get('sports_players',
{'season':2019,'gameType':'R'})['people'] if x['fullName']=='Ozzie Albies'), 'hitting', 'career')

xanderBog
ozzieAlbies

#splitting the stings
splitXB = xanderBog.split('\n')
splitOA = ozzieAlbies.split('\n')

# getting the name
name = splitXB[0].split(',')
name = name[0]
print(name)

nameOA = splitOA[0].split(',')
nameOA = nameOA[0]
print(nameOA)

# getting the type of stats
statsFor = splitXB[2]
print(statsFor)

statsForOA = splitOA[2]
print(statsForOA)

# cleaning array of strings
splitXBclean = splitXB[3:len(splitXB)-2]
splitXBclean

splitOAclean = splitOA[3:len(splitOA)-2]
splitOAclean

# preparing data frame {'col1': [1, 2], 'col2': [3, 4]}
import pandas as pd
dfXN = pd.DataFrame(data={'Player': [name], 'Stats': [statsFor], 'Season': 2019})
dfXN

dfOA = pd.DataFrame(data={'Player': [nameOA], 'Stats': [statsForOA], 'Season': 2019})
dfOA

# doing the rest
for data in splitXBclean:
    #splitting
    keyPair = data.split(':')
    # remove space caracters
    keyPair[1] = keyPair[1].replace(" ", "")
    # cast to flaot
    keyPair[1] = float(keyPair[1])
    # adding to dataframe
    dfXN[keyPair[0]] = keyPair[1]

dfXN

for data in splitOAclean:
    #splitting
    keyPair = data.split(':')
    # remove space caracters
    keyPair[1] = keyPair[1].replace(" ", "")
    # cast to flaot
    keyPair[1] = float(keyPair[1])
    # adding to dataframe
    dfOA[keyPair[0]] = keyPair[1]

dfOA

# this is really a quick and dirty approach for "cleaning" the data
# the code above needs to refactored and put in loops, but we figure that out later
# now we can combine the tow data frames to one and save it as a csv

dfXN = dfXN.append(dfOA)
dfXN = dfXN.reset_index(drop=True)
dfXN

# export to csv
dfXN.to_csv('/Users/Hannes/baseball-project/baseballmd/notebooks/playerStats.csv', index = False)


# further experimentation: 

personIds = "645277,593428,544369"
splitParams = {'personIds':personIds, 'hydrate':'stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc],season=2019'}
people = statsapi.get('people',params)
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



# sample url splits of season 2018 with random player IDs
https://statsapi.mlb.com/api/v1/people?personIds=434378,519203&hydrate=stats(group=[hitting,pitching],type=[statSplits],sitCodes=[vr,vl],season=2018)

# sample url splits of season 2019 with multiple players
https://statsapi.mlb.com/api/v1/people?personIds=645277,593428,544369&hydrate=stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc],season=2019)

# sample url splits of season 2019 only xander
https://statsapi.mlb.com/api/v1/people?personIds=593428&hydrate=stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc],season=2019)

# sample url splits of entire season 2019 only xander (last row in table)
https://statsapi.mlb.com/api/v1/people?personIds=593428&hydrate=stats(type=[season],season=2018)

################################# Careere Data #####################################
# sample URL for Career data of just one specific season with one player
https://statsapi.mlb.com/api/v1/people?personIds=593428&hydrate=stats(group=[hitting,pitching],type=[statsSingleSeason],season=2018)

# sample URL for Career data of one season for several players
https://statsapi.mlb.com/api/v1/people?personIds=645277,593428&hydrate=stats(group=[hitting,pitching],type=[statsSingleSeason],season=2018)

# sample URL for Career data of entire mlb Career
https://statsapi.mlb.com/api/v1/people?personIds=593428&hydrate=stats(group=[hitting,pitching],type=[career])

statsapi.meta('baseballStats')

## experimentation
https://statsapi.mlb.com/api/v1/people?personIds=645277,593428,544369&hydrate=stats(group=[hitting,pitching,fielding],type=[yearByYear])