import pandas as pd
import plotly.express as px

# Daten einlesen
raw_data = pd.read_csv('wanderungen-deutschland-ausland-monate.csv', encoding='ISO-8859-1', delimiter=';')

# Spaltennamen anpassen
raw_data.columns = ['Monat', 'Zuzüge aus dem Ausland', 'Fortzüge ins Ausland', 'Wanderungssaldo']

# Daten konvertieren
raw_data['Zuzüge aus dem Ausland'] = raw_data['Zuzüge aus dem Ausland'].str.replace(',', '.').astype(float)
raw_data['Fortzüge ins Ausland'] = raw_data['Fortzüge ins Ausland'].str.replace(',', '.').astype(float)
raw_data['Wanderungssaldo'] = raw_data['Wanderungssaldo'].str.replace(',', '.').astype(float)

# Datum als Index verwenden
raw_data['Datum'] = pd.to_datetime(raw_data['Monat'])
raw_data.set_index('Datum', inplace=True)

# Plot erstellen
fig = px.bar(data_frame=raw_data, x=raw_data.index, y='Wanderungssaldo',
             labels={'x': 'Datum', 'Wanderungssaldo': 'Anzahl'},
             title='Wanderungen über die Grenzen Deutschlands')

# Linien für Zuzüge aus dem Ausland und Fortzüge ins Ausland hinzufügen
fig.add_scatter(x=raw_data.index, y=raw_data['Zuzüge aus dem Ausland'], mode='lines', name='Zuzüge aus dem Ausland')
fig.add_scatter(x=raw_data.index, y=raw_data['Fortzüge ins Ausland'], mode='lines', name='Fortzüge ins Ausland')

# Layout anpassen
fig.update_layout(
    xaxis=dict(tickangle=45),
    legend_title_text=None
)

# Plot anzeigen
fig.show()