# imports
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
from dash.dependencies import Input, Output
import dash_table as dt
import re
import numpy as np

from app import app
from .components import Header
from .database import getPlayerInformation, getSummedCareerStats, getOptionsBasicTable

# getting raw data in
rawPlayerData = getPlayerInformation()

# Data for the dropdown list
options = []
for name in rawPlayerData['fullName']:
    options.append(name)
options.sort()

# default Data for basic table



# this is the layout
layout = html.Div([
    Header(),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(
                    id='playerSelection1',
                    options=[
                        {'label': '{}'.format(i), 'value': i} for i in options
                    ],
                    placeholder="Select Player",
                    ),
                ] , className="playerDropdown"),
            
                html.Div([
                    html.Div([
                        daq.ToggleSwitch(
                        id='metricToggle',
                        value=False
                        ),
                    ]),
                    html.Div(id='outputMetricToggle', style={'text-align':'center'})
                ], className="toggleSwitch"),

                html.Div([
                    dcc.Dropdown(
                    id='playerSelection2',
                    options=[
                        {'label': '{}'.format(i), 'value': i} for i in options
                    ],
                    placeholder="Select Player",
                    ),
                ] , className="playerDropdown2"),
            ]),
            html.Div([
                html.Div([ 
                    html.Div(id='imageDiv', className="playerImage"),
                    html.Div(id='playerInformation', className="playerInformation"),
                ], style={'width':'50%', 'float':'left'}), 
                
                html.Div([ 
                    html.Div(id='imageDiv2', className="playerImage2"),
                    html.Div(id='playerInformation2', className="playerInformation2"),
                ], style={'width':'50%', 'float':'right'}), 
            ]),
        ]),
        html.Div(style={'background-image':'url(/assets/SDV_bat_header_copy.png)'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='basicTableDorpdown',
                    multi=True,
                    placeholder='Select metrics'

                ),
            ], id='basicTableDropdownDiv', className="basicTableDropdown"),
            html.Div([
                html.Button('Hitting', id='Hitting', n_clicks=0 ,className='Hitting'),
                html.Button('Fielding', id='Fielding', n_clicks=0 ,className='Fielding'),
                html.Button('Pitching', id='Pitching', n_clicks=0,className='Pitching')
            ], className='buttonGroup'),

            html.Div(id='basicTableDivWrapper', className='basicTableDivWrapper')
        ], id='basicTableAndDropdownDiv', className='basicTableAndDropdownDiv'),


        ], className='playerContent'),
    ], className="page"),

    #  dt.DataTable(
    #             id='table',
    #             columns=[{"name": i, "id": i, "selectable": True} for i in pivotRelevant.columns],
    #             data=pivotRelevant.to_dict('records'),
    #             style_cell={'font-family':'arial', 'border':'none', 'textAlign': 'left'},
    #             style_as_list_view=True,
    #             style_header = {'display': 'none'}
    #         ),

# Callback for updating basic table
@app.callback(
    [Output('basicTableDivWrapper', 'children'),
    Output('basicTableDorpdown','options'),
    Output('basicTableDorpdown','value')],
    [Input('Hitting','n_clicks'),
    Input('Fielding', 'n_clicks'), 
    Input('Pitching', 'n_clicks')]
    )

def update_table(hittingClicks, fieldingClicks, pitchingClicks):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    deafultdropdown=[] 
    if 'Hitting' in changed_id:
        msg = 'hitting'
        deafultdropdown=['Name', 'Career','G','AB','R','H','TB', '2B','3B','HR','AVG', 'OPS','GO/GA']
    elif 'Fielding' in changed_id:
        msg = 'fielding'
        deafultdropdown=['Name' ,'Career', 'POS','G','GS', 'INN','TC','PO','A','E','DP', 'RF', 'FPCT']
    elif 'Pitching' in changed_id:
        msg = 'pitching'
        deafultdropdown=['Name', 'Career','W','L','G','SVO','IP','H','R','HR','NP', 'IBB','AVG','GO/AO']
    else:
        msg = 'hitting'
        deafultdropdown=['Name', 'Career','G','AB','R','H','TB', '2B','3B','HR','AVG', 'OPS','GO/GA']
    print(msg)
    tableData = getSummedCareerStats(msg)
    basicTableOptions = getOptionsBasicTable(msg) 
    displayedData = tableData.loc[:,deafultdropdown]
    table = html.Div([
        dt.DataTable(
            id='basicTable',
            columns=[{"name": i, "id": i} for i in displayedData.columns],
            sort_action='native',
            data = displayedData.to_dict('records'),
            style_cell={'textAlign': 'left','background-color': '#D3D3D3', 'color':'black'}
        ),
    ], className='basicTableDiv')
    return table, basicTableOptions, deafultdropdown


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
    [Output('imageDiv2', 'children'),
     Output('playerInformation2', 'children')],
    [Input('playerSelection2', 'value'),
     Input('metricToggle', 'value')],
)
def showPlayerInformation2(playerName, toggleValue):
    playerImage = ''
    table = ''
    if playerName:
        myData = rawPlayerData.loc[rawPlayerData['fullName'] == playerName]
        myData.reset_index(drop=True, inplace=True)
        playerImage = html.Img(src=myData['imageLink'].iloc[0])
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
        table = html.Div([
            dt.DataTable(
                id='table',
                columns=[{"name": i, "id": i, "selectable": True} for i in pivotRelevant.columns],
                data=pivotRelevant.to_dict('records'),
                style_cell={'border':'none', 'textAlign': 'left','background-color': '#27282a'},
                style_as_list_view=True,
                style_header = {'display': 'none'},
                
            ),
        ], className="playerInformation2")        
    
    return playerImage, table

# Callback to load player information left
@app.callback(
    [Output('imageDiv', 'children'),
     Output('playerInformation', 'children')],
    [Input('playerSelection1', 'value'),
     Input('metricToggle', 'value')],
)
def showPlayerInformation(playerName, toggleValue):
    playerImage = ''
    table = ''
    if playerName:
        myData = rawPlayerData.loc[rawPlayerData['fullName'] == playerName]
        myData.reset_index(drop=True, inplace=True)
        playerImage = html.Img(src=myData['imageLink'].iloc[0])
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
        table = html.Div([
            dt.DataTable(
                id='table',
                columns=[{"name": i, "id": i, "selectable": False} for i in pivotRelevant.columns],
                data=pivotRelevant.to_dict('records'),
                style_cell={'border':'none', 'textAlign': 'left', 'background-color': '#27282a'},
                style_as_list_view=True,
                style_header = {'display': 'none'}
            ),
        ], className="playerInformation")        
    
    return playerImage, table