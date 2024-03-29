import os
import json
import dash
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import numpy as np
import pandas as pd

from src import utils
from src.collect_data import data_collector
from src.proc_time import Process_Time, holidays_list_str

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
dash_app.config.suppress_callback_exceptions = True
app = dash_app.server

from tabs import tab_about
from tabs import tab_timeline
from tabs import tab_timeprog
from tabs import tab_hist
from tabs import tab_week

dash_app.title = 'Data Analysis'
dash_app.layout = html.Div([
    dcc.Tabs(id='tabs-main', value='tab-about', children=[
        dcc.Tab(label='About', value='tab-about'),
        dcc.Tab(label='Timeline', value='tab-timeline'),
        dcc.Tab(label='Explore Data', value='tab-timeprog'),
        dcc.Tab(label='Histograms', value='tab-hist'),
        dcc.Tab(label='Weekly', value='tab-week'),
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
    elif tab == 'tab-hist':
        return tab_hist.tab_hist_layout
    elif tab == 'tab-week':
        return tab_week.tab_week_layout

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-TAB: timeprog-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-

@dash_app.callback(Output('tab-tl-graph', 'figure'),
              [Input('tab-pl-tz', 'n_clicks'),
               Input('tab-pl-hl', 'n_clicks'),])
def tab_tl_graph(tog_tz, tog_hl):

    traces = []

    #Give an order when plotting the info from the loaded json file.
    df_names = ['Sleep', 'Exercise', 'Stress', 'Step', 'Heart', 'Floors',
                'Calories', 'Summary']
    with open('./outputs/time_collection.json', 'r') as inp:
        M = json.load(inp)

    for i, name in enumerate(df_names):
        timef = M[name]    
        traces.append(go.Scattergl(
            x=timef,
            y=(i + 1) * np.ones(len(timef)),
            mode='markers',
            opacity=.7,
            marker=dict(size=2),
            showlegend=False
    ))

    #Plot Timeline.
    fig = go.Figure(data = traces,
                    layout = dict(
                        xaxis={'title': 'Date',},
                        hovermode='closest'))

    #Toggle tz_change.
    if tog_tz % 2 == 0:
        for i, t in enumerate(M['tz_change_dates']):             
            fig.add_shape(
                    go.layout.Shape(
                        type='line', xref='x', yref='paper', x0=t, x1=t,
                        y0=0, y1=1, opacity=0.3,
                        line=dict(color='LightSeaGreen', width=2, dash='dash'),
                    ))

    if tog_hl % 2 == 0:
        for i, t in enumerate(M['date_holidays']):             
            fig.add_shape(
                    go.layout.Shape(
                        type='line', xref='x', yref='paper', x0=t, x1=t,
                        y0=0, y1=1, opacity=0.3,
                        line=dict(color='firebrick', width=2, dash='dot'),
                    ))

    #Improve fig ticks.
    fig.update_layout(
        xaxis = dict(
            tickmode = 'array',
            tickvals = np.arange(2016.5, 2019.51, 0.5),
            ticktext = ['June 2016', 'Jan. 2017', 'June 2017', 'Jan. 2018',
                        'June 2018', 'Jan. 2019', 'June 2019']),
        yaxis = dict(
            tickmode = 'array',
            tickvals = np.arange(0, len(df_names) + 1.1, 1),
            ticktext = [''] + df_names + ['']),
        height=650,
        margin=go.layout.Margin(b=20,t=10)
    )
    return fig

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
               Input('pg-slider', 'value'),
               Input('tab-pg-tz', 'n_clicks'),])
def tab_tl_graph(ds1, y1, z1, ds2, y2, z2, date_range, tog_tz):

    fig = make_subplots(rows=2, cols=1, vertical_spacing = 0.05)
    t_min, t_max = utils.format_date(date_range)

    df1 = data_collector(ds1)   
    df2 = data_collector(ds2)   

    df1 = df1[((df1['Start_time_obj'] > t_min) & (df1['Start_time_obj'] < t_max))]
    df2 = df2[((df2['Start_time_obj'] > t_min) & (df2['Start_time_obj'] < t_max))]

    if z1 == 'None':
        fig.append_trace(go.Scattergl(
            x=df1['Start_time_obj'],
            y=df1[y1],
            mode='markers',
            opacity=1.,
            marker=dict(size=5),
            showlegend=False
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
            showlegend=False
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

    #Toggle Timezone changes.
    if tog_tz % 2 == 0:
        if 'time_offset' in df1.columns: 
            tz_list = utils.make_tz_changers(df1, 'date', 'time_offset')
            for i, t in enumerate(tz_list):
                fig.add_shape(
                        go.layout.Shape(
                            type='line', x0=t.replace('/', '-'), x1=t.replace('/', '-'),
                            y0=0, y1=1,
                            line=dict(color='LightSeaGreen', width=2, dash='dot',),
                        ), row=1, col=1)
                fig.layout.shapes[i]['yref']='paper'
    
    fig.update_yaxes(title_text=y1, row=1, col=1)
    fig.update_xaxes(title_text='Date', row=2, col=1)
    fig.update_yaxes(title_text=y2, row=2, col=1)
    fig.update_layout(
        height=650,
        margin=go.layout.Margin(b=20,t=10),)
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

@dash_app.callback(Output('tab-pg-slider-container', 'children'),
              [Input('pg-slider', 'value')])
def tab_IR_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)


#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-TAB: histogram-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=

#Dataset 1 (top plot) inputs.
@dash_app.callback(Output('tab-hist-y', 'options'),
                   [Input('tab-hist-ds', 'value')])
def make_variable_dropdown(dataset):
    cols = utils.dataset2cols[dataset]
    return  [{'label': i, 'value': i} for i in cols]

@dash_app.callback(Output('tab-hist-y', 'value'),
                   [Input('tab-hist-y', 'options')])
def make_variable_dropdown(options):
    return options[0]['value']

@dash_app.callback(Output('tab-hist-graph', 'figure'),
              [Input('tab-hist-ds', 'value'),
               Input('tab-hist-y', 'value'),
               Input('hist-slider', 'value'),])
def tab_tl_graph(ds, y, date_range):
    t_min, t_max = utils.format_date(date_range)
    df = data_collector(ds)   
    dff = df[((df['Start_time_obj'] > t_min) & (df['Start_time_obj'] < t_max))]
    aux_df = dff[[y]]
    fig = px.histogram(dff, x=y)
    return fig

@dash_app.callback(Output('tab-hist-slider', 'children'),
              [Input('tab-hist-ds', 'value')])
def tab_pg_slider(ds):
    df = data_collector(ds)   
    t_min, t_max, t_list = utils.trim_time(df, df)

    return html.Div(
        dcc.RangeSlider(
            id='hist-slider',
            min=t_min,
            max=t_max,
            value=[t_min, t_max],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@dash_app.callback(Output('tab-hr-slider-container', 'children'),
              [Input('hr-slider', 'value')])
def tab_IR_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-TAB: histogram-=-=-=--=-=-=-=-=-=-=-=-=-=-=-=

#Dataset 1 (top plot) inputs.
@dash_app.callback(Output('tab-week-y', 'options'),
                   [Input('tab-week-ds', 'value')])
def make_variable_dropdown(dataset):
    cols = utils.dataset2cols[dataset]
    return  [{'label': i, 'value': i} for i in cols]

@dash_app.callback(Output('tab-week-y', 'value'),
                   [Input('tab-week-y', 'options')])
def make_variable_dropdown(options):
    return options[0]['value']

@dash_app.callback(Output('tab-week-graph', 'figure'),
              [Input('tab-week-ds', 'value'),
               Input('tab-week-y', 'value'),
               Input('week-slider', 'value'),])
def tab_tl_graph(ds, y, date_range):
    t_min, t_max = utils.format_date(date_range)
    df = data_collector(ds)   
    dff = df[((df['Start_time_obj'] > t_min) & (df['Start_time_obj'] < t_max))]
    aux_df = dff[[y]]
    fig = px.box(dff, x='weekday_num', y=y)

    fig.update_layout(
        xaxis = dict(
            title='Day of the Week',
            tickmode = 'array',
            tickvals = [1, 2, 3, 4, 5, 6, 7],
            ticktext = [
                'Sunday', 'Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday', 'Saturday']),
    )
    return fig

@dash_app.callback(Output('tab-week-slider', 'children'),
              [Input('tab-week-ds', 'value')])
def tab_pg_slider(ds):
    df = data_collector(ds)   
    t_min, t_max, t_list = utils.trim_time(df, df)

    return html.Div(
        dcc.RangeSlider(
            id='week-slider',
            min=t_min,
            max=t_max,
            value=[t_min, t_max],
            marks={year: str(year) for year in t_list},
            step=1./12.
        )
    )  

@dash_app.callback(Output('tab-week-slider-container', 'children'),
              [Input('week-slider', 'value')])
def tab_IR_slider_container(date_range):
    t_min, t_max = utils.format_date(date_range)
    return 'Date range is "{}" -- "{}"'.format(t_min, t_max)

#=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-END: TABs-=-=--=-=-=-=-=-=-=-=-=-=-=-=-=-=-
                                
if __name__ == '__main__':
    dash_app.run_server(host='0.0.0.0', port=8050, debug=False)
    #dash_app.run_server(debug=True)
