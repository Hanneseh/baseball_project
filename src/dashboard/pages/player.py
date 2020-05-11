# imports
import pandas as pd
import dash_daq
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table as dt
import re
import numpy as np

from app import app
from .database import getPlayerInformation, getSummedCareerStats, getOptionsBasicTable, getOptionsIndividualCareerStatsTable, getIndividualCareerStats, getPlayerID, getLevelOptions, getSeasonOptions, getOptionsSplitsTable, getSplitStats

# getting raw player Information in
rawPlayerData = getPlayerInformation()

# Data for the dropdown list
options = []
for name in rawPlayerData['fullName']:
    options.append(name)
options.sort()

# this is the layout
layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='playerSelection1',
                        options=[{'label': '{}'.format(i), 'value': i} for i in options],
                        placeholder="Select Player",),
                ] , className="playerDropdown"),
            
                html.Div([
                    dash_daq.ToggleSwitch(
                        id='metricToggle',
                        value=False
                        ),
                    html.Div(id='outputMetricToggle', style={'text-align':'center'})
                ], className="toggleSwitch"),

                html.Div([
                    dcc.Dropdown(
                        id='playerSelection2',
                        options=[{'label': '{}'.format(i), 'value': i} for i in options],
                        placeholder="Select Player",
                        ),
                ] , className="playerDropdown2"),
            ]),
            html.Div([
                html.Div(id='playerInfoLeft', style={'width':'50%', 'float':'left'}),
                html.Div(id='playerInfoRight', style={'width':'50%', 'float':'right'}), 
            ]),
        ]),

        html.Div([
            html.Div(id="individHeadline", className="Sectio1"),
            html.Div([
                html.Div([
                    html.Button('Batting', id='careerHitting', n_clicks=0 ,className='Hitting'),
                    html.Button('Fielding', id='careerFielding', n_clicks=0 ,className='Fielding'),
                    html.Button('Pitching', id='careerPitching', n_clicks=0,className='Pitching'),
                    ], id='statTypeButtons', className='statTypeButtons' ,style={"display":"None"}),
                html.Div([
                    html.Div([
                        dcc.Dropdown(
                            id='seasonDropdown',
                            placeholder='Select Season',
                        ),
                    ],className="seasonDropdown"),
                    html.Div([
                        dcc.Dropdown(
                            id='levelDropdown',
                            placeholder='Select Level',
                        ),
                    ],className="levelDropdown"),
                    ], id='splitDropdownWrapper', className='statTypeButtons',style={"display":"None"}),
                html.Div([
                    html.Button('Career', id='career', n_clicks=0 ,className='Hitting'),
                    html.Button('Splits', id='splits', n_clicks=0 ,className='Fielding'),
                    ], id='statCagegoryButtons', className='statCategoryButtonGroup')
                ], id='individualPlayerInfoButtons', className='individualPlayerInfoButtons'),

            html.Div([
                dcc.Dropdown(
                    id='individualPlayerInfoDropdown',
                    multi=True,
                    placeholder='Select metrics'
                ),
            ], id='individualPlayerInfoDropdownWrapper', className="basicTableDropdown"),

            html.Div(id='individualTabpleDiv', className='playerInfoDisplayed'),
            ],id='playerInfoWrapper', className='playerInfoDisplayed',style={"display":"None"}),
        
        html.Div(id='compareDivWrapper', className='playerInfoDisplayed'),

        html.Div([
            html.Div([html.H3(['Career Summary Of All Players']
            ),], className="Sectio1"),
            html.Div([
                
                html.Button('Batting', id='Hitting', n_clicks=0 ,className='Hitting'),
                html.Button('Fielding', id='Fielding', n_clicks=0 ,className='Fielding'),
                html.Button('Pitching', id='Pitching', n_clicks=0,className='Pitching')
            ], className='buttonGroup'),
            html.Div([
                dcc.Dropdown(
                    id='basicTableDorpdown',
                    multi=True,
                    placeholder='Select metrics'
                ),
            ], id='basicTableDropdownDiv', className="basicTableDropdown"),
            
            html.Div([
                html.Div([
                    dt.DataTable(
                        id='basicTable',
                        sort_action='native',
                        style_cell={'textAlign': 'left','color': 'black'},
                        style_table={'maxHeight': ' 481px', 'overflowY': 'scroll'},
                    ),
                ], className='basicTableDiv')
            ],id='basicTableDivWrapper', className='basicTableDivWrapper')
        ], id='basicTableAndDropdownDiv', className='basicTableAndDropdownDiv'),
        
        ], className='playerContent'),
    ], className="page"),

