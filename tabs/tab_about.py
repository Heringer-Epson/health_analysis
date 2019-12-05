import dash_html_components as html
import dash_core_components as dcc
import base64

img_path = './images/timeline.png'
img_base64 = base64.b64encode(open(img_path, 'rb').read()).decode('ascii')

tab_about_layout = html.Div([
    
    #Header and authorship.
    html.Div([
        html.H3(
            'Data Analysis',
            style={'font-weight':'bold'}
        ),
        html.H3(
            'v(1.0.0)',
            style={'marginLeft': '0.75em'}
        ),    
    ], style={'display': 'flex', 'marginLeft': '3em', 'marginTop': '1.5em'}),
    
    html.H6(
        'by Epson Heringer',
        style={'marginLeft': '4em', 'marginTop': '-1em', 'font-style':'italic'}
    ),

    #Body.
    #E.g. https://community.plot.ly/t/two-graphs-side-by-side/5312
    html.Div([

        html.Div([

            #Left panel.
            html.Div([
                dcc.Markdown(
                    """
                    ###### OVERVIEW
                    This web app analyzes data collected from a health app
                    and provides interactive plots that summarize relevant trends.

                    #Target questions.
                    
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    
                    ###### DATA
                    The data is comprised by a colection ... from multiple devices,
                    spanning Jun-2016 to Jun-2019.
                    
                    &nbsp;&nbsp;&nbsp;&nbsp;

                    ###### TECHNICAL DETAILS
                    This package was written in Python and deployed on the Google
                    Cloud. Dash/Plotly were used for building the web app.

                    Github source code: https://github.com/Heringer-Epson/health_analysis
                    """,
                    style={'marginLeft': '3em'},
                ),      
                
            ], className="six columns"),

            #Right panel.
            html.Div([
                html.Img(
                  src='data:image/png;base64,{}'.format(img_base64),
                  style={'width':'700px', 'height':'800px', 'margin':'auto'}),

            ], style={'marginTop': '-5em'}, className="six columns"),
        ], className="row")
    ])
])   
