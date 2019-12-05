import dash_html_components as html
import dash_core_components as dcc
import base64

img_path = './images/timeline.png'
img_base64 = base64.b64encode(open(img_path, 'rb').read()).decode('ascii')

tab_timeline_layout = html.Div([
    
    #Header and authorship.
    html.Div([
        html.H6(
            'Simulating future intrabank rates',
            style={'font-weight':'bold'}
        ),
    ], style={'display': 'flex', 'marginLeft': '3em', 'marginTop': '1.5em'}),

    #Body.
    #E.g. https://community.plot.ly/t/two-graphs-side-by-side/5312
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
                html.Img(
                  src='data:image/png;base64,{}'.format(img_base64),
                  style={'width':'700px', 'height':'400px', 'margin':'auto'}),

            ],  className="six columns"),
        ], className="row")
    ])
])   
