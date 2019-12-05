import os
import json
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import numpy as np
import pandas as pd

from src import utils
from src.collect_data import data_collector
from src.proc_time import Process_Time

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dash_app.config.suppress_callback_exceptions = True
app = dash_app.server

from tabs import tab_about
from tabs import tab_timeline
from tabs import tab_timeprog

dash_app.title = 'Data Analysis'
dash_app.layout = html.Div([
    dcc.Tabs(id='tabs-main', value='tab-about', children=[
        dcc.Tab(label='About', value='tab-about'),
        dcc.Tab(label='Timeline', value='tab-timeline'),
        dcc.Tab(label='Explore Data', value='tab-timeprog'),
    ]),
    html.Div(id='tabs-main-content')
])

@dash_app.callback(Output('tabs-main-content', 'children'),
              [Input('tabs-main', 'value')])
def render_content(tab):
    if tab == 'tab-about':
        return tab_about.tab_about_layout
    elif tab == 'tab-timeline':
        return tab_timeline.tab_timeline_layout
    elif tab == 'tab-timeprog':
        return tab_timeprog.tab_timeprog_layout

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-TAB: timeprog-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-

@dash_app.callback(Output('tab-timeprog-D1', 'children'),
                   [Input('tab-timeprog-dataset', 'value')])
def retrieve_dataset(dataset):
    df = data_collector(dataset)
    return df.to_json()

@dash_app.callback(Output('tab-timeprog-y', 'options'),
                   [Input('tab-timeprog-dataset', 'value')])
def make_variable_dropdown(dataset):
    #df_dict = json.loads(df_json)
    cols = utils.dataset2cols[dataset]
    #return  [{'label': i, 'value': i} for i in df_dict.keys()]
    return  [{'label': i, 'value': i} for i in cols]

@dash_app.callback(Output('tab-timeprog-y', 'value'),
                   [Input('tab-timeprog-y', 'options')])
def make_variable_dropdown(options):
    return options[0]['value']

'''
@dash_app.callback(Output('tab-IR-graph', 'figure'),
              [Input('tab-IR-curr-dropdown', 'value'),
               Input('tab-IR-tenor-dropdown', 'value'),
               Input('IR-year-slider', 'value')])
def tab_IR_graph(curr, tenor, date_range):

    t_min, t_max = utils.format_date(date_range)
    M = Preproc_Data(curr=curr, t_ival=[t_min, t_max]).run()
    df = M['{}m_1d'.format(str(tenor))]
    
    traces = []
    traces.append(go.Scattergl(
        x=df['date'],
        y=df['ir'],
        text=df['ir_transf'],
        mode='lines',
        opacity=.5,
        line=dict(color='black', width=3.),
        name='1 day',
    ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Date',},
            yaxis={'title': 'IR',},
            hovermode='closest',
        )
    }

@dash_app.callback(Output('tab-IR-slider', 'children'),
              [Input('tab-IR-curr-dropdown', 'value'),
               Input('tab-IR-tenor-dropdown', 'value')])
def tab_IR_slider(curr, tenor):
    t_min, t_max, t_list = utils.compute_t_range(
      currtag=curr, tenor=[int(tenor)])
    return html.Div(
        dcc.RangeSlider(
            id='IR-year-slider',
            min=t_min,
            max=t_max,
            value=[2010, 2015],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@dash_app.callback(Output('tab-IR-slider-container', 'children'),
              [Input('IR-year-slider', 'value')])
def tab_IR_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)
'''

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-END: TABs-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                
if __name__ == '__main__':
    #dash_app.run_server(host='0.0.0.0', port=8080, debug=False)
    dash_app.run_server(debug=True)
