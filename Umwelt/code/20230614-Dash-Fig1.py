import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df_treib = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/treibhausgase_abs.csv')
df_treib_I90 = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/treibhausgase_I90.csv')
df_NH3 = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NH3.csv')
df_NOX = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NOX.csv')
df_NMVOC = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NMVOC.csv')
df_PM10 = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/PM10.csv')
df_BIP = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/BIP.csv')
df_demo = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/demo.csv')
df_umweltschutz = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/umweltschutz_abs.csv')


df_BIP['Jahr'] = pd.to_datetime(df_BIP['Jahr'])  # Nach dem Exportieren war "Jahr" nicht mehr im datetime-Format
df_demo['Jahr'] = pd.to_datetime(df_demo['Jahr'])
# print(df_demo.dtypes)
# print(df_demo)

liste_laender = df_NH3.columns[2:].tolist()  # für die Checkliste

dataframes = {          # hier können alle Schadstoffe oder sonstiges eingefügt werden
    'Treibhausgase': df_treib,
    'NH3': df_NH3,
    'NMVOC': df_NMVOC,
    'NOX': df_NOX,
    'PM10': df_PM10
}

### Für das Balken Diagramm
werte = df_treib.iloc[-1, 2:].tolist()  # Werte für das Jahr 2020 (letzte Zeile) als Liste
laender = df_treib.columns[2:].tolist()  # Spaltenüberschriften als Liste

df_sorted = pd.DataFrame({'Werte': werte, 'Länder': laender}).sort_values(by='Werte', ascending=True)  # Sortieren nach den Werten

fig_balken = px.bar(x=df_sorted['Werte'], y=df_sorted['Länder'], orientation='h')
fig_balken.update_traces(marker_color=['red' if land == 'Deutschland' else 'darkblue' if land == 'EU27_2020' else 'lightgrey' for land in df_sorted['Länder']])
fig_balken.update_layout(xaxis_title='Tonnen pro Kopf in 2020', yaxis_title='Länder')
fig_balken.add_vline(x=df_sorted.loc[df_sorted['Länder'] == 'EU27_2020', 'Werte'].values[0], line_dash='dash', line_color='white')

### endet hier, Balken2 beginnt

eu27_2020_value = werte[laender.index('EU27_2020')]  # Wert von EU27_2020
# print(eu27_2020_value)
werte_modified = [wert - eu27_2020_value for wert in werte]  # Von jedem Wert den Wert von EU27_2020 abziehen
# print(werte_modified)
df_modified = pd.DataFrame({'Werte': werte_modified, 'Länder': laender})  # DataFrame mit den modifizierten Werten erstellen
# print(df_modified)
df_sorted = df_modified.sort_values(by='Werte', ascending=True)

fig_balken2 = px.bar(df_sorted, x='Werte', y='Länder', orientation='h')
fig_balken2.update_traces(marker_color=['red' if land == 'Deutschland' else 'lightgrey' for land in df_sorted['Länder']])
fig_balken2.update_layout(xaxis_title='Differenz zu EU27_2020 in Tonnen pro Kopf', yaxis_title='Länder')
### endet hier

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Luftschadstoffe Linien'),
    dcc.Dropdown(
        options=[
            {'label': 'Treibhausgase', 'value': 'Treibhausgase'},
            {'label': 'NH3', 'value': 'NH3'},
            {'label': 'NMVOC', 'value': 'NMVOC'},
            {'label': 'NOX', 'value': 'NOX'},
            {'label': 'PM10', 'value': 'PM10'}
        ],
        value='NH3',
        id='dropdown-selection'
    ),
    dcc.Graph(id='graph-schadstoff'),
    dcc.Checklist(id='checkliste', options=[{'label': land, 'value': land} for land in liste_laender], value=['Deutschland', 'EU27_2020'], inline=True),

    html.Div([
        html.H4('Luftschadstoffe Scatter'),
        dcc.Dropdown(
            options=[
                {'label': 'NH3', 'value': 'NH3'},
                {'label': 'NMVOC', 'value': 'NMVOC'},
                {'label': 'NOX', 'value': 'NOX'},
                {'label': 'PM10', 'value': 'PM10'},
                {'label': 'Treibhausgase', 'value': 'Treibhausgase'},
            ],
            value='NH3',
            id='dropdown-selection2'
        ),
        dcc.RadioItems(
            options=[
                {'label': 'Bevölkerung', 'value': 'demo'},
                {'label': 'BIP', 'value': 'BIP'}
            ],
            value='demo',
            id='yaxis-type'
        ),
        dcc.Graph(id='graph-scatter'),
        dcc.Slider(
            step=None,
            id='year--slider',
            value=df_demo['Jahr'].dt.year.max(),
            marks={str(year): str(year) for year in df_demo['Jahr'].dt.year.unique()}
        ),

        html.Div([
            html.H4('Änderung der Treibhausgase bezogen auf 1990'),
            dcc.Graph(id='graph-index90')]
        ),

        html.Div([
            html.H4('Balkendiagramm Treibhausgase pro Kopf'),
            dcc.Graph(figure=fig_balken)]
        ),

        html.Div([
            html.H4('Differenz zum EU27 Schnitt Treibhausgase pro Kopf'),
            dcc.Graph(figure=fig_balken2)]
        )
    ])
])


@app.callback(
    Output('graph-schadstoff', 'figure'),
    Input('dropdown-selection', 'value'),
    Input('checkliste', 'value')
)
def update_graph(value, selected_land):
    dataframe = dataframes.get(value)
    if dataframe is not None:
        fig = px.line()
        for land in selected_land:
            fig.add_scatter(x=dataframe['Jahr'], y=dataframe[land], mode='lines', name=land, showlegend=True)
        fig.update_yaxes(title_text='in t')
        return fig


@app.callback(
    Output('graph-scatter', 'figure'),
    Input('dropdown-selection2', 'value'),
    Input('yaxis-type', 'value'),
    Input('year--slider', 'value')
)
def update_graph(value, yaxis_type, year_value):
    x_dataframe = dataframes.get(value)
    year_value = pd.to_datetime(year_value, format='%Y')  # Konvertiere das Jahr in den richtigen Datumsformat
    if yaxis_type == 'demo':
        y_dataframe = df_demo[df_demo['Jahr'] == year_value]
    else:
        y_dataframe = df_BIP[df_BIP['Jahr'] == year_value]
    if x_dataframe is not None and not y_dataframe.empty:  # Überprüfe, ob y_dataframe nicht leer ist
        fig = px.scatter()
        for land in x_dataframe.columns[2:]:
            marker_color = 'red' if land == 'Deutschland' else 'lightblue'
            fig.add_scatter(x=x_dataframe[land], y=y_dataframe[land], mode='markers', name=land,
                            marker_color=marker_color)
        return fig


@app.callback(
    Output('graph-index90', 'figure'),
    Input('checkliste', 'value')
)
def greenhouse_index(selected_land):
    fig = px.line()
    for land in selected_land:
        fig.add_scatter(x=df_treib_I90['Jahr'], y=df_treib_I90[land], mode='lines', name=land, showlegend=True)
        fig.update_yaxes(title_text='Ausstoß bezogen auf 1990')
        fig.add_hline(y=100, line_dash="dash", line_color="black")
    return fig




if __name__ == '__main__':
    app.run_server(debug=True)
