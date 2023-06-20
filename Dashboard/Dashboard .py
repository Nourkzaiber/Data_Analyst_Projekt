import numpy as np
import pandas as pd
import dash
from dash import html, Input, Output, dcc, dash_table
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score


# ---------------------------------------------------------------------------------------------

def fig_bevoelk(val_years):
    raw_data = pd.read_csv('https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/allgemein/ausgangdaten/12411-0005.csv',
                           skiprows=6, nrows=87, encoding='ISO-8859-1', sep=';')
    data = raw_data.copy()
    data.columns = ['Altersjahre', '31.12.2017', '31.12.2018', '31.12.2019', '31.12.2020', '31.12.2021']
    data = data[data['Altersjahre'] != 'Insgesamt']

    if val_years == []:
        indx_years = [1, 3]
    else:
        indx_years = []
        for i in range(0, len(data.columns)):
            if data.columns[i][-2:] == str(val_years[0]) or data.columns[i][-2:] == str(val_years[-1]):
                indx_years.append(i)

    # Datenvisualisierung
    if len(indx_years) > 1:
        fig_bev02 = px.line(data, x='Altersjahre', y=data.columns[indx_years[0]:indx_years[1] + 1], markers=True)
    else:
        fig_bev02 = px.line(data, x='Altersjahre', y=data.columns[indx_years[0]], markers=True)

    fig_bev02.update_layout(title="Altersverteilung der deutschen Bevölkerung",
                            xaxis_title='Altersjahre',
                            yaxis_title='Bevölkerung',
                            showlegend=True)

    return [data, fig_bev02]


# ---------------------------------------------------------------------------------------------

def fig_gebsterb(vals):
    raw_data_sterbene = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/allgemein/ausgangdaten/12613-0002.csv', skiprows=5,
        nrows=73, encoding='ISO-8859-1', delimiter=';')
    raw_data_geborene = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/allgemein/ausgangdaten/Geboren_12612-0001.csv',
        skiprows=5, nrows=73, encoding='ISO-8859-1',
        delimiter=';')

    data_geborene = raw_data_geborene.dropna()
    data_sterbene = raw_data_sterbene.dropna()

    data_geborene.rename(columns={'Unnamed: 0': 'Jahr'}, inplace=True)
    data_sterbene.rename(columns={'Unnamed: 0': 'Jahr'}, inplace=True)

    years = data_geborene['Jahr']
    births = data_geborene['Insgesamt']
    deaths = data_sterbene['Insgesamt']
    excess = births - deaths

    fig = px.line(title='Geborene, Gestorbene und Geburtenüberschuss über die Jahre')
    if vals == []:
        vals = ["Geburtenzahl", "Sterbezahl"]
    if len(vals) == 1 and vals[0] == "Geburtenzahl":
        fig.add_scatter(x=years, y=births, mode='lines', name='Geborene')
    elif len(vals) == 1 and vals[0] == "Sterbezahl":
        fig.add_scatter(x=years, y=deaths, mode='lines', name='Gestorbene')
    else:
        fig.add_scatter(x=years, y=births, mode='lines', name='Geborene')
        fig.add_scatter(x=years, y=deaths, mode='lines', name='Gestorbene')
        fig.add_bar(x=years, y=excess, name='Geburtenüberschuss')

    fig.update_layout(
        xaxis_title='Jahr',
        yaxis_title='Anzahl',
        legend_title='Kategorie',
        showlegend=True
    )
    return [data_geborene, data_sterbene, fig]


# ---------------------------------------------------------------------------------------------

def fig_bev_wanderung(vals):
    raw_data = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/allgemein/ausgangdaten/wanderungen-deutschland-ausland-monate.csv',
        encoding='ISO-8859-1', delimiter=';')

    # Spaltennamen anpassen
    raw_data.columns = ['Monat', 'Zuzüge aus dem Ausland', 'Fortzüge ins Ausland', 'Wanderungssaldo']

    # Daten konvertieren
    raw_data['Zuzüge aus dem Ausland'] = raw_data['Zuzüge aus dem Ausland'].str.replace(',', '.').astype(float)
    raw_data['Fortzüge ins Ausland'] = raw_data['Fortzüge ins Ausland'].str.replace(',', '.').astype(float)
    raw_data['Wanderungssaldo'] = raw_data['Wanderungssaldo'].str.replace(',', '.').astype(float)

    # Datum als Index verwenden
    raw_data['Datum'] = pd.to_datetime(raw_data['Monat'])
    raw_data.set_index('Datum', inplace=True)

    fig = px.bar(title='Wanderungen über die Grenzen Deutschlands')
    if vals == []:
        vals = ['Zuzüge aus dem Ausland', 'Fortzüge ins Ausland']
    if len(vals) == 1 and vals[0] == 'Zuzüge aus dem Ausland':
        fig.add_scatter(x=raw_data.index, y=raw_data['Zuzüge aus dem Ausland'], mode='lines',
                        name='Zuzüge aus dem Ausland')
    elif len(vals) == 1 and vals[0] == 'Fortzüge ins Ausland':
        fig.add_scatter(x=raw_data.index, y=raw_data['Fortzüge ins Ausland'], mode='lines', name='Fortzüge ins Ausland')
    else:
        fig = px.bar(data_frame=raw_data, x=raw_data.index, y='Wanderungssaldo',
                     labels={'x': 'Datum', 'Wanderungssaldo': 'Anzahl'},
                     title='Wanderungen über die Grenzen Deutschlands')

        # Linien für Zuzüge aus dem Ausland und Fortzüge ins Ausland hinzufügen
        fig.add_scatter(x=raw_data.index, y=raw_data['Zuzüge aus dem Ausland'], mode='lines',
                        name='Zuzüge aus dem Ausland')
        fig.add_scatter(x=raw_data.index, y=raw_data['Fortzüge ins Ausland'], mode='lines', name='Fortzüge ins Ausland')

    # Layout anpassen
    fig.update_layout(
        xaxis=dict(tickangle=45),
        legend_title_text=None
    )

    return [raw_data, fig]


# ---------------------------------------------------------------------------------------------
def bev_homoehen_fig():
    # Daten einlesen
    data = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/allgemein/ausgangdaten/gleichgeschlechtliche-eheschliessungen.csv',
        delimiter=';', encoding='ISO-8859-1')

    # Spaltennamen anpassen
    data.columns = ['Jahr', 'zwischen Männern', 'zwischen Frauen']
    # print(data)

    # Gesamtzahl berechnen
    data['Gesamt'] = data['zwischen Männern'] + data['zwischen Frauen']

    fig = px.bar(data_frame=data, x="Jahr", y="Gesamt",
                 labels={'Jahr': 'Jahr', 'Gesamt': 'Anzahl'},
                 title="Zahl der gleichgeschlechtlichen Eheschließungen")

    # Linien für Zuzüge aus dem Ausland und Fortzüge ins Ausland hinzufügen
    fig.add_scatter(x=data["Jahr"], y=data['zwischen Männern'], mode='lines',
                    name='Zwischen Männern')
    fig.add_scatter(x=data["Jahr"], y=data['zwischen Frauen'], mode='lines',
                    name='Zwischen Frauen')

    # Layout anpassen
    fig.update_layout(
        xaxis=dict(tickangle=45),
        legend_title_text=None
    )
    return fig


# ---------------------------------------------------------------------------------------------
def bev_ehen_fig():
    # Daten einlesen
    data = pd.read_csv('https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/allgemein/ausgangdaten/12611-0001.csv',
                       skiprows=6, nrows=73, encoding='ISO-8859-1', delimiter=';')
    data.columns = ['Jahr', 'Anzahl', 'Prozent']

    # Plot erstellen
    fig = px.line(data_frame=data, x='Jahr', y='Anzahl', title='Eheschließungen im Zeitverlauf',
                  labels={'Jahr': 'Jahr', 'Anzahl': 'Anzahl'}, markers=True)

    # Layout anpassen
    fig.update_layout(yaxis_range=[0, 1000000])

    # Achsenticks anpassen
    fig.update_xaxes(tickangle=45)
    return fig


# ---------------------------------------------------------------------------------------------

def fig_gebmon(vals):
    # Daten einlesen
    data = pd.read_csv('https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/allgemein/ausgangdaten/12612-0002.csv',
                       skiprows=5, nrows=50, encoding='ISO-8859-1', delimiter=';')
    data.rename(columns={'Unnamed: 0': 'Jahr', 'Unnamed: 1': 'Monat'}, inplace=True)

    # Reihenfolge der Monate festlegen
    month_order = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober',
                   'November', 'Dezember']

    # Monat als kategorische Variable mit der gewünschten Reihenfolge festlegen
    data['Monat'] = pd.Categorical(data['Monat'], categories=month_order, ordered=True)

    # Datenvisualisierung mit Plotly Express
    fig = px.line(data_frame=data, x='Monat', y='Insgesamt', color='Jahr',
                  labels={'Monat': 'Monat', 'Insgesamt': 'Anzahl Lebendgeborene', 'Jahr': 'Jahr'},
                  title='Lebendgeborene nach ausgewählten Monaten (pro Jahr)')

    fig.update_traces(mode='lines+markers', marker=dict(size=5))

    fig.update_layout(
        yaxis=dict(range=[30000, 90000]),  # Y-Achse auf Bereich 0-75000 begrenzen
        legend_title_text=None,
        showlegend=True
    )

    return [data, fig]


# ---------------------------------------------------------------------------------------------

def fig_erwquo():
    # Daten einlesen
    raw_data = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/allgemein/ausgangdaten/erwerbstaetigkeit-eltern.csv',
        encoding='ISO-8859-1', delimiter=';', skiprows=1,
        names=['Jahr', 'Mütter', 'Väter'])

    # Umwandlung der Spalten in numerische Werte
    raw_data['Mütter'] = raw_data['Mütter'].str.replace(',', '.').astype(float)
    raw_data['Väter'] = raw_data['Väter'].str.replace(',', '.').astype(float)

    fig = px.line(raw_data, x='Jahr', y=['Mütter', 'Väter'], title='Erwerbstätigenquote von Müttern und Vätern')
    fig.update_layout(
        xaxis_title='Jahr',
        yaxis_title='Erwerbstätigenquote',
        legend_title='Geschlecht'
    )
    return fig


# ---------------------------------------------------------------------------------------------

def fig_bev_regr_erwerb():
    # Daten einlesen
    raw_data = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/allgemein/ausgangdaten/erwerbstaetigkeit-eltern.csv',
        encoding='ISO-8859-1', delimiter=';', skiprows=1,
        names=['Jahr', 'Mütter', 'Väter'])

    # Umwandlung der Spalten in numerische Werte
    raw_data['Mütter'] = raw_data['Mütter'].str.replace(',', '.').astype(float)

    # X und y Variablen für die Regression erstellen
    X = sm.add_constant(raw_data['Jahr'])  # Konstante hinzufügen
    y = raw_data['Mütter']

    # Lineare Regression erstellen
    model = sm.OLS(y, X)
    results = model.fit()
    # print(results.summary())
    # ylre = -999.5238 +0.5137*X
    # Vorhersage für zukünftige Werte
    future_years = np.arange(2022, 2030)  # Annahme für die nächsten 8 Jahre
    future_X = sm.add_constant(future_years)
    predictions = results.predict(future_X)

    df_pred = pd.DataFrame({'Jahre': future_years, 'Quote': predictions})
    raw_data["fitted_mut"] = results.fittedvalues.values

    # Daten und Regressionlinie plotten
    fig = px.scatter(data_frame=raw_data, x='Jahr', y='Mütter', title='Erwerbstätigenquote von Müttern')
    fig.add_trace(go.Scatter(x=df_pred["Jahre"], y=df_pred["Quote"], name="Vorhersage"))
    fig.add_trace(go.Scatter(x=raw_data["Jahr"], y=raw_data["fitted_mut"], name="Regression"))
    fig.update_layout(
        xaxis_title='Jahr',
        yaxis_title='Erwerbstätigenquote'
    )

    # Vorhersagewerte ausgeben
    future_predictions = pd.DataFrame({'Jahr': future_years, 'Vorhersage': predictions})
    print(future_predictions)

    # Berechnung des R²-Werts
    predicted_values = results.predict()
    r2 = r2_score(raw_data['Mütter'], predicted_values)
    print("Bestimmtheitsmaß (R²):", r2)
    return fig


# ---------------------------------------------------------------------------------------------

def figure_01_ea():
    # Datenimport
    # pfad = "file://localhost/D:/alexc/Documents/2023_Alfatraining/Modul_5_DataAnalyst/Tag 9/4364_Autoverkaufsdaten_dataPreprocessing_cleaning.csv"
    # raw_data = pd.read_csv(pfad)

    data_fig1 = np.linspace(0, 10, 100)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=data_fig1, y=np.sin(data_fig1), mode='lines', name='Sinus'))
    fig1.add_trace(go.Scatter(x=data_fig1, y=np.cos(data_fig1), mode='lines', name='Kosinus'))

    return (fig1)


# ---------------------------------------------------------------------------------------------

def dashboard():
    ######## Daten Umwelt ################
    df_treib = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Umwelt/data%20preprocessing/treibhausgase_abs.csv')
    df_treib_I90 = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Umwelt/data%20preprocessing/treibhausgase_I90.csv')
    df_NH3 = pd.read_csv('https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Umwelt/data%20preprocessing/NH3.csv')
    df_NOX = pd.read_csv('https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Umwelt/data%20preprocessing/NOX.csv')
    df_NMVOC = pd.read_csv('https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Umwelt/data%20preprocessing/NMVOC.csv')
    df_PM10 = pd.read_csv('https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Umwelt/data%20preprocessing/PM10.csv')
    df_BIP = pd.read_csv('https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Umwelt/data%20preprocessing/BIP.csv')
    df_demo = pd.read_csv('https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Umwelt/data%20preprocessing/demo.csv')
    df_umweltschutz = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Umwelt/data%20preprocessing/umweltschutz_abs.csv')

    df_BIP['Jahr'] = pd.to_datetime(df_BIP['Jahr'])  # Nach dem Exportieren war "Jahr" nicht mehr im datetime-Format
    df_demo['Jahr'] = pd.to_datetime(df_demo['Jahr'])
    # print(df_demo.dtypes)
    # print(df_demo)

    liste_laender = df_treib.columns[2:].tolist()  # für die Checkliste

    dataframes = {  # hier können alle Schadstoffe oder sonstiges eingefügt werden
        'Treibhausgase': df_treib,
        'NH3': df_NH3,
        'NMVOC': df_NMVOC,
        'NOX': df_NOX,
        'PM10': df_PM10
    }

    ### Für das Balken Diagramm
    werte = df_treib.iloc[-1, 2:].tolist()  # Werte für das Jahr 2020 (letzte Zeile) als Liste
    laender = df_treib.columns[2:].tolist()  # Spaltenüberschriften als Liste

    df_sorted = pd.DataFrame({'Werte': werte, 'Länder': laender}).sort_values(by='Werte',
                                                                              ascending=True)  # Sortieren nach den Werten

    fig_balken = px.bar(x=df_sorted['Werte'], y=df_sorted['Länder'], orientation='h')
    fig_balken.update_traces(
        marker_color=['red' if land == 'Deutschland' else 'darkblue' if land == 'EU27_2020' else 'lightgrey' for land in
                      df_sorted['Länder']])
    fig_balken.update_layout(xaxis_title='Tonnen pro Kopf in 2020', yaxis_title='Länder')
    fig_balken.add_vline(x=df_sorted.loc[df_sorted['Länder'] == 'EU27_2020', 'Werte'].values[0], line_dash='dash',
                         line_color='white')

    ### endet hier, Balken2 beginnt

    eu27_2020_value = werte[laender.index('EU27_2020')]  # Wert von EU27_2020
    # print(eu27_2020_value)
    werte_modified = [wert - eu27_2020_value for wert in werte]  # Von jedem Wert den Wert von EU27_2020 abziehen
    # print(werte_modified)
    df_modified = pd.DataFrame(
        {'Werte': werte_modified, 'Länder': laender})  # DataFrame mit den modifizierten Werten erstellen
    # print(df_modified)
    df_sorted = df_modified.sort_values(by='Werte', ascending=True)

    fig_balken2 = px.bar(df_sorted, x='Werte', y='Länder', orientation='h')
    fig_balken2.update_traces(
        marker_color=['red' if land == 'Deutschland' else 'lightgrey' for land in df_sorted['Länder']])
    fig_balken2.update_layout(xaxis_title='Differenz zu EU27_2020 in Tonnen pro Kopf', yaxis_title='Länder')
    ### endet hier

    # ---------------------------------------------------------------------------------------------------------------------

    ###### Mobilität ############

    # Daten einlesen
    data_road = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Mobilit%C3%A4t/Data%20preprocessing/46131-0003_G%C3%BCterverkehr_Stra%C3%9Fe_bearbeitete_daten.csv')
    data_rail = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Mobilit%C3%A4t/Data%20preprocessing/46131-0003_Eisenbahn_bearbeitete_daten.csv')
    data_BIP = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Mobilit%C3%A4t/Data%20preprocessing/81000-0001_BWS%2C%20BIP_bearbeitete_daten.csv')
    merge_BIP_road = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Mobilit%C3%A4t/Data%20preprocessing/merge_BIP_Strasse.csv')
    merge_BIP_rail = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Mobilit%C3%A4t/Data%20preprocessing/merge_BIP_Eisenbahn.csv')
    merge_BIP_road_rail = pd.read_csv(
        'https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Mobilit%C3%A4t/Data%20preprocessing/merge_BIP_Strasse_Eisenbahn.csv')

    ################ Beginn Dash ####################################
    app = dash.Dash(external_stylesheets=[dbc.themes.SPACELAB], suppress_callback_exceptions=True)

    ### Bevölkerungszusammensetzung Subthema Auswahl ###
    dropdown_b01 = dcc.Dropdown(
        ["Geburtenverteilung über das Jahr",
         "Erwerbstätigkeit Eltern",
         "Regression Erwerbstätigkeit Mütter",
         "Migration",
         "Gleichgeschlechtliche Ehen",
         "Ehen nicht gleichgeschlechtlich",
         "Altersverteilung der deutschen Bevölkerung"],
        value="Geburtenverteilung über das Jahr",
        id='subthema_bevoelk')

    z_c03 = dbc.Row(dbc.Col(children=dropdown_b01, width={"size": 10, "offset": 1}))

    z_c04 = dbc.Row(children=[], id="inhalt_geburten")

    s_b02 = dbc.Col(children=[z_c03, html.Br(), z_c04])

    ### Bevölkerungszusammensetzung Hauptthema ###

    datfig = fig_gebsterb([])
    fig_gebstr = datfig[2]
    s_d01 = dbc.Col(dcc.Graph(id="id_fig_bev01", figure=fig_gebstr), md=9)  # , md=4 ### Alterszusammensetzung
    s_d02 = dbc.Col(dcc.Checklist(options=['Geburtenzahl', 'Sterbezahl'],
                                  value=['Geburtenzahl', 'Sterbezahl'],
                                  inline=False,
                                  id="chklst_geburten"), md=3)
    z_c01 = dbc.Row([s_d01, s_d02])

    s_b01 = dbc.Col([z_c01])
    z_a03 = dbc.Row([s_b01, s_b02])

    ### Umwelt Hauptthema ###
    z_e03 = dbc.Row([dcc.Slider(step=None,
                                id='year--slider',
                                value=df_demo['Jahr'].dt.year.max(),
                                marks={str(year): str(year) for year in df_demo['Jahr'].dt.year.unique()}
                                )])  # Slider
    # Graph scatter
    z_e02 = dbc.Row([dcc.Graph(id='graph-scatter')])  # Graph
    z_e01 = dbc.Row([html.H4('Luftschadstoffe in der EU in Bezug zur Einwohnerzahl und BIP')])  # Header
    s_d04 = dbc.Col(
        [dcc.RadioItems(options=[{'label': 'Einwohner', 'value': 'demo'},
                                 {'label': 'BIP', 'value': 'BIP'}],
                        value='demo',
                        id='yaxis-type',
                        labelStyle={'display': 'block'})],
        md=2,
        width={"size": 3, "offset": -1})

    s_d03 = dbc.Col([z_e01, z_e02, z_e03])

    z_d01 = dbc.Row([html.H4('Luftschadstoffe Entwicklung seit 1990')])

    s_d06 = dbc.Col([dcc.Checklist(id='checkliste',
                                   options=[{'label': land, 'value': land} for land in liste_laender],
                                   value=['Deutschland', 'EU27_2020'],
                                   inline=True,
                                   labelStyle={'display': 'block', 'margin-right': '10px'})],
                    md=2,
                    width={"size": 3, "offset": -1})
    # Graph schadstoff
    s_d05 = dbc.Col([z_d01, dcc.Graph(id='graph-schadstoff')],
                    md=10)
    z_c06 = dbc.Row([s_d05, s_d06])

    z_c05 = dbc.Row([s_d03, s_d04])
    s_b04 = dbc.Col([z_c05, html.Br(), z_c06], width={"size": 9})

    s_b03 = dbc.Col(
        [dcc.Dropdown(options=[{'label': 'Treibhausgase', 'value': 'Treibhausgase'},
                               {'label': 'NH3', 'value': 'NH3'},
                               {'label': 'NMVOC', 'value': 'NMVOC'},
                               {'label': 'NOX', 'value': 'NOX'},
                               {'label': 'PM10', 'value': 'PM10'}],
                      value='NH3',
                      id='dropdown-selection')],
        # md=1,
        width={"size": 1, "offset": 1})

    z_b03 = dbc.Row(html.Div([
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
            id='dropdown-selection2'
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
    ]))

    z_b02 = dbc.Row([
        dbc.Col(
            html.Div([
                html.H4('Balkendiagramm Treibhausgase pro Kopf'),
                dcc.Graph(figure=fig_balken, style={'height': '600px'})
            ]),
            width=6,
        ),
        dbc.Col(
            html.Div([
                html.H4('Differenz zum EU27 Schnitt Treibhausgase pro Kopf'),
                dcc.Graph(figure=fig_balken2, style={'height': '600px'})
            ]),
            width=6,
        )
    ])

    z_b01 = dbc.Row([
        dbc.Col(
            html.Div([
                html.H4('Änderung der Treibhausgase bezogen auf 1990'),
                dcc.Graph(id='graph-index90')
            ])
        )
    ])

    z_a04 = dbc.Row([s_b03, s_b04, z_b01, z_b02, z_b03])

    ################## Mobilität ################################ 526 im vgl zu 382

    # Layout der Zeile 1 definieren
    # Straße
    z_b04 = app.layout = dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H4('Beförderungsmenge und -leistung (Straße)'),
                            html.P("Select columns to plot:"),
                            dcc.Dropdown(
                                id='column-dropdown_road',
                                options=[{'label': col, 'value': col} for col in data_road.columns[1:]],
                                value=[],
                                multi=True,
                            ),
                            dcc.Graph(id="graph_road"),
                        ],
                        md=4,
                        width={"size": 2, "offset": 0.5}
                    ),
                    dbc.Col(
                        [
                            html.H4('Beförderungsmenge und -leistung (Schiene)'),
                            html.P("Select columns to plot:"),
                            dcc.Dropdown(
                                id='column-dropdown_rail',
                                options=[{'label': col, 'value': col} for col in data_rail.columns[1:]],
                                value=[],
                                multi=True,
                            ),
                            dcc.Graph(id="graph_rail"),
                        ],
                        md=4,
                        width={"size": 2}
                    ),
                    dbc.Col(
                        [
                            html.H4('Bruttowertschöpfung, Bruttoinlandsprodukt'),
                            html.P("Select columns to plot:"),
                            dcc.Dropdown(
                                id='column-dropdown_BIP',
                                options=[{'label': col, 'value': col} for col in data_BIP.columns[1:]],
                                value=[],
                                multi=True,
                            ),
                            dcc.Graph(id="graph_BIP"),
                        ],
                        md=4,
                        width={"size": 2, "offset": -0.5}
                    ),
                ]
            )
        ]
    )

    # Layout der Zeile 2 definieren
    # BIP_Straße
    s_c04 = dbc.Col([
        html.H4('Linear Regression BIP, Straße'),
        html.P("Wählen Sie die Spalten für die Regression:"),
        html.Label('Unabhängige Variable (x):'),
        dcc.Dropdown(
            id='x-dropdown_BIP_road',
            options=[{'label': col, 'value': col} for col in merge_BIP_road.columns[1:]],
            value=None,
        ),
        html.Label('Abhängige Variable (y):'),
        dcc.Dropdown(
            id='y-dropdown_BIP_road',
            options=[{'label': col, 'value': col} for col in merge_BIP_road.columns[1:]],
            value=None,
        ),
        html.Div(id='regression-results_BIP_road')
    ],
    width={"size": 3, "offset": 2})

    # BIP_Schiene
    s_c05 = dbc.Col([
        html.H4('Linear Regression BIP, Schiene'),
        html.P("Wählen Sie die Spalten für die Regression:"),
        html.Label('Unabhängige Variable (x):'),
        dcc.Dropdown(
            id='x-dropdown_BIP_rail',
            options=[{'label': col, 'value': col} for col in merge_BIP_rail.columns[1:]],
            value=None,
        ),
        html.Label('Abhängige Variable (y):'),
        dcc.Dropdown(
            id='y-dropdown_BIP_rail',
            options=[{'label': col, 'value': col} for col in merge_BIP_rail.columns[1:]],
            value=None,
        ),
        html.Div(id='regression-results_BIP_rail')
    ],
    width={"size": 3, "offset": 2})

    z_b05 = dbc.Row([s_c04, s_c05])

    # Layout der Zeile 3 definieren
    # Multilineare Regression (BIP - Straße - Eisenbahn)
    s_c06 = dbc.Col([
        html.H4('Multiple Regression BIP, Straße, Schiene'),
        html.P("Wählen Sie die Spalten für die Regression:"),
        html.Label('Abhängige Variable (y):'),
        dcc.Dropdown(
            id='y-dropdown_BIP_road_rail',
            options=[{'label': col, 'value': col} for col in merge_BIP_road_rail.columns[1:]],
            value=None,
        ),
        html.Label('Unabhängige Variablen (x):'),
        dcc.Dropdown(
            id='x-dropdown_BIP_road_rail',
            options=[{'label': col, 'value': col} for col in merge_BIP_road_rail.columns[1:]],
            value=[],
            multi=True
        ),
        html.Div(id='regression-results_BIP_road_rail')
    ],
    width={"size": 3, "offset": 4},
    )

    z_b06 = dbc.Row([s_c06])

    z_a05 = dbc.Row([z_b04, z_b05, z_b06])

    ### Hauptfenster ###

    tab1_content = [html.Br(), z_a03]  # Bevölkerungszusammensetzung
    tab2_content = [html.Br(), z_a04]  # Umwelt
    tab3_content = [html.Br(), z_a05]  # Mobilität

    tabs = dbc.Tabs(
        [dbc.Tab("", label="Themen:", disabled=True),
         dbc.Tab(tab1_content, label="Bevölkerungszusammensetzung", tab_id="tab_a01"),
         dbc.Tab(tab2_content, label="Umwelt und Luftemissionen"),  ###### Noch zu ändern
         dbc.Tab(tab3_content, label="Mobilität"),  ###### Noch zu ändern
         ], active_tab="tab_a01")

    z_a02 = dbc.Row(dbc.Col([tabs], width={"size": 12, "offset": 0}))

    # Hauptfenster Zeile 1
    z_a01 = dbc.NavbarSimple(children=
                             [dbc.DropdownMenu(children=
                                               [dbc.DropdownMenuItem("Authors", header=True),
                                                dbc.DropdownMenuItem(divider=True),
                                                dbc.DropdownMenuItem("Esra Aciksöz Werner",
                                                                     href="https://www.linkedin.com/in/esra-aciks%C3%B6z-werner-18a131268/"),
                                                dbc.DropdownMenuItem("Kapila Kasam",
                                                                     href="https://www.linkedin.com/in/kapila-kasam-019181156/"),
                                                dbc.DropdownMenuItem("Marcus Köbe",
                                                                     href="https://www.linkedin.com/in/marcus-koebe/"),
                                                dbc.DropdownMenuItem("Nour-Eddine Kzaiber", href="#"),
                                                dbc.DropdownMenuItem("Peter Thul",
                                                                     href="https://www.linkedin.com/in/peter-thul-659151195/"),
                                                dbc.DropdownMenuItem("Alexander Warmbold",
                                                                     href="https://www.xing.com/profile/Alexander_Warmbold2/portfolio")
                                                ], nav=True, in_navbar=True, label="Team", )
                              ], brand="Dashboard Gruppe B",
                             brand_href="https://www.alfatraining.de")  # , color="primary", dark=True)

    layout_proj = html.Div(children=[z_a01, html.Br(), z_a02], id="GesamtAppLayout")  # Hauptcontainer/Fenster
    app.layout = layout_proj

    ### Callback zu den Subthemen Bevölkerung #### ---------------------------------------------------------------------------------------------

    @app.callback(
        Output("inhalt_geburten", "children"),
        Input("subthema_bevoelk", "value"))
    def count_clicks(n):
        if n == "Geburtenverteilung über das Jahr":
            ### Bevölkerungszusammensetzung Subthema Geburten/Jahr ###
            datafig_b03 = fig_gebmon([])
            fig1 = datafig_b03[1]
            s_d02 = dbc.Col(dcc.Graph(figure=fig1))  # , md=4 ### Alterszusammensetzung

            return [s_d02]

        elif n == "Erwerbstätigkeit Eltern":
            ### Erwerbstätigkeit Eltern ###
            fig1 = fig_erwquo()
            s_d01 = dbc.Col(dcc.Graph(figure=fig1), md=9)  # , md=4 ### Alterszusammensetzung

            return [s_d01]

        elif n == "Regression Erwerbstätigkeit Mütter":
            ### Erwerbstätigkeit Eltern ###
            fig1 = fig_bev_regr_erwerb()
            s_d01 = dbc.Col(dcc.Graph(figure=fig1), md=9)  # , md=4 ### Alterszusammensetzung

            return [s_d01]

        elif n == "Migration":
            ### Migration ###
            # datfig = fig_bev_wanderung([])
            # s_d03 = dbc.Col(dcc.Graph(figure=datfig[1]), md=9, id="id_bev_migr_graph")  # , md=4 ### Migration
            s_d03 = dbc.Col(dcc.Graph(id="id_bev_migr_graph"), md=9)  # , md=4 ### Migration

            s_d07 = dbc.Col(dcc.Checklist(options=['Zuzüge aus dem Ausland', 'Fortzüge ins Ausland'],
                                          value=['Zuzüge aus dem Ausland', 'Fortzüge ins Ausland'],
                                          inline=False,
                                          id="chklst_bev_migr"), md=3)

            return [s_d03, s_d07]

        elif n == "Gleichgeschlechtliche Ehen":
            ### Ehe Gleichgeschlechtlich ###
            fig1 = bev_homoehen_fig()
            s_d05 = dbc.Col(dcc.Graph(figure=fig1), md=9)  # , md=4 ### Ehe Gleichgeschlechtlich

            return [s_d05]  # , s_d06]

        elif n == "Ehen nicht gleichgeschlechtlich":
            ### Ehe Gleichgeschlechtlich ###
            fig1 = bev_ehen_fig()
            s_d05 = dbc.Col(dcc.Graph(figure=fig1), md=9)  # , md=4 ### Ehe Gleichgeschlechtlich

            return [s_d05]  # , s_d06]



        elif n == "Altersverteilung der deutschen Bevölkerung":
            ### Altersverteilung der deutschen Bevölkerung ###
            datenfig_ea01 = fig_bevoelk([])  # Daten Esra A. 01 Bevölkerungszusammensetzung (Figure und Datensatz)
            fig_bev02 = datenfig_ea01[1]
            daten_bev02 = datenfig_ea01[0]

            z_d08 = dbc.Row([dbc.Col([dcc.RangeSlider(min=int(daten_bev02.columns[1][-2:]),
                                                      max=int(daten_bev02.columns[-1][-2:]),
                                                      step=1,
                                                      value=[int(daten_bev02.columns[2][-2:]),
                                                             int(daten_bev02.columns[-2][-2:])],
                                                      marks={
                                                          17: 'Jahr 2017',
                                                          18: 'Jahr 2018',
                                                          19: 'Jahr 2019',
                                                          20: 'Jahr 2020',
                                                          21: 'Jahr 2021'
                                                      },
                                                      # wenn z.B. 2019 als int stehen würde, dann erscheint es als 2k im Graph
                                                      id='my-range-slider01', )])])

            z_d07 = dbc.Col(dcc.Graph(id="id_fig_bev02", figure=fig_bev02), md=9)  # , md=4 ### Alterszusammensetzung

            return [z_d07, z_d08]

        return

    ### Callback zum Hauptthema Bevölkerung (Geboren/Sterben) #### ---------------------------------------------------------------------------------------------

    @app.callback(Output("id_fig_bev01", "figure"),
                  Input("chklst_geburten", "value"))
    def fig_bevoelk01_update(vals):
        datfig = fig_gebsterb(vals)
        fig_gebstr = datfig[2]
        return fig_gebstr

    ### Callback zum Subthema Bevölkerung, Alterszusammenstellung #### ---------------------------------------------------------------------------------------------

    @app.callback(Output("id_fig_bev02", "figure"),
                  Input("my-range-slider01", "value"))
    def fig_bevoelk02_update(slider_values):
        datenfig_ea01 = fig_bevoelk(
            slider_values)  # Daten Esra A. 01 Bevölkerungszusammensetzung (Figure und Datensatz)
        fig = datenfig_ea01[1]
        return fig

    ### Callback zum Subthema Bevölkerung, Migration #### ---------------------------------------------------------------------------------------------
    @app.callback(Output("id_bev_migr_graph", "figure"),
                  Input("chklst_bev_migr", "value"))
    def fig_migr_update(vals):
        datfig = fig_bev_wanderung(vals)
        fig = datfig[1]
        return fig

    ### Callback zum Hauptthema Umwelt, Linienplot #### ---------------------------------------------------------------------------------------------
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
        Input('dropdown-selection', 'value'),
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
        Input('dropdown-selection2', 'value')
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
        df_BIP = pd.read_csv('https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Umwelt/data%20preprocessing/BIP.csv')
        df_demo = pd.read_csv('https://raw.githubusercontent.com/Nourkzaiber/Data_Analyst_Projekt/main/Umwelt/data%20preprocessing/demo.csv')
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
                                # Von Plotly: Ordinary Least Squares (OLS) regression Trendlinie
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

    #################################################### ---------------------------------------------------------------------------------------------

    ############### Mobilität ############################
    # Callback-Funktion für die Aktualisierung des Graphen (Straße)
    @app.callback(
        Output("graph_road", "figure"),
        Input("column-dropdown_road", "value")
    )
    def update_graph(selected_columns):
        # Figure-Objekt erstellen mit einer sekundären Y-Achse
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Schleife über ausgewählte Spalten
        for column in selected_columns:
            if column in data_road.columns[1:12:2]:
                # Falls die Spalte eine ungerade Zahl hat, wird sie auf der primären Y-Achse dargestellt
                fig.add_trace(
                    go.Scatter(x=data_road['Jahr'], y=data_road[column], name=column),
                    secondary_y=False,
                )
            elif column in data_road.columns[2:13:2]:
                # Falls die Spalte eine gerade Zahl hat, wird sie auf der sekundären Y-Achse dargestellt
                fig.add_trace(
                    go.Scatter(x=data_road['Jahr'], y=data_road[column], name=column),
                    secondary_y=True,
                )

        # Layout des Graphen aktualisieren
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        fig.update_layout(title_text="Güterverkehr")
        fig.update_xaxes(title_text="Jahr")
        fig.update_yaxes(title_text="Beförderte Gütermenge in 1000 t", secondary_y=False)
        fig.update_yaxes(title_text="Beförderungsleistung in Mill. TKm", secondary_y=True)

        return fig

    # Callback-Funktion für die Aktualisierung des Graphen (Schiene)
    @app.callback(
        Output("graph_rail", "figure"),
        Input("column-dropdown_rail", "value")
    )
    def update_graph(selected_columns):
        # Figure-Objekt erstellen mit einer sekundären Y-Achse
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Schleife über ausgewählte Spalten
        for column in selected_columns:
            if column in data_rail.columns[1:10:2]:
                # Falls die Spalte eine ungerade Zahl hat, wird sie auf der primären Y-Achse dargestellt
                fig.add_trace(
                    go.Scatter(x=data_rail['Jahr'], y=data_rail[column], name=column),
                    secondary_y=False,
                )
            elif column in data_rail.columns[2:11:2]:
                # Falls die Spalte eine gerade Zahl hat, wird sie auf der sekundären Y-Achse dargestellt
                fig.add_trace(
                    go.Scatter(x=data_rail['Jahr'], y=data_rail[column], name=column),
                    secondary_y=True,
                )

        # Layout des Graphen aktualisieren
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        fig.update_layout(title_text="Güterverkehr")
        fig.update_xaxes(title_text="Jahr")
        fig.update_yaxes(title_text="Beförderte Gütermenge in 1000 t", secondary_y=False)
        fig.update_yaxes(title_text="Beförderungsleistung in Mill. TKm", secondary_y=True)

        return fig

    # Callback-Funktion für die Aktualisierung des Graphen (BIP)
    @app.callback(
        Output("graph_BIP", "figure"),
        Input("column-dropdown_BIP", "value")
    )
    def update_graph(selected_columns):
        # Figure-Objekt erstellen mit einer sekundären Y-Achse
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        # Schleife über ausgewählte Spalten
        for column in selected_columns:
            if column in data_BIP.columns[1:6]:
                # Falls die Spalte eine ungerade Zahl hat, wird sie auf der primären Y-Achse dargestellt
                fig.add_trace(
                    go.Scatter(x=data_BIP['Jahr'], y=data_BIP[column], name=column),
                    secondary_y=False,
                )
            elif column in data_BIP.columns[6:7]:
                # Falls die Spalte eine gerade Zahl hat, wird sie auf der sekundären Y-Achse dargestellt
                fig.add_trace(
                    go.Scatter(x=data_BIP['Jahr'], y=data_BIP[column], name=column),
                    secondary_y=True,
                )

        # Layout des Graphen aktualisieren
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            )
        )

        fig.update_layout(
            title_text="Bruttowertschöpfung, Bruttoinlandsprodukt (nominal/preisbereinigt): Deutschland, Jahre")
        fig.update_xaxes(title_text="Jahr")
        fig.update_yaxes(title_text="(Mrd. EUR)", secondary_y=False)
        fig.update_yaxes(title_text="%", secondary_y=True)

        return fig

    # Callback-Funktion für die Aktualisierung des Graphen (BIP_Strasse)
    @app.callback(
        Output('regression-results_BIP_road', 'children'),
        Input('x-dropdown_BIP_road', 'value'),
        Input('y-dropdown_BIP_road', 'value')
    )
    def linear_regression(x_column, y_column):
        if x_column is not None and y_column is not None:
            x = merge_BIP_road[
                x_column]  # Die unabhängige Variable x (x-Werte) aus dem merge_BIP_road DataFrame extrahieren
            y = merge_BIP_road[
                y_column]  # Die abhängige Variable y (y-Werte) aus dem merge_BIP_road DataFrame extrahieren

            x = sm.add_constant(
                x)  # Eine konstante Spalte zu den x-Werten hinzufügen (für den y-Achsenabschnitt der Regression)

            model = sm.OLS(y,
                           x).fit()  # Eine lineare Regression durchführen: y als abhängige Variable und x als unabhängige Variable

            b0 = model.params[0]  # Der geschätzte Koeffizient für den y-Achsenabschnitt (Intercept)
            b1 = model.params[1]  # Der geschätzte Koeffizient für die Steigung (Slope)
            r_squared = model.rsquared  # Der Bestimmtheitskoeffizient (R-Quadrat) des Regressionsmodells

            y_pred = b0 + b1 * x[
                x_column]  # Die vorhergesagten y-Werte (basierend auf der Regression) für jeden x-Wert berechnen

            # Streudiagramm der Datenpunkte erstellen
            plt.scatter(x[x_column], y)

            # Regressionsgerade zeichnen
            plt.plot(x[x_column], y_pred, color='orange', linewidth=3)

            # Achsenbeschriftungen setzen
            plt.xlabel(x_column, fontsize=20)
            plt.ylabel(y_column, fontsize=20)
            # plt.show()

            # Ergebnis-Text erstellen
            result_text = f"b0 (Konstante): {b0}\n"
            result_text += f"b1: {b1}\n"
            result_text += f"R2-Wert: {r_squared:.2f}"

            return html.Div([
                html.H5("Regressionsplot:"),  # Überschrift für den Regressionsplot
                dcc.Graph(
                    figure={
                        'data': [
                            {'x': x[x_column], 'y': y, 'mode': 'markers', 'name': 'Datenpunkte'},
                            # Datenpunkte als Scatterplot
                            {'x': x[x_column], 'y': y_pred, 'mode': 'lines', 'name': 'Regressionsgerade'}
                            # Regressionsgerade als Linienplot
                        ],
                        'layout': {
                            'title': 'Regression',  # Titel des Plots
                            'xaxis': {'title': x_column},  # Titel der x-Achse
                            'yaxis': {'title': y_column}  # Titel der y-Achse
                        }
                    }
                ),
                html.H5("Regressionskoeffizienten2:"),  # Überschrift für die Regressionskoeffizienten
                html.Pre(result_text)  # Anzeige der Regressionskoeffizienten als vorformatierter Text
            ])

        return html.Div()
    # Callback-Funktion für die Aktualisierung des Graphen (BIP_Schiene)
    @app.callback(
        Output('regression-results_BIP_rail', 'children'),
        Input('x-dropdown_BIP_rail', 'value'),
        Input('y-dropdown_BIP_rail', 'value')
    )
    def linear_regression(x_column, y_column):
        if x_column is not None and y_column is not None:
            x = merge_BIP_rail[
                x_column]  # Die unabhängige Variable x (x-Werte) aus dem merge_BIP_rail DataFrame extrahieren
            y = merge_BIP_rail[
                y_column]  # Die abhängige Variable y (y-Werte) aus dem merge_BIP_rail DataFrame extrahieren

            x = sm.add_constant(
                x)  # Eine konstante Spalte zu den x-Werten hinzufügen (für den y-Achsenabschnitt der Regression)

            model = sm.OLS(y,
                           x).fit()  # Eine lineare Regression durchführen: y als abhängige Variable und x als unabhängige Variable

            b0 = model.params[0]  # Der geschätzte Koeffizient für den y-Achsenabschnitt (Intercept)
            b1 = model.params[1]  # Der geschätzte Koeffizient für die Steigung (Slope)
            r_squared = model.rsquared  # Der Bestimmtheitskoeffizient (R-Quadrat) des Regressionsmodells

            y_pred = b0 + b1 * x[
                x_column]  # Die vorhergesagten y-Werte (basierend auf der Regression) für jeden x-Wert berechnen

            # Streudiagramm der Datenpunkte erstellen
            plt.scatter(x[x_column], y)

            # Regressionsgerade zeichnen
            plt.plot(x[x_column], y_pred, color='orange', linewidth=3)

            # Achsenbeschriftungen setzen
            plt.xlabel(x_column, fontsize=20)
            plt.ylabel(y_column, fontsize=20)
            # plt.show()

            # Ergebnis-Text erstellen
            result_text = f"b0 (Konstante): {b0}\n"
            result_text += f"b1: {b1}\n"
            result_text += f"R2-Wert: {r_squared:.2f}"

            return html.Div([
                html.H5("Regressionsplot:"),  # Überschrift für den Regressionsplot
                dcc.Graph(
                    figure={
                        'data': [
                            {'x': x[x_column], 'y': y, 'mode': 'markers', 'name': 'Datenpunkte'},
                            # Datenpunkte als Scatterplot
                            {'x': x[x_column], 'y': y_pred, 'mode': 'lines', 'name': 'Regressionsgerade'}
                            # Regressionsgerade als Linienplot
                        ],
                        'layout': {
                            'title': 'Regression',  # Titel des Plots
                            'xaxis': {'title': x_column},  # Titel der x-Achse
                            'yaxis': {'title': y_column}  # Titel der y-Achse
                        }
                    }
                ),
                html.H5("Regressionskoeffizienten2:"),  # Überschrift für die Regressionskoeffizienten
                html.Pre(result_text)  # Anzeige der Regressionskoeffizienten als vorformatierter Text
            ])

        return html.Div()
    # Callback-Funktion für die Aktualisierung des Graphen (BIP_Strasse_Schiene)
    @app.callback(
        Output('regression-results_BIP_road_rail', 'children'),
        Input('y-dropdown_BIP_road_rail', 'value'),
        Input('x-dropdown_BIP_road_rail', 'value')
    )
    def multi_regression(y_column, x_columns):
        if y_column is not None and len(x_columns) > 0:
            x = merge_BIP_road_rail[x_columns]
            x = sm.add_constant(x)
            y = merge_BIP_road_rail[y_column]
            model = sm.OLS(y, x).fit()
            ergibnis = model.summary()

            result = html.Div([
                html.H5("Regressionskoeffizienten:"),
                html.Pre(
                    # Verwenden Sie result_html als Text
                    children=ergibnis.as_text()
                )
            ])
            return result
        # Wenn keine Variablen ausgewählt sind, keine Ergebnisse anzeigen
        return html.Div()

    app.run_server(debug=True)


# ---------------------------------------------------------------------------------------------


def main():
    dashboard()


# ---------------------------------------------------------------------------------------------

if __name__ == '__main__':
    main()
