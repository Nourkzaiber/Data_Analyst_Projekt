import pandas as pd
import plotly.express as px

raw_data = pd.read_csv('12411-0005.csv', skiprows=6, nrows=87, encoding='ISO-8859-1', sep=';')
data = raw_data.copy()
data.columns = ['Altersjahre', '31.12.2017', '31.12.2018', '31.12.2019', '31.12.2020', '31.12.2021']
data = data[data['Altersjahre'] != 'Insgesamt']

fig = px.line(data_frame=data, x='Altersjahre', y=['31.12.2017', '31.12.2018', '31.12.2019', '31.12.2020', '31.12.2021'],
              title='Altersverteilung der deutschen Bevölkerung')
fig.update_layout(
    xaxis_title='Altersjahre',
    yaxis_title='Bevölkerung',
    legend_title='Jahr',
    xaxis={'tickangle': 90, 'range': [-0.5, len(data)-0.5]}
)
fig.show()