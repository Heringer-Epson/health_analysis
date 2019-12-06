import dash_html_components as html
import dash_core_components as dcc

import src.utils as utils

datasets = utils.dataset2fname.keys()

tab_timeprog_layout = html.Div([

    #Top variable panel
    html.Div([
        html.H6(
            'Top Plot',
            style={'marginLeft': '3em', 'font-weight':'bold'}
        ),
     
        html.H6('Dataset:', style={'marginLeft': '3.0em', }),
        dcc.Dropdown(
            id='tab-tp-ds1',
            options=[{'label': i, 'value': i} for i in datasets],
            value='Sleep',
            style={'width': '150px', 'marginLeft': '.5em'}
        ),  
       
        html.H6('y-variable:', style={'marginLeft': '3em'}),
        dcc.Dropdown(id='tab-tp-ds1-y', style={'width': '150px', 'marginLeft': '.5em'}),

        html.H6('color-code:', style={'marginLeft': '3em'}),
        dcc.Dropdown(id='tab-tp-ds1-z', style={'width': '150px', 'marginLeft': '.5em'}),

        html.Button(
                id='tab-pg-tz',
                n_clicks=1,
                children='Toggle Timezone Changes',
                style={'width': '300px', 'marginLeft': '5em'}),     

    ], style={'display': 'flex', 'marginTop': '1.5em'}), 

    #Bottom variable panel
    html.Div([
        html.H6(
            'Bot Plot',
            style={'marginLeft': '3em', 'font-weight':'bold'}
        ),
     
        html.H6('Dataset:', style={'marginLeft': '3.0em', }),
        dcc.Dropdown(
            id='tab-tp-ds2',
            options=[{'label': i, 'value': i} for i in datasets],
            value='Exercise',
            style={'width': '150px', 'marginLeft': '.5em'}
        ),  
       
        html.H6('y-variable:', style={'marginLeft': '3em'}),
        dcc.Dropdown(id='tab-tp-ds2-y', style={'width': '150px', 'marginLeft': '.5em'}),

        html.H6('color-code:', style={'marginLeft': '3em'}),
        dcc.Dropdown(id='tab-tp-ds2-z', style={'width': '150px', 'marginLeft': '.5em'})

    ], style={'display': 'flex', 'marginTop': '-0.5em'}), 

    #Graph.
    html.Div([
        dcc.Graph(id='tab-tp-graph'),
    ], style={'width': '95%', 'marginTop': '1em'}),

    #Time slider and text below it.
    html.Div([
        html.Div(
            id='tab-pg-slider',
            style={'width': '95%', 'marginTop': '1em'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-pg-slider-container',
        style={'textAlign': 'center'},),
        

])  

