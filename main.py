import os
import json
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from plotly.subplots import make_subplots
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

#Dataset 1 (top plot) inputs.
@dash_app.callback(Output('tab-tp-ds1-y', 'options'),
                   [Input('tab-tp-ds1', 'value')])
def make_variable_dropdown(dataset):
    cols = utils.dataset2cols[dataset]
    return  [{'label': i, 'value': i} for i in cols]

@dash_app.callback(Output('tab-tp-ds1-y', 'value'),
                   [Input('tab-tp-ds1-y', 'options')])
def make_variable_dropdown(options):
    return options[0]['value']

@dash_app.callback(Output('tab-tp-ds1-z', 'options'),
                   [Input('tab-tp-ds1', 'value')])
def make_colorcode_dropdown(dataset):
    cols = utils.dataset2zoptions[dataset]
    return  [{'label': i, 'value': i} for i in cols]

@dash_app.callback(Output('tab-tp-ds1-z', 'value'),
                   [Input('tab-tp-ds1-z', 'options')])
def make_variable_dropdown(options):
    return options[0]['value']


#Dataset 2 (bottom plot) inputs.
@dash_app.callback(Output('tab-tp-ds2-y', 'options'),
                   [Input('tab-tp-ds2', 'value')])
def make_variable_dropdown(dataset):
    cols = utils.dataset2cols[dataset]
    return  [{'label': i, 'value': i} for i in cols]

@dash_app.callback(Output('tab-tp-ds2-y', 'value'),
                   [Input('tab-tp-ds2-y', 'options')])
def make_variable_dropdown(options):
    return options[0]['value']

@dash_app.callback(Output('tab-tp-ds2-z', 'options'),
                   [Input('tab-tp-ds2', 'value')])
def make_colorcode_dropdown(dataset):
    cols = utils.dataset2zoptions[dataset]
    return  [{'label': i, 'value': i} for i in cols]


@dash_app.callback(Output('tab-tp-ds2-z', 'value'),
                   [Input('tab-tp-ds2-z', 'options')])
def make_variable_dropdown(options):
    return options[0]['value']

@dash_app.callback(Output('tab-tp-graph', 'figure'),
              [Input('tab-tp-ds1', 'value'),
               Input('tab-tp-ds1-y', 'value'),
               Input('tab-tp-ds1-z', 'value'),
               Input('tab-tp-ds2', 'value'),
               Input('tab-tp-ds2-y', 'value'),
               Input('tab-tp-ds2-z', 'value'),
               Input('pg-slider', 'value'),])
def tab_IR_graph(ds1, y1, z1, ds2, y2, z2, date_range):

    fig = make_subplots(rows=2, cols=1)
    t_min, t_max = utils.format_date(date_range)

    df1 = data_collector(ds1)   
    df2 = data_collector(ds2)   

    df1 = df1[((df1['Start_time_obj'] > t_min) & (df1['Start_time_obj'] < t_max))]
    df2 = df2[((df2['Start_time_obj'] > t_min) & (df2['Start_time_obj'] < t_max))]

    #df1, df2 = utils.trim_time(df1, df2)
    if z1 == 'None':
        fig.append_trace(go.Scattergl(
            x=df1['Start_time_obj'],
            y=df1[y1],
            mode='markers',
            opacity=1.,
            marker=dict(size=5),
            name=ds1,
        ), row=1, col=1)
    
    else:
        for i in df1[z1].unique():
            dff = df1[df1[z1] == i]
            fig.append_trace(go.Scattergl(
                x=dff['Start_time_obj'],
                y=dff[y1],
                mode='markers',
                opacity=1.,
                marker=dict(size=5),
                name=str(i),
            ), row=1, col=1)


    #Bottom plot, df2
    if z2 == 'None':
        fig.append_trace(go.Scattergl(
            x=df2['Start_time_obj'],
            y=df2[y2],
            mode='markers',
            opacity=1.,
            marker=dict(size=5),
            name=ds2,
        ), row=2, col=1)
    
    else:
        for i in df2[z2].unique():
            dff = df2[df2[z2] == i]
            fig.append_trace(go.Scattergl(
                x=dff['Start_time_obj'],
                y=dff[y2],
                mode='markers',
                opacity=1.,
                marker=dict(size=5),
                name=str(i),
            ), row=2, col=1)        
    

    fig.update_yaxes(title_text=y1, row=1, col=1)
    fig.update_xaxes(title_text='Date', row=2, col=1)
    fig.update_yaxes(title_text=y2, row=2, col=1)

    fig.update_layout(height=700)
    return fig
 

@dash_app.callback(Output('tab-pg-slider', 'children'),
              [Input('tab-tp-ds1', 'value'),
               Input('tab-tp-ds2', 'value')])
def tab_pg_slider(ds1, ds2):
    df1 = data_collector(ds1)   
    df2 = data_collector(ds2)   
    t_min, t_max, t_list = utils.trim_time(df1, df2)

    return html.Div(
        dcc.RangeSlider(
            id='pg-slider',
            min=t_min,
            max=t_max,
            value=[t_min, t_max],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  
'''

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
