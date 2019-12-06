import dash_html_components as html
import dash_core_components as dcc
import base64

img_path = './images/pexels_data-analysis.jpeg'
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
    html.Div([

        html.Div([

            #Left panel.
            html.Div([
                dcc.Markdown(
                    """
                    ###### OVERVIEW
                    This web app analyzes data collected from a health app
                    and provides interactive plots that allow for data exploration
                    and figures that summarize relevant trends.

                    Based on the trends I find, I infer the person's routine,
                    location, job, age, and gender. This section will be deployed
                    in the near future.
                    
                    &nbsp;&nbsp;&nbsp;&nbsp;
                    
                    ###### DATA
                    The data is comprised by a series of csv files collected
                    from multiple devices, but all regarding the same person.
                    The time period spans Jun-2016 to Jun-2019.
                    
                    The person is anonymous and the data was sourced ethically.
                    
                    &nbsp;&nbsp;&nbsp;&nbsp;

                    ###### TECHNICAL DETAILS
                    This package was written in Python and deployed on the Google
                    Cloud. Dash/Plotly were used for building the web app.

                    Github source code: https://github.com/Heringer-Epson/health_analysis
                    """,
                    style={'marginLeft': '3em', 'marginTop': '5em'},
                ),      
                
            ], className="six columns"),

            #Right panel.
            html.Div([
                html.Img(
                  src='data:image/png;base64,{}'.format(img_base64),
                  style={'width':'700px', 'height':'600px', 'margin':'auto'}),
                dcc.Markdown(
                    """
                    Image credit: Kevin Ku. Sourced from https://www.pexels.com 
                    """
                )
            ], style={'marginTop': '3em'}, className="six columns"),
     
        ], className="row")
    ])
])   
