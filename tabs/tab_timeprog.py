import dash_html_components as html
import dash_core_components as dcc

datasets = ['Sleep-1', 'Sleep-2', 'Exercise'] 

tab_timeprog_layout = html.Div([
    
    html.Div([

        html.Div([

            #Left panel.
            html.Div([
                dcc.Markdown(
                    """
                    ###### OVERVIEW
                    BLURB.
                    """,
                    style={'marginLeft': '3em'},
                ),      
            ], className="six columns"),

            #Right panel.
            html.Div([
            
                html.Div([
                    dcc.Dropdown(
                        id='tab-timeprog-dataset',
                        options=[{'label': i, 'value': i} for i in datasets],
                        value='Sleep-1'
                    ),
                    dcc.Dropdown(
                        id='tab-timeprog-y',
                        options=[{'label': i, 'value': i} for i in datasets],
                        value='duration'
                    ),
                ],
                style={'width': '25%', 'display': 'inline-block'}),

                html.Div([
                    dcc.Dropdown(
                        id='tab-timeprog-z',
                        options=[{'label': i, 'value': i} for i in datasets],
                        value='exercise-type'
                    ),
                ],style={'width': '25%', 'float': 'right', 'display': 'inline-block'})
            ], style={'marginTop': '3em'}),

            #dcc.Graph(id='indicator-graphic'),

            #dcc.Slider(
            #    id='year--slider',
            #    min=df['Year'].min(),
            #    max=df['Year'].max(),
            #    value=df['Year'].max(),
            #    marks={str(year): str(year) for year in df['Year'].unique()},
            #    step=None
            #)
            #],  className="six columns"),
        
        
        
        
        
        
        ], className="row")
    ]),
   
    #Hidden tab for expensive calculation of matrix of paths for forward days.
    html.Div(id='tab-timeprog-D1', style={'display': 'none'})

])  
