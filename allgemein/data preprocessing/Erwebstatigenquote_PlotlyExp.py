import pandas as pd
import plotly.express as px

# Daten einlesen
raw_data = pd.read_csv('erwerbstaetigkeit-eltern.csv', encoding='ISO-8859-1', delimiter=';', skiprows=1, names=['Jahr', 'Mütter', 'Väter'])

# Umwandlung der Spalten in numerische Werte
raw_data['Mütter'] = raw_data['Mütter'].str.replace(',', '.').astype(float)
raw_data['Väter'] = raw_data['Väter'].str.replace(',', '.').astype(float)

fig = px.line(raw_data, x='Jahr', y=['Mütter', 'Väter'], title='Erwerbstätigenquote von Müttern und Vätern')
fig.update_layout(
    xaxis_title='Jahr',
    yaxis_title='Erwerbstätigenquote',
    legend_title='Geschlecht'
)
fig.show()