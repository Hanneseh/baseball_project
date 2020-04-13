# importing the api wrapper
import statsapi
import pandas as pd

# player IDs df
players = pd.DataFrame(data={'Name': ['Ozzie Albies', 'Xander Bogaerts', 'Didi Gregorius'], 'ID':[645277, 593428, 544369]})
players

statsapi.player_stats(next(
        x['id'] for x in statsapi.get(
            'sports_players',
            {'season':2019,'gameType':'R'}
            )
            ['people'] if x['fullName']=='Xander Bogaerts'),
             'hitting', 'career')

statsapi.get('sports_players',{'season':2019,'gameType':'R'})['people'] if x['id']==645277),'hitting', 'career')

statsapi.get('sports_players',{'season':2019,'gameType':'R'})

statsapi.get('people',{'personIds':'645277,593428','hydrate':'stats(group=[hitting,pitching],type=[statSplits],sitCodes=[vr,vl])')

requests.get


splitParams = {'personIds':personIds, 'hydrate':'stats(group=[hitting,pitching],type=[statSplits],sitCodes=[vr,vl],season=2019)'}
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
https://statsapi.mlb.com/api/v1/people?personIds=645277,593428,544369&hydrate=stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc,h0],season=2019)

# sample url splits of season 2019 only xander
https://statsapi.mlb.com/api/v1/people?personIds=593428&hydrate=stats(type=[statSplits],sitCodes=[h,a,d,n,g,t,1,2,3,4,5,6,7,8,9,10,11,12,preas,posas,vr,vl,r0,r1,r2,r3,r12,r13,r23,r123,risp,o0,o1,o2,i01,i02,i03,i04,i05,i06,i07,i08,i09,ix,b2,b3,b4,b4,b5,b6,lo,lc,ac,bc,h0],season=2019)


### sample URL for Career data 
