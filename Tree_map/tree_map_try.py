import plotly.offline as pyo
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import plotly.graph_objs as go
import squarify

import pandas as pd
import numpy as np

app = dash.Dash()
#server = app.server
#app.config.supress_callback_exceptions = True


### Read data ###
df = pd.read_csv('test_data_treemap.csv')

###### Get options for selection ###########

# from the loaded data set df

#county_options = df['Location'].unique()
county_options = []
for ll in df['Location'].unique():
    county_options.append({'label':'{}'.format(ll), 'value':ll})

#year_options = df['Year'].unique()
year_options = []
for y in df['Year'].unique():
    year_options.append({'label':'{}'.format(y), 'value':y})

#age_options = df['Age'].unique()
age_options = []
for ag in df['Age'].unique():
    age_options.append({'label':'{}'.format(ag), 'value':ag})

#gender_options = df['Sex'].unique()
gender_options = []
for g in df['Sex'].unique():
    gender_options.append({'label':'{}'.format(g), 'value':g})


####### Layout of the dashboard ######

app.layout = html.Div([
    html.H1('Treemaps Dashboard example',style={'marginLeft':'20px'}),

    html.Div([
        html.H3('Select Location:', style={'paddingRight':'0px'}),
        dcc.Dropdown(
            id='my_county_symbol',
            options=county_options,
            #value='Taiwan',
            placeholder='Select a location...',
            multi=False
        )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%','marginLeft':'20px'}),

    html.Div(),

    html.Div([
        html.H3('Select Year:', style={'paddingRight':'0px'}),
        dcc.Dropdown(
            id='my_year_symbol',
            options=year_options,
            #value='Taiwan',
            placeholder='Select a year...',
            multi=False
        )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%','marginLeft':'20px'}),

    html.Div(),

    html.Div([
        html.H3('Select Age:', style={'paddingRight':'0px'}),
        dcc.Dropdown(
            id='my_age_symbol',
            options=age_options,
            #value='Taiwan',
            placeholder='Select an age group...',
            multi=False
        )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%','marginLeft':'20px'}),

    html.Div(),

    html.Div([
        html.H3('Select Gender:', style={'paddingRight':'0px'}),
        dcc.Dropdown(
            id='my_gender_symbol',
            options=gender_options,
            #value='Taiwan',
            placeholder='Select a gender...',
            multi=False
        )
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%','marginLeft':'20px'}),

    html.Div(),

    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit and plot!',
            style={'fontSize':20, 'marginLeft':'20px'}
        ),
    ], style={'display':'inline-block','width':'30%','marginTop':'20px'}),

    html.Div(),

    html.Div([
        dcc.Graph(
            id='my_graph',
            figure={
                'data': [
                    {'x': [], 'y': []}
                    ],
                    'layout':
                    {"title": "Select location(s) and time period and start plotting",
                    "height": 720,
                    "width": 200},  # px
                    }
                    ),
    ], style = {'display':'inline-block','marginLeft':'0px','width':'50%'}
    ),

    #html.Div(),

'''
    html.Div([
        dcc.Graph(
            id='my_graph2',
            figure={
                'data': [
                    {'x': [], 'y': []}
                    ],
                    'layout':
                    {"title": "This is a bar chart",
                    "height": 720,
                    "width": 200},  # px

                    }
                    ),
    ], style = {'display':'inline-block','marginLeft':'0px','width':'50%'}
    ),
'''
])


@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_county_symbol','value'),
    State('my_year_symbol', 'value'),
    State('my_age_symbol', 'value'),
    State('my_gender_symbol', 'value'),
    State('my_graph', 'figure')])

def update_graph(n_clicks, county, year, age, gender, figure):

    selected_data = df[(df['Location']==county) & (df['Year']==year) & (df['Age']==age) & (df['Sex']==gender)]
    selected_data.set_index('Disease',inplace=True) # set the disease type to be the index to call, not sure if it's a good idea


    Year = selected_data['Year'].unique()
    Gender = selected_data['Sex'].unique()
    Age = selected_data['Age'].unique()

    #Dict_data = {}
    #for disease in selected_data.index:
    #    Dict_data[disease] = selected_data.loc[county]


    ## Put things into the graph.

#    NOTE: There will/should be a section that categorize disease type into say three groups.
#    A specific color should be assigned to each categoryself.




    x = 0.
    y = 0.
    width = 100.
    height = 100.

    #values = [500, 433, 78, 25, 25, 7]
    values = selected_data['Value']

    normed = squarify.normalize_sizes(values, width, height)
    rects = squarify.squarify(normed, x, y, width, height)

    # Choose colors from http://colorbrewer2.org/ under "Export"
    color_brewer = ['rgb(166,206,227)','rgb(31,120,180)','rgb(227,26,28)']
    shapes = []
    annotations = []
    counter = 0

    for r in rects:
        shapes.append(
            dict(
                type = 'rect',
                x0 = r['x'],
                y0 = r['y'],
                x1 = r['x']+r['dx'],
                y1 = r['y']+r['dy'],
                line = dict( width = 2 ),
                fillcolor = color_brewer[counter]
            )
        )
        annotations.append(
            dict(
                x = r['x']+(r['dx']/2),
                y = r['y']+(r['dy']/2),
                text = values[counter],
                showarrow = False
            )
        )
        counter = counter + 1
        if counter >= len(color_brewer):
            counter = 0

    figure = {
    'data': [go.Scatter(
        x = [ r['x']+(r['dx']/2) for r in rects ],
        y = [ r['y']+(r['dy']/2) for r in rects ],
        text = [ str(v) for v in values ],
        mode = 'text',
        )
    ],
    'layout': go.Layout(
        height=700,
        width=700,
        xaxis={'showgrid':False, 'zeroline':False, 'showticklabels': False},
        yaxis={'showgrid':False, 'zeroline':False, 'showticklabels': False},
        shapes=shapes,
        annotations=annotations,
        hovermode='closest',
        )
    }
    return figure

if __name__ == '__main__':
    app.run_server(debug=True,host='127.0.0.1',port='8003')
