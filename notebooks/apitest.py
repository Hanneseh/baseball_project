# api testing 
# https://github.com/toddrob99/MLB-StatsAPI/wiki

# imports
import statsapi

# get general information about player by id 
statsapi.get('person', {'personId':593428})

# get 
statsapi.player_stat_data(593428, type="career")


statsapi.get('person_stats', {'personId':593428, 'gamePk':"career"})


statsapi.player_stat_data(593428, group="[hitting,pitching,fielding]", type="career")


# retriving player stats by Function: player_stats
statsapi.player_stats(593428, group="[hitting,pitching,fielding]", type="career")

# retriving player stats by Function: player_stat_data

# retriving player stats by Function: get

player = statsapi.lookup_player('nola,')
player

