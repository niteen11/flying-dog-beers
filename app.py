import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_json('https://data.cityofnewyork.us/resource/nwxe-4ae8.json?$limit=10000')

df_copy = df;

app.layout = html.Div([
    html.Div([
    dcc.Dropdown(id='drop-down',style={'height': '30px'},
                     options=[
                         {'label': 'All', 'value': 'all'},
                         {'label': 'Bronx', 'value': 'bronx'},
                         {'label': 'Brooklyn', 'value': 'brooklyn'},
                         {'label': 'Manhattan', 'value': 'manhattan'},
                         {'label': 'Queens', 'value': 'queens'},
                         {'label': 'Staten Island', 'value': 'staten'}
                     ],
                     value='all'
                     ),
            html.Div(id='data-filter')
    ]),

    html.Div([html.H6('DATA 608 - CUNY MSDS - Niteen Kumar'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Tree Health', value='tab-1-example'),
        dcc.Tab(label='Tree Steward', value='tab-2-example'),
    ]),
    html.Div(id='tabs-content-example')
    ])
])

# @app.callback(
#     dash.dependencies.Output('data-filter', 'children'),
#     [dash.dependencies.Input('drop-down', 'value')])

def filter_data(dropdown):
    # return html.Div(['You have selected "{}"'.format(dropdown)])
    if dropdown == 'bronx':
        df_copy = df[df['boroname'] == 'Bronx'].copy()
    elif dropdown == 'brooklyn':
        df_copy = df[df['boroname'] == 'Brooklyn'].copy()
    elif dropdown == 'queens':
        df_copy = df[df['boroname'] == 'Queens'].copy()
    elif dropdown == 'staten':
        df_copy = df[df['boroname'] == 'Staten Island'].copy()
    elif dropdown == 'manhattan':
        df_copy = df[df['boroname'] == 'Manhattan'].copy()
    else:
        df_copy = df.copy()
    return df_copy.to_json(orient='split')

@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value'),
               Input('drop-down', 'value')
               ])

def render_content(tab,dropdown):
    if tab == 'tab-1-example':
        print('success')
        print(dropdown)
        df_boro_filter = filter_data(dropdown=dropdown)
        df_data = pd.read_json(df_boro_filter, orient='split')
        df_health = df_data.groupby(['health', 'spc_common'])[['tree_id']].count().reset_index().copy()
        good = df_health[df_health['health'] == 'Good']
        fair = df_health[df_health['health'] == 'Fair']
        poor = df_health[df_health['health'] == 'Poor']
        return html.Div([
            # html.H3('Tree Health Variable - Good, Fair, Poor for '),
            html.H3(['Tree Health Variable - Good, Fair, Poor for {}'.format(str(dropdown).upper())]),
            dcc.Graph(
                id='graph-1-tabs',
                figure={
                    'data': [go.Bar(x=good['spc_common'],
                                    y=good['tree_id'],
                                    name='Good', marker={'color': '#1abf51'}),
                             go.Bar(x=fair['spc_common'],
                                    y=fair['tree_id'],
                                    name='Fair', marker={'color': '#e8d31e'}),

                             go.Bar(x=poor['spc_common'],
                                    y=poor['tree_id'],
                                    name='Poor', marker={'color': '#a31010'})

                             ],
                            'layout': go.Layout(
                                barmode='stack',
                                xaxis=dict(title='Trees'),
                                yaxis=dict(title='number of trees'),
                            )
                }
            )
        ])
    elif tab == 'tab-2-example':
        print('success')
        print(dropdown)
        df_boro_filter = filter_data(dropdown=dropdown)
        df_st_data = pd.read_json(df_boro_filter, orient='split')
        df_steward = df_st_data.groupby(['steward', 'health'])[['tree_id']].count().reset_index().copy()
        good = df_steward[df_steward['health'] == 'Good']
        fair = df_steward[df_steward['health'] == 'Fair']
        poor = df_steward[df_steward['health'] == 'Poor']
        return html.Div([
            # html.H3('Tree Health Variable - Good, Fair, Poor for '),
            html.H3(['Tree Steward Variable - {}'.format(str(dropdown).upper())]),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [go.Bar(x=good['steward'],
                        y=good['tree_id'],
                        name='Good',
                        marker={'color': '#1abf51'}),

                             go.Bar(x=fair['steward'],
                                    y=fair['tree_id'],
                                    name='Fair',
                                    marker={'color': '#e8d31e'}),

                             go.Bar(x=poor['steward'],
                                    y=poor['tree_id'],
                                    name='Poor',
                                    marker={'color': '#a31010'})
                             ],
                    'layout': go.Layout(
                        barmode='stack',
                        xaxis=dict(title='stewardship'),
                        yaxis=dict(title='number of trees'),
                    )
                }
            )
        ])

if __name__ == '__main__':
    app.run_server()
