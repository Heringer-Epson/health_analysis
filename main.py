import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#My routines.
from src.routine_test import Inp_Pars

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dash_app.config.suppress_callback_exceptions = True
app = dash_app.server

dash_app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        This is Dash running on Google App Engine.
    '''),

    html.H6('Currency:', style={'marginLeft': '3.0em', }),
    dcc.Dropdown(
        id='tab-test',
        options=[{'label': i, 'value': i} for i in ['USD', 'CAD']],
        value='USD',
        style={'width': '100px', 'marginLeft': '.5em'},
    ),

    html.Div(
        id='printer',
        style={'textAlign': 'center'},),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization' + str(Inp_Pars.T_sim)
            }
        }
    )
])

@dash_app.callback(Output('printer', 'children'),
              [Input('tab-test', 'value')])
def tab_func(curr):
    return 'Currency is "{}'.format(curr)

if __name__ == '__main__':
    dash_app.run_server(debug=True)
