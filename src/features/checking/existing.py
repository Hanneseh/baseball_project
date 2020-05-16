


import math

a_dict = {'id': 636072, 'fullName': 'Calten Daal', 'type': 'MiLB Career', 'statGroupe': 'hitting', 'gamesPlayed': 354.0, 'runs': 136.0, 'doubles': 28.0, 'triples': 7.0, 'homeRuns': 2.0, 'strikeOuts': 221.0, 'baseOnBalls': 62.0, 'intentionalWalks': 2.0, 'hits': 344.0, 'hitByPitch': 5.0, 'atBats': 1206.0, 'caughtStealing': 12.0, 'stolenBases': 46.0, 'groundIntoDoublePlay': 40.0, 'numberOfPitches': nan, 'plateAppearances': 1294.0, 'totalBases': 392.0, 'rbi': 104.0, 'leftOnBase': 485.0, 'sacBunts': 15.0, 'sacFlies': 5.0, 'sport': 'MiLB'}
b_dict = {'id': 636072, 'fullName': 'Calten Daal', 'type': 'MiLB Career', 'statGroupe': 'hitting', 'gamesPlayed': 354.0, 'runs': 136.0, 'doubles': 28.0, 'triples': 7.0, 'homeRuns': 2.0, 'strikeOuts': 221.0, 'baseOnBalls': 62.0, 'intentionalWalks': 2.0, 'hits': 344.0, 'hitByPitch': 5.0, 'atBats': 1206.0, 'caughtStealing': 12.0, 'stolenBases': 46.0, 'groundIntoDoublePlay': 40.0, 'numberOfPitches': nan, 'plateAppearances': 1294.0, 'totalBases': 392.0, 'rbi': 104.0, 'leftOnBase': 485.0, 'sacBunts': 15.0, 'sacFlies': 5.0, 'sport': 'MiLB'}

for value in a_dict:
    print(value)

    
    if isinstance(value, numbers.Number) and !math.isnan(value):
        sumValues.append(value)