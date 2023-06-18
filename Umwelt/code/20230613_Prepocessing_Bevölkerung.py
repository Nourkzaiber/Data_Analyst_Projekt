'''Bevölkerung am 1. Januar nach Alter und Geschlecht
Online Datencode
DEMO_PJAN__custom_6542521
Letzte Aktualisierung: 12/06/2023 23:00 '''

import pandas as pd

# Einladen der Datei von github in pandas dataframe
df_demo_raw = pd.read_csv(
    'https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/demo_pjan__custom_6542521_tabular.tsv', sep='\t')
# print(df_demo_raw)

# Ersetze Buchstaben und Leerzeichen in allen Spalten außer der ersten
df_demo = df_demo_raw
df_demo.iloc[:, 1:] = df_demo.iloc[:, 1:].astype(str).apply(
    lambda x: x.str.replace(r'[a-zA-Z\s]', '', regex=True))
# print(df_demo)

### Transponieren
# # # Setze die Spalte 'freq,unit,age,sex,geo\TIME_PERIOD' als Index
df_demo.set_index('freq,unit,age,sex,geo\\TIME_PERIOD', inplace=True)

# Transponiere den DataFrame
df_demo = df_demo.transpose()

# Zurücksetzen des Indexes und umbenennen
df_demo.reset_index(inplace=True)
df_demo = df_demo.rename(columns={'index': 'Jahr'})
# print(df_demo)
# print(df_demo.dtypes)

# Werte in float umwandeln und das Jahr als datetime
# Schleife über die Spalten ab der zweiten Spalte
for col in df_demo.columns[1:]:
    df_demo[col] = pd.to_numeric(df_demo[col], errors='coerce') #pd.to_numeric() mit errors='coerce': Werte, die nicht in Float umgewandelt werden, werden NaN
df_demo['Jahr'] = pd.to_datetime(df_demo['Jahr'])
# print(df_demo, df_demo.dtypes)

# # Teil-String aus den Spaltenüberschriften entfernen, damit nur das Länderkürzel bleibt
df_demo.columns = df_demo.columns.str.replace('A,NR,TOTAL,T,', '')
# print(df_demo)

# # Nur Länder nehmen, die auch in anderen Datensätzen vorhanden sind
selected_laender = ['AT', 'BE', 'BG', 'CH', 'CY', 'CZ', 'DE', 'DK', 'EE', 'EL', 'ES', 'EU27_2020', 'FI', 'FR', 'HR',
                    'HU', 'IE', 'IS', 'IT', 'LI', 'LT', 'LU', 'LV', 'MT', 'NL', 'NO', 'PL', 'PT', 'RO', 'SE', 'SI',
                    'SK', 'TR']

# Filtern nach den Ländern und das Jahr
spalten = ['Jahr'] + selected_laender
df_demo = df_demo.filter(items=spalten)
# print(df_demo)


# # Spaltenüberschriften austauschen
land = {
    'Jahr': 'Jahr',
    'AT': 'Österreich',
    'BE': 'Belgien',
    'BG': 'Bulgarien',
    'CH': 'Schweiz',
    'CY': 'Zypern',
    'CZ': 'Tschechien',
    'DE': 'Deutschland',
    'DK': 'Dänemark',
    'EE': 'Estland',
    'EL': 'Griechenland',
    'ES': 'Spanien',
    'EU27_2020': 'EU27_2020',
    'FI': 'Finnland',
    'FR': 'Frankreich',
    'HR': 'Kroatien',
    'HU': 'Ungarn',
    'IE': 'Irland',
    'IS': 'Island',
    'IT': 'Italien',
    'LI': 'Lichtenstein',
    'LT': 'Litauen',
    'LU': 'Luxemburg',
    'LV': 'Lettland',
    'MT': 'Malta',
    'NL': 'Niederlande',
    'NO': 'Norwegen',
    'PL': 'Polen',
    'PT': 'Portugal',
    'RO': 'Rumänien',
    'SE': 'Schweden',
    'SI': 'Slowenien',
    'SK': 'Slowakei',
    'TR': 'Türkei'}
# Spaltenüberschriften austauschen
df_demo = df_demo.rename(columns=land)

# Spaltenüberschriften alphabetisch sortieren
sorted_columns = sorted(df_demo.columns)
sorted_columns.remove('Jahr')
sorted_columns.insert(0, 'Jahr')
df_demo = df_demo.reindex(columns=sorted_columns)
# print(df_demo)

# letzten beiden Zeilen Entfernen, weil die Schadstoffdaten nur bis 2020 gehen
df_demo = df_demo.iloc[:-2]
# print(df_demo.dtypes)

# # # # in csv-Dateien schreiben
df_demo.to_csv('demo.csv', index=True)
