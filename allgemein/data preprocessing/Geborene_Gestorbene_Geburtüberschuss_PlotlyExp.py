import pandas as pd
import plotly.express as px

raw_data_sterbene = pd.read_csv('12613-0002.csv', skiprows=5, nrows=73, encoding='ISO-8859-1', delimiter=';')
raw_data_geborene = pd.read_csv('Geboren_12612-0001.csv', skiprows=5, nrows=73, encoding='ISO-8859-1', delimiter=';')

data_geborene = raw_data_geborene.dropna()
data_sterbene = raw_data_sterbene.dropna()

data_geborene.rename(columns={'Unnamed: 0': 'Jahr'}, inplace=True)
data_sterbene.rename(columns={'Unnamed: 0': 'Jahr'}, inplace=True)

years = data_geborene['Jahr']
births = data_geborene['Insgesamt']
deaths = data_sterbene['Insgesamt']
excess = births - deaths

fig = px.line(title='Geborene, Gestorbene und Geburtenüberschuss über die Jahre')
fig.add_scatter(x=years, y=births, mode='lines', name='Geborene')
fig.add_scatter(x=years, y=deaths, mode='lines', name='Gestorbene')
fig.add_bar(x=years, y=excess, name='Geburtenüberschuss')

fig.update_layout(
    xaxis_title='Jahr',
    yaxis_title='Anzahl',
    legend_title='Kategorie',
    showlegend=True
)

fig.show()