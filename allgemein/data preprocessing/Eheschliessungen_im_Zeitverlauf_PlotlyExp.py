import pandas as pd
import plotly.express as px

# Daten einlesen
data = pd.read_csv('12611-0001.csv', skiprows=6, nrows=73, encoding='ISO-8859-1', delimiter=';')
data.columns = ['Jahr', 'Anzahl', 'Prozent']

# Plot erstellen
fig = px.line(data_frame=data, x='Jahr', y='Anzahl', title='Eheschließungen im Zeitverlauf',
              labels={'Jahr': 'Jahr', 'Anzahl': 'Anzahl'}, markers=True)

# Layout anpassen
fig.update_layout(yaxis_range=[0, 1000000])

# Achsenticks anpassen
fig.update_xaxes(tickangle=45)

# Plot anzeigen
fig.show()