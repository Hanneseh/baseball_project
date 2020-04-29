# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import pandas as pd
# from app import app
# import dash_table as dt 
# import plotly.express as px
# from pymongo import MongoClient

# import numpy as np 

# '''
# TO DO:
# - Get all carrer summary stats form the database and organize them in a datafram
#     - Hints: {"type" : "career", "statGroupe" : "hitting"}
# - Try to figure a way out 
# '''
# client = MongoClient("localhost:27017")
# db=client['baseballmd']
# collection = db.careerStats

# rawCompareData = pd.DataFrame(list(collection.find({"type" : "career", "statGroupe" : "hitting"})))
# #https://dash.plotly.com/dash-core-components/graph
# selectedCompareData=rawCompareData.drop(columns=['_id', 'id', 'sport','gameType'])
# selectedCompareData.columns 
# # selectedCompareData.rename(columns={'fullName', 'type', 'statGroupe', 'gamesPlayed', 'groundOuts',
# #        'airOuts', 'runs', 'doubles', 'triples', 'homeRuns', 'strikeOuts',
# #        'baseOnBalls', 'intentionalWalks', 'hits', 'hitByPitch', 'avg',
# #        'atBats', 'obp', 'slg', 'ops', 'caughtStealing', 'stolenBases',
# #        'stolenBasePercentage', 'groundIntoDoublePlay', 'numberOfPitches',
# #        'plateAppearances', 'totalBases', 'rbi', 'leftOnBase', 'sacBunts',
# #        'sacFlies', 'babip', 'groundOutsToAirouts', 'atBatsPerHomeRun',
# #        'gameType'}




# df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
# df.rename(columns={"A": "a", "B": "c"})


# layout = html.Div([
#     html.H3('Compare Players'),

#     html.Div([dt.DataTable(
#         id='table',
#         columns=[{"name": i, "id": i} for i in selectedCompareData.columns],
#         data=selectedCompareData.to_dict('records'),
#         style_table={'overflowX': 'scroll', 'height':'auto'}
#     )])
#     # dt.DataTable(
#     #     id='table', 
        
#     #     data=rawPlayerData.to_dict('records'),
#     #     style_table={'overflowX': 'scroll', 'whiteSpace': 'normal', 'height':'auto'},
        
#     # )

# ], className="page")
