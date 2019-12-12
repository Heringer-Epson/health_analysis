import dash_html_components as html
import dash_core_components as dcc
import src.utils as utils

datasets = utils.dataset2fname.keys()

tab_hist_layout = html.Div([

    #Top variable panel
    html.Div([
        html.H6(
            'Histogram View',
            style={'marginLeft': '3em', 'font-weight':'bold'}
        ),
     
        html.H6('Dataset:', style={'marginLeft': '3.0em', }),
        dcc.Dropdown(
            id='tab-hist-ds',
            options=[{'label': i, 'value': i} for i in datasets],
            value='Sleep',
            style={'width': '150px', 'marginLeft': '.5em'}
        ),  
       
        html.H6('y-variable:', style={'marginLeft': '3em'}),
        dcc.Dropdown(id='tab-hist-y', style={'width': '150px', 'marginLeft': '.5em'}),   

    ], style={'display': 'flex', 'marginTop': '1.5em'}), 

    #Graph.
    html.Div([
        dcc.Graph(id='tab-hist-graph'),
    ], style={'width': '95%', 'marginTop': '1em'}),

    #Time slider and text below it.
    html.Div([
        html.Div(
            id='tab-hist-slider',
            style={'width': '95%', 'marginTop': '1em'}
            ),
    ], style={'marginBottom': 25, 'marginLeft': 100, 'marginRight': 100}),

    html.Div(
        id='tab-hist-slider-container',
        style={'textAlign': 'center'},),
        

])  