# 1. evaluates player input --> returns button combination √
# 2. evaluates button press --> stores current button combo in the buttons, updates buttons in case of splits
# 3. evaluates button state --> returns dropdown list
# 4. evaluates dropdown and buttons --> returns table


# evaluates player input --> returns button combination
@app.callback(
    [Output('playerInfoWrapper', 'style'),
    Output('individHeadline', 'children'),
    Output('compareDivWrapper', 'children'),
    ],
    [Input('playerSelection1', 'value'),
    Input('playerSelection2', 'value')],)
def evaluatePlayerInput(playerSec1Value, playerSec2Value):
    wrapperstyle = {"display":"None"}
    headline = '',
    compareContent = '',
    if (playerSec1Value and not playerSec2Value) or (playerSec2Value and not playerSec1Value):
        if playerSec1Value:
            headline = html.H3(['Individual Player Stats of ' + playerSec1Value], style={"text-align":"center"}),
        else:
            headline = html.H3(['Individual Player Stats of ' + playerSec2Value], style={"text-align":"center"}),
        wrapperstyle = {}
    if playerSec1Value and playerSec2Value: 
        compareContent = html.Div([
            html.H3('Really cheap mockup of what the comparision table will look like'),
            html.Img(src='assets/mockup.png', style={'width':'100%'})
        ], id="compareMockUp"),
    return wrapperstyle, headline, compareContent

# evaluates button press --> stores current button combo in the buttons, updates buttons in case of splits
@app.callback(
    [Output('career', 'value'),
    Output('careerHitting','value'),
    Output('splitDropdownWrapper', 'style'),
    Output('statTypeButtons', 'style'),
    Output('seasonDropdown', 'options'), 
    Output('seasonDropdown', 'value'),
    Output('careerFielding', 'value')
    ],
    [
    Input('careerHitting','n_clicks'),
    Input('careerFielding', 'n_clicks'), 
    Input('careerPitching', 'n_clicks'),
    Input('career', 'n_clicks'),
    Input('splits', 'n_clicks'),
    Input('playerSelection1', 'value'),
    Input('playerSelection2', 'value'),
    ])
def evaluateButtonPress(hittingClicks, fieldingClicks, pitchingClicks, careerClicks, splitsClicks, playerLeft, playerRight):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    statsCategory = 'career'
    statsType = 'hitting'
    infoButtonVisibility = {}
    splitDropdownVisibility = {"display":"None"}
    listOfOptions = ['', '']
    seasonOptions = [{'label': '{}'.format(i), 'value': i} for i in listOfOptions]
    seasonValue = listOfOptions[0]
    playerId = 0
    if playerLeft:
            playerId = getPlayerID(playerLeft)
    if playerRight: 
        playerId = getPlayerID(playerRight)
    if 'careerHitting' in changed_id:
        statsType = 'hitting'
    if 'careerFielding' in changed_id:
        statsType = 'fielding'
    if 'careerPitching' in changed_id:
        statsType = 'pitching'
    if 'career' in changed_id:
        statsCategory = 'career'
    if 'splits' in changed_id:
        listOfOptions = getSeasonOptions(playerId)
        seasonOptions = [{'label': '{}'.format(i), 'value': i} for i in listOfOptions]
        seasonValue = listOfOptions[len(listOfOptions)-1]
        statsCategory = 'splits'
        infoButtonVisibility = {"display":"None"}
        splitDropdownVisibility = {}
    playerId = str(playerId)
    return statsCategory, statsType, splitDropdownVisibility, infoButtonVisibility, seasonOptions, seasonValue, playerId

# returns options for level dropdown
@app.callback(
    [Output('levelDropdown', 'options'),
    Output('levelDropdown', 'value')],
    [
    Input('seasonDropdown', 'value'),
    Input('careerFielding', 'value')
    ])
def setLevelValueAndOptions(seasonValue, playerId):
    listOfOptions = ['', '']
    levelOptions = [{'label': '{}'.format(i), 'value': i} for i in listOfOptions]
    levelValue = listOfOptions[0]
    if isinstance(seasonValue, int):
        playerId = int(playerId)
        listOfOptions = getLevelOptions(playerId, seasonValue)
        levelOptions = [{'label': '{}'.format(i), 'value': i} for i in listOfOptions]
        levelValue = listOfOptions[len(listOfOptions)-1]
    return levelOptions, levelValue

# evaluates button state --> returns dropdown list
@app.callback(
    [Output('individualPlayerInfoDropdown', 'options'),
    Output('individualPlayerInfoDropdown', 'value'),],
    [Input('career', 'value'),
    Input('careerHitting','value'),
    Input('levelDropdown', 'value'), 
    Input('seasonDropdown', 'value')])
def evaluateButtonState(statsCategory, statsType, levelDropdown, seasonDropdown):

    dropdownOptions = [{'label': 'Name', 'value': 'Name'},{'label': 'Career', 'value': 'Career'},]
    dropdownValues = ['Name']

    if statsCategory == 'career':
        if statsType == 'hitting':
            dropdownOptions = getOptionsIndividualCareerStatsTable('hitting')
            dropdownValues=['Season','ISO','AVG', 'OPS','G','AB','R','H','TB', '2B','3B','HR','GO/GA']
        if statsType == 'fielding':
            dropdownOptions = getOptionsIndividualCareerStatsTable('fielding')
            dropdownValues=['POS','G','GS', 'INN','TC','PO','A','E','DP', 'RF', 'FPCT']
        if statsType == 'pitching':
            dropdownOptions = getOptionsIndividualCareerStatsTable('pitching')
            dropdownValues=['W','L','G','SVO','IP','H','R','HR','NP', 'IBB','AVG','GO/AO']
    if statsCategory == 'splits':
       dropdownOptions = getOptionsSplitsTable()
       dropdownValues = ['Split', 'Team', 'G', 'AB','R', 'H', 'AVG', 'OBP', 'SLG', 'OPS']
    
    return dropdownOptions, dropdownValues


# evaluates dropdown and buttons --> returns table
@app.callback(
    [Output('individualTabpleDiv', 'children')],
    [Input('individualPlayerInfoDropdown', 'value'),
    Input('career', 'value'),
    Input('careerHitting','value'),
    Input('levelDropdown', 'value'), 
    Input('seasonDropdown', 'value'),
    Input('careerFielding', 'value'),])
def update_Individualtable(dropdownValue, statsCategory, statsType, levelDropdown, seasonDropdown, playerId):
    if playerId != '0':
        playerId = int(playerId)
        tableData = ''
        if statsCategory == 'career':
            if statsType == 'hitting':
                tableData = getIndividualCareerStats(playerId, statsType)
            if statsType == 'fielding':
                tableData = getIndividualCareerStats(playerId, statsType)
            if statsType == 'pitching':
                tableData = getIndividualCareerStats(playerId, statsType)
        if statsCategory == 'splits' and len(levelDropdown) > 1 and len(dropdownValue) == 10:
            tableData = getSplitStats(playerId, seasonDropdown, levelDropdown)

        if isinstance(tableData, str):
            table = html.Div([ tableData], className='individualPlayerInfoTableDiv'),
            return table
        else:
            displayedData = tableData[dropdownValue]
            table = html.Div([
                dt.DataTable(
                    id='individualPlayerInfoTable',
                    sort_action='native',
                    style_cell={'textAlign': 'left','color': 'black'},
                    style_table={'maxHeight': ' 481px', 'overflowY': 'scroll'},
                    data=displayedData.to_dict('records'),
                    columns = [{"name": i, "id": i} for i in displayedData.columns],
                    ),
                    ], className='individualPlayerInfoTableDiv'),
            return table
    else:
        table = html.Div([ ''
        ], className='individualPlayerInfoTableDiv'),
        return table


