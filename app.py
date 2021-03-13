import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('hta.csv')


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#fig = px.area(df, x="Year", y="Snow_Percent")

fig = px.line(df, x="Year", y="Snow_Percent", title='Placeholder')

fig['layout']['yaxis']['autorange'] = "reversed"

app.title = 'ChronosZoi' 

app.layout = html.Div([


    
    html.H1("ChronosZoi 2021", style={'text-align': 'center'}),

    html.Div([
    dcc.Input(
        id='input-field',
        type='text',
        placeholder='Enter snow depth',
    ),
    ], style = {'width': '100%', 'display': 'flex-box', 'align-items': 'center', 'justify-content': 'center'}),


    html.H3(id='output-header', style={'text-align': 'center'}),


    dcc.Graph(id='my_bee_map', figure=fig, style={'text-align': 'center'}),

    html.Div([
    daq.Thermometer(
        label='Sea Surface Temperature',
        labelPosition='top',
        id='my-thermometer',
        min=0,
        max=12,
        showCurrentValue=True,
        color='red',
        style={
            'margin-bottom': '5%',
            'backgroundColor': 'transparent'
        }
    ),
    ], style = {'width': '100%', 'display': 'inline-block', 'align-items': 'left', 'justify-content': 'left'}),


    html.Div([
    daq.Gauge(
    id='my-gauge',
    color={'gradient':True, "ranges":{"green":[0.39, 1],"yellow":[0.24, 0.39],"red":[0, 0.24]}},
    #color="#9B51E0",
    label='Chlorophyll',
    max=1,
    min=0,
    ),
    ], style = {'width': '100%', 'display': 'inline-block', 'align-items': 'right', 'justify-content': 'right'}),

  

    html.Div(id='slider-output-container'),
    dcc.Slider(
        id='thermometer-slider',
        #marks={str(Year): str(Year) for Year in df['Year'].unique()},
        value=1,
        min=1976,
        max=2100,    


    ),

])




@app.callback(
    dash.dependencies.Output('my-thermometer', 'value'),
    dash.dependencies.Output(component_id='my-gauge', component_property='value'),
    dash.dependencies.Output('slider-output-container', 'children'),
    [dash.dependencies.Input('thermometer-slider', 'value')])
def update_thermometer(value):
    global yr
    yr = value
    a = df[df['Year'] == value]
    b = float(a['T_Anomaly'].values)
    c = float(a['Chlorophyll'].values)
    d = 'Year {}'.format(value)
    return b, c, d

@app.callback(
    dash.dependencies.Output('output-header','children'),
    [dash.dependencies.Input('input-field','value')]
)
def update_header(prop):
    prop = float(prop)
    row = df[df['Year'] == yr]
    snow_percent = float(row['Snow_Decimals'].values)
    res_str = str(round(prop*snow_percent, 2)) 
    result = res_str + " cm in the year " + str(yr)
    return result



if __name__ == '__main__':
    app.run_server(debug=True)

