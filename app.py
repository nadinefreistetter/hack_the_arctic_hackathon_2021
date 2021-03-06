import dash
import dash_daq as daq
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

df = pd.read_csv('hta.csv')

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# fig = px.area(df, x="Year", y="Snow_Percent")

plot_df = df.copy()

plot_df = plot_df.rename(columns={'Snow_Percent': 'Percentage of Snow'})

fig = px.line(plot_df, x="Year", y="Percentage of Snow", title='Placeholder')

fig.update_layout(title='Percentage of snow over the years compared to the cold climate (1961 - 1990)',
                  yaxis_title='Percentage of Snow', )

fig['layout']['yaxis']['autorange'] = "reversed"

app.title = 'ChronosZoi'

app.layout = html.Div([

    html.Img(src=app.get_asset_url('SvalbardIMG1.jpg'), style={'width': '100%'}),

    html.Br(),

    html.H1("ChronosZoi 2021 Web Application: Trends in the Svalbard area visualised.", style={'text-align': 'center'}),

    html.Br(),

    html.P("Welcome to this Web Application. With this tool, you can see what trends are going on in the Svalbard area."
           " Here, you can select any year between 1976 (first observations) and 2100 (end of the century), to see how"
           " the observed and forecasted trends are for the temperature, snow depth and water quality.",
           style={'text-align': 'center'}),

    html.Br(),
    html.Br(),

    daq.Slider(
        id='thermometer-slider',
        min=1976,
        max=2100,
        value=1976,
        handleLabel={"showCurrentValue": True, "label": "Year"},
        step=1,
        size=1500,
    ),

    html.Br(),
    html.Br(),

    html.P("The average amount of snowfall in the Svalbard area is decreasing. "
           "Here below, you can add any value, representing the snow depth in the old climate of Svalbard (around 1976)."
           "The text below will show how that number has changed over the years.",
           style={'text-align': 'center'}),

    html.Div([
        dcc.Input(
            id='input-field',
            type='text',
            placeholder='Enter snow depth (cm)',
            style={'width': '100%', 'align-items': 'center', 'justify-content': 'center', 'text-align': 'center'}
        ),
    ], style={'width': '100%', 'align-items': 'center', 'justify-content': 'center'}),

    html.H3(id='output-header', style={'text-align': 'center'}),

    dcc.Graph(id='my_bee_map', figure=fig, style={'text-align': 'center'}),

    html.Img(src=app.get_asset_url('SvalbardIMG2.jpg'), style={'width': '100%'}),

    html.Br(),
    html.Br(),

    html.P("The Svalbard area is one of the fastest-warming places on Earth and this trend is forecasted to continue. "
           "The thermometer below shows the temperature anomaly compared to the 30-year average of 1961 - 1990.",
           style={'text-align': 'center'}),

    html.H3(id='output-thermometer-header', style={'text-align': 'center'}),

    html.Div([
        daq.Thermometer(
            label='Temperature anomaly',
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
    ], style={'width': '100%', 'display': 'inline-block', 'align-items': 'left', 'justify-content': 'left'}),

    html.Img(src=app.get_asset_url('SvalbardIMG3.jpg'), style={'width': '100%'}),

    html.Br(),
    html.Br(),

    html.P("Chlorophyll in the ocean pulls carbon dioxide out of the water (and the atmosphere) and enriches it with"
           " oxygen. Furthermore, it is the primary food source for countless creatures on the bottom of the food"
           " chain. Therefore, higher concentrations are generally seen as good and a lack of chlorophyll"
           " (among other caused by rising ocean temperatures, lack of nutrients, lack of light, turbulent"
           " water or other changes in the water chemistry) therefore is a threat to all marine life.",
           style={'text-align': 'center'}),

    html.Br(),

    html.Div([
        daq.Gauge(
            id='my-gauge',
            color={'gradient': True, "ranges": {"green": [0.39, 1], "yellow": [0.24, 0.39], "red": [0, 0.24]}},
            # color="#9B51E0",
            label='Chlorophyll concentration',
            max=1,
            min=0,
        ),
    ], style={'width': '100%', 'display': 'inline-block', 'align-items': 'right', 'justify-content': 'right'}),

    html.Div(id='slider-output-container'),

html.A(html.Button('Refresh Data / Select a new year', style={'width':'1500px','align-text':'center'}),href='/'),

])

@app.callback(
    dash.dependencies.Output('my-thermometer', 'value'),
    dash.dependencies.Output(component_id='my-gauge', component_property='value'),
    dash.dependencies.Output('slider-output-container', 'children'),
    dash.dependencies.Output('output-thermometer-header', 'children'),
    [dash.dependencies.Input('thermometer-slider', 'value')])
def update_thermometer(value):
    global yr
    yr = value
    a = df[df['Year'] == value]
    b = float(a['T_Anomaly'].values)
    t_anom = (str(round(b, 1)))
    c = float(a['Chlorophyll'].values)
    d = ''
    temp_out = "The temperature is about " + t_anom + "??C higher in " + str(yr) + " than around 1976."
    return b, c, d, temp_out


@app.callback(
    dash.dependencies.Output('output-header', 'children'),
    [dash.dependencies.Input('input-field', 'value')]
)
def update_header(prop):
    prop = float(prop)
    row = df[df['Year'] == yr]
    snow_percent = float(row['Snow_Decimals'].values)
    res_str = str(round(prop * snow_percent, 1))

    first_row = df[df['Year'] == 1976]
    first_snow_percent = float(first_row['Snow_Decimals'].values)
    first_res_str = str(abs(round(prop * snow_percent, 1) - round(prop * first_snow_percent, 1)))

    result = "It will be around " + res_str + " cm in the year " + str(
        yr) + ", which is " + first_res_str + " cm lower than the year 1976."
    return result


if __name__ == '__main__':
    app.run_server(debug=True)