# Callback for updating basic table dropdown options and default values
@app.callback(
    [Output('Hitting','value'),
    Output('basicTableDorpdown','value'),
    Output('basicTableDorpdown', 'options')],
    [Input('Hitting','n_clicks'),
    Input('Fielding', 'n_clicks'), 
    Input('Pitching', 'n_clicks')])
def determinButtonPress(hittingClicks, fieldingClicks, pitchingClicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    pressedButton = ''
    deafultdropdown=[]
    dropdownOptions = ''
    if 'Hitting' in changed_id:
        pressedButton = '1'
        dropdownOptions = getOptionsBasicTable('hitting')
        deafultdropdown=['Name', 'Career','G','AB', 'ISO','R','H','TB', '2B','3B','HR','AVG', 'OPS','GO/GA']
    elif 'Fielding' in changed_id:
        pressedButton = '2'
        dropdownOptions = getOptionsBasicTable('fielding')
        deafultdropdown=['Name' ,'Career', 'POS','G','GS', 'INN','TC','PO','A','E','DP', 'RF', 'FPCT']
    elif 'Pitching' in changed_id:
        pressedButton = '3'
        dropdownOptions = getOptionsBasicTable('pitching')
        deafultdropdown=['Name', 'Career','W','L','G','SVO','IP','H','R','HR','NP', 'IBB','AVG','GO/AO']
    else:
        pressedButton = '1'
        dropdownOptions = getOptionsBasicTable('hitting')
        deafultdropdown=['Name', 'Career','G','AB','R','H','TB', '2B','3B','HR','AVG', 'OPS','GO/GA']
    return pressedButton, deafultdropdown, dropdownOptions

# Callback to load the correct "basic table" data and columns
@app.callback(
    [Output('basicTable', 'columns'),
    Output('basicTable', 'data')],
    [Input('basicTableDorpdown', 'value'),
    Input('Hitting', 'value')])
def update_table(dropdownValue, buttonValue):
    buttonString = ''
    if buttonValue == '1':
        buttonString = 'hitting'
    if buttonValue == '2':
        buttonString = 'fielding'
    if buttonValue == '3':
        buttonString = 'pitching'
    tableData = getSummedCareerStats(buttonString)
    displayedData = tableData.loc[:,dropdownValue]
    columns = [{"name": i, "id": i} for i in displayedData.columns]
    data = displayedData.to_dict('records')
    return columns, data

# Callback to change unit toggle value
@app.callback(
    Output('outputMetricToggle', 'children'),
    [Input('metricToggle', 'value')])
def update_output(value):
    if value == False: 
        return 'Imperial'
    else:
        return 'Metric'

# Callback to load player information right
@app.callback(
    [Output('playerInfoRight', 'children')],
    [Input('playerSelection2', 'value'),
     Input('metricToggle', 'value')],
)
def showPlayerInformation2(playerName, toggleValue):
    if playerName:
        myData = rawPlayerData.loc[rawPlayerData['fullName'] == playerName]
        myData.reset_index(drop=True, inplace=True)
        relevantData = myData.drop(columns = ['id', 'imageLink'])
        valuesValues = []
        formattedColumnNames = ['Name', 'Birthdate', 'Age', 'Height', 'Weight', 'Active', 'Position']
        for playerValue in relevantData.loc[0]:
            if isinstance(playerValue, str) and "\"" in playerValue:
                if toggleValue == True:
                    extracted = []
                    for digit in playerValue:
                        if digit.isdigit():
                            extracted.append(digit)
                    meters = (float(extracted[0]) * 30.48 + float(extracted[1]) * 2.54) / 100
                    playerValue = "{:.2f} m".format(meters)
            if isinstance(playerValue, np.int64) and playerValue >= 99:
                if toggleValue == False:
                    playerValue = str(playerValue) + " lbs"
                if toggleValue == True:
                    kilos = playerValue * 0.453592
                    playerValue = "{:.2f} kg".format(kilos)
            if isinstance(playerValue, np.bool_) and playerValue == True:
                playerValue = 'Yes'
            valuesValues.append(playerValue)

        pivotData = {}
        pivotData['Descriptions'] = formattedColumnNames
        pivotData['Values'] = valuesValues
        pivotRelevant = pd.DataFrame(data=pivotData)

        playerInfoRight = html.Div([
            html.Div([
                html.Img(src=myData['imageLink'].iloc[0]),
            ],id='imageDiv2', className="playerImage2"),
            html.Div([
                html.Div([
                    dt.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i, "selectable": True} for i in pivotRelevant.columns],
                        data=pivotRelevant.to_dict('records'),
                        style_cell={'border':'none', 'textAlign': 'left','background-color': 'whitesmoke'},
                        style_as_list_view=True,
                        style_header = {'display': 'none'},
                        
                    ),
                ], className="playerInformation2"),   
            ],id='playerInformation2', className="playerInformation2"),
        ]),
    else:
        playerInfoRight = html.Div(['No player selected'],className="noplayerright"),
    
    return playerInfoRight

