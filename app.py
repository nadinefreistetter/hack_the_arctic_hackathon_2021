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

fig = px.line(df, x="Year", y="Snow_Percent")

fig['layout']['yaxis']['autorange'] = "reversed"


app.layout = html.Div([

    html.H1("ChronosZoi 2021", style={'text-align': 'center'}),

    dcc.Graph(id='my_bee_map', figure=fig),


    daq.Thermometer(
        id='my-thermometer',
        value=1,
        min=0,
        max=13,
        showCurrentValue=True,
        style={
            'margin-bottom': '5%'
        }

    ),

    daq.Gauge(
    id='my-gauge',
    color={"gradient":True,"ranges":{"green":[0.4,1],"yellow":[0.25, 0.39],"red":[0, 0.24]}},
    value=2,
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
    [dash.dependencies.Input('thermometer-slider', 'value')])
def update_thermometer(value):
    a = df[df['Year'] == value]
    b = float(a['T_Anomaly'].values)
    return b


if __name__ == '__main__':
    app.run_server(debug=True)

