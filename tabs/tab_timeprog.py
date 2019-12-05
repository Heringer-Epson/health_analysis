import dash_html_components as html
import dash_core_components as dcc

import src.utils as utils

datasets = ['Sleep-1', 'Exercise'] 

tab_timeprog_layout = html.Div([
    
    html.Div([
        
        html.Div([
            dcc.Dropdown(
                id='tab-tp-ds1',
                options=[{'label': i, 'value': i} for i in datasets],
                value='Sleep-1'
            ),
            dcc.Dropdown(id='tab-tp-ds1-y'),
            dcc.Dropdown(id='tab-tp-ds1-z'),               
        ],
        style={'width': '25%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='tab-tp-ds2',
                options=[{'label': i, 'value': i} for i in datasets],
                value='Exercise'
            ),
            dcc.Dropdown(id='tab-tp-ds2-y'),
            dcc.Dropdown(id='tab-tp-ds2-z'),               
        ],
        style={'width':'25%', 'display':'inline-block', 'marginTop': '1em'}),
    
    ], style={'textAlign': 'center'}),

    html.Div([
        dcc.Graph(id='tab-tp-graph'),
    ], style={'width': '95%', 'marginTop': '0em'}),

    html.Div([
        html.Div(
            id='tab-pg-slider',
            style={'width': '100%'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),


        

])  
