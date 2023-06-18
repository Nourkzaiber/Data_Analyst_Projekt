import pandas as pd
import plotly.express as px

# Daten einlesen
data = pd.read_csv('12612-0002.csv', skiprows=5, nrows=50, encoding='ISO-8859-1', delimiter=';')
data.rename(columns={'Unnamed: 0': 'Jahr', 'Unnamed: 1': 'Monat'}, inplace=True)

# Reihenfolge der Monate festlegen
month_order = ['Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']

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

fig.show()