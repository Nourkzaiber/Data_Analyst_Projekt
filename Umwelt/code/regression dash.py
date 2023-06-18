import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import statsmodels.api as sm

df_treib = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/treibhausgase_abs.csv')
# df_treib_I90 = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/treibhausgase_I90.csv')
df_NH3 = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NH3.csv')
df_NOX = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NOX.csv')
df_NMVOC = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/NMVOC.csv')
df_PM10 = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/PM10.csv')
df_BIP = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/BIP.csv')
df_demo = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/demo.csv')
df_umweltschutz = pd.read_csv(
    'https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/umweltschutz_abs.csv')

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Vorhersage für Deutschland'),
    html.Label('Luftschadstoff auswählen'),
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
    html.H2('Umweltschutz'),
    dcc.Graph(id='luftschadstoff-umweltschutz-graph'),
    html.Div(id='umwelt-gleichung-output'),

    html.H2('BIP'),
    dcc.Graph(id='luftschadstoff-BIP-graph'),
    html.Div(id='bip-gleichung-output'),

    html.H2('Bevölkerung'),
    dcc.Graph(id='luftschadstoff-demo-graph'),
    html.Div(id='demo-gleichung-output'),
])


# Funktion zur Berechnung der Gleichung der Regressionsgeraden
def berechne_gleichung(x, y, x_label):
    X = sm.add_constant(x)  # Konstante hinzufügen
    regression = sm.OLS(y, X).fit()  # Lineare Regression durchführen
    intercept = regression.params[0]  # Achsenabschnitt
    slope = regression.params[1]  # Steigung
    equation = f'Luftschadstoff = {slope:.2f} * {x_label} + {intercept:.2f}'
    return equation


# Callback-Funktion für die Aktualisierung des Graphen und der Gleichung basierend auf dem Dropdown-Wert
@app.callback(
    Output('luftschadstoff-umweltschutz-graph', 'figure'),
    Output('umwelt-gleichung-output', 'children'),
    Output('luftschadstoff-BIP-graph', 'figure'),
    Output('bip-gleichung-output', 'children'),
    Output('luftschadstoff-demo-graph', 'figure'),
    Output('demo-gleichung-output', 'children'),
    Input('dropdown-selection', 'value')
)
def update_graph(selected_luftschadstoff):
    # Basierend auf dem ausgewählten Luftschadstoff die entsprechenden Daten laden
    if selected_luftschadstoff == 'NH3':
        df_selected = df_NH3
    elif selected_luftschadstoff == 'NOX':
        df_selected = df_NOX
    elif selected_luftschadstoff == 'NMVOC':
        df_selected = df_NMVOC
    elif selected_luftschadstoff == 'PM10':
        df_selected = df_PM10
    elif selected_luftschadstoff == 'Treibhausgase':
        df_selected = df_treib

    # Daten zusammenführen für die Regression
    merged_data_umwelt = pd.merge(df_umweltschutz, df_selected, on='Jahr')
    merged_data_bip = pd.merge(df_BIP, df_selected, on='Jahr')
    merged_data_demo = pd.merge(df_demo, df_selected, on='Jahr')

    # Lineare Regressionen durchführen
    x_umwelt = merged_data_umwelt['Deutschland_x']
    y_umwelt = merged_data_umwelt['Deutschland_y']
    equation_umwelt = berechne_gleichung(x_umwelt, y_umwelt, 'Umweltschutz')

    x_bip = merged_data_bip['Deutschland_x']
    y_bip = merged_data_bip['Deutschland_y']
    equation_bip = berechne_gleichung(x_bip, y_bip, 'BIP')

    x_demo = merged_data_demo['Deutschland_x']
    y_demo = merged_data_demo['Deutschland_y']
    equation_demo = berechne_gleichung(x_demo, y_demo, 'Bevölkerung')

    # Plots erstellen
    fig_umwelt = px.scatter(merged_data_umwelt, x='Deutschland_x', y='Deutschland_y', trendline='ols',
                            # Von Plotly Express: Ordinary Least Squares (OLS) regression Trendlinie
                            labels={'Deutschland_x': 'Umweltschutzausgaben in Mio EUR',
                                    'Deutschland_y': selected_luftschadstoff},
                            title=f'Umweltschutz vs. {selected_luftschadstoff}')

    fig_bip = px.scatter(merged_data_bip, x='Deutschland_x', y='Deutschland_y', trendline='ols',
                         labels={'Deutschland_x': 'BIP in Mio EUR', 'Deutschland_y': selected_luftschadstoff},
                         title=f'BIP vs. {selected_luftschadstoff}')

    fig_demo = px.scatter(merged_data_demo, x='Deutschland_x', y='Deutschland_y', trendline='ols',
                          labels={'Deutschland_x': 'Bevölkerung', 'Deutschland_y': selected_luftschadstoff},
                          title=f'Bevölkerung vs. {selected_luftschadstoff}')
    return fig_umwelt, html.H4('Gleichung der Regressionsgeraden: ' + equation_umwelt,
                               style={'font-size': '14px', 'font-weight': 'bold', 'text-align': 'center'}), \
        fig_bip, html.H4('Gleichung der Regressionsgeraden: ' + equation_bip,
                         style={'font-size': '14px', 'font-weight': 'bold', 'text-align': 'center'}), \
        fig_demo, html.H4('Gleichung der Regressionsgeraden: ' + equation_demo,
                          style={'font-size': '14px', 'font-weight': 'bold', 'text-align': 'center'})


if __name__ == '__main__':
    app.run_server(debug=True)
