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


app.layout = html.Div([


    
    html.H1("ChronosZoi 2021", style={'text-align': 'center'}),

    dcc.Input(
        id='input-field',
        type='text'
    ),

    html.H3(id='output-header'),


    dcc.Graph(id='my_bee_map', figure=fig),


    daq.Thermometer(
        label='Sea Surface Temperature',
        labelPosition='top',
        id='my-thermometer',
        min=0,
        max=12,
        showCurrentValue=True,
        color='red',
        style={
            'margin-bottom': '5%'
        }

    ),

    daq.Gauge(
    id='my-gauge',
    color={"ranges":{"green":[0.39, 1],"yellow":[0.24, 0.39],"red":[0, 0.24]}},
    #color="#9B51E0",
    label='Chlorophyll',
    max=1,
    min=0,
    ),  




    dcc.Slider(
        id='thermometer-slider',
        #marks={str(Year): str(Year) for Year in df['Year'].unique()},
        value=1,
        min=1976,
        max=2100,    


    ),
    html.Div(id='slider-output-container')

])




@app.callback(
    dash.dependencies.Output('my-thermometer', 'value'),
    dash.dependencies.Output(component_id='my-gauge', component_property='value'),
    [dash.dependencies.Input('thermometer-slider', 'value')])
def update_thermometer(value):
    a = df[df['Year'] == value]
    b = float(a['T_Anomaly'].values)
    c = float(a['Chlorophyll'].values)
    return b, c

@app.callback(
    dash.dependencies.Output('output-header','children'),
    [dash.dependencies.Input('input-field','value')]
)
def update_header(prop):
    return prop



if __name__ == '__main__':
    app.run_server(debug=True)