# Callback to load player information left
@app.callback(
    [Output('playerInfoLeft', 'children')],
    [Input('playerSelection1', 'value'),
     Input('metricToggle', 'value')],
)
def showPlayerInformation(playerName, toggleValue):
    if playerName:
        myData = rawPlayerData.loc[rawPlayerData['fullName'] == playerName]
        myData.reset_index(drop=True, inplace=True)
        relevantData = myData.drop(columns = ['id', 'imageLink'])
        valuesValues = []
        formattedColumnNames = ['Name', 'Birthdate', 'Age', 'Height', 'Weight', 'Active', 'Position']
        for playerValue in relevantData.loc[0]:
            if isinstance(playerValue, str) and "\"" in playerValue:
                if toggleValue == True:
                    extracted = []
                    for digit in playerValue:
                        if digit.isdigit():
                            extracted.append(digit)
                    meters = (float(extracted[0]) * 30.48 + float(extracted[1]) * 2.54) / 100
                    playerValue = "{:.2f} m".format(meters)
            if isinstance(playerValue, np.int64) and playerValue >= 99:
                if toggleValue == False:
                    playerValue = str(playerValue) + " lbs"
                if toggleValue == True:
                    kilos = playerValue * 0.453592
                    playerValue = "{:.2f} kg".format(kilos)
            if isinstance(playerValue, np.bool_) and playerValue == True:
                playerValue = 'Yes'
            valuesValues.append(playerValue)

        pivotData = {}
        pivotData['Descriptions'] = formattedColumnNames
        pivotData['Values'] = valuesValues
        pivotRelevant = pd.DataFrame(data=pivotData)

        playerInfoLeft = html.Div([
            html.Div([
                html.Img(src=myData['imageLink'].iloc[0]),
            ],id='imageDiv', className="playerImage"),
            html.Div([
                html.Div([
                    dt.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i, "selectable": True} for i in pivotRelevant.columns],
                        data=pivotRelevant.to_dict('records'),
                        style_cell={'border':'none', 'textAlign': 'left','background-color': 'whitesmoke'},
                        style_as_list_view=True,
                        style_header = {'display': 'none'},
                        
                    ),
                ], className="playerInformation"),   
            ],id='playerInformation', className="playerInformation"),
        ]),
    else:
        playerInfoLeft = html.Div(['No player selected'],className="noplayerleft"),     
    
    return playerInfoLeft