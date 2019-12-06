import dash_html_components as html
import dash_core_components as dcc

import src.utils as utils

datasets = utils.dataset2fname.keys()

tab_timeline_layout = html.Div([

    html.Div([
        html.Button(
                id='tab-pl-tz',
                n_clicks=1,
                children='Toggle Timezone Changes',
                style={'width': '300px', 'marginLeft': '5em'}),     
        html.Button(
                id='tab-pl-hl',
                n_clicks=1,
                children='Toggle Holiday',
                style={'width': '300px', 'marginLeft': '5em'}),   
    ], style={'display': 'flex', 'marginTop': '1.5em'}), 

    #Graph.
    html.Div([
        dcc.Graph(id='tab-tl-graph'),
    ], style={'width': '100%', 'marginTop': '1em'}),

])  

