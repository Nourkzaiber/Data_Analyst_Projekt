'''Gesamtwirtschaftliche investitionen für den Umweltschutz
Online Datencode: TEN00136
In dieser Tabelle werden die Investitionen gezeigt, die von der Volkswirtschaft (Staat und Kapitalgesellschaften) zur
Erbringung von Umweltschutzdienstleistungen (z. B. Abfall- und Abwasserwirtschaft, Dekontaminierung verseuchter Böden)
getätigt werden. Die Angaben beinhalten Investitionen der Kapitalgesellschaften für den Umgang mit eigenen
Umweltbelastungen.
'''

import pandas as pd

# Einladen der Datei von github in pandas dataframe
df_umweltschutz_raw = pd.read_csv(
    'https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/ten00136.tsv', sep='\t')
# print(df_umweltschutz_raw)

# Ersetze Buchstaben und Leerzeichen in allen Spalten außer der ersten
df_umweltschutz = df_umweltschutz_raw
df_umweltschutz.iloc[:, 1:] = df_umweltschutz.iloc[:, 1:].astype(str).apply(
    lambda x: x.str.replace(r'[a-zA-Z\s]', '', regex=True))
# print(df_umweltschutz)

# Beschränken der Daten auf absolute Zahlen)
df_umweltschutz_abs = df_umweltschutz[df_umweltschutz["unit,geo\\time"].str.contains(".*MIO_EUR.*")]
# print(df_umweltschutz_abs)

### Transponieren
# Setze die Spalte 'unit,geo\\time' als Index
df_umweltschutz_abs.set_index('unit,geo\\time', inplace=True)

# Transponiere den DataFrame
df_umweltschutz_abs = df_umweltschutz_abs.transpose()

# Zurücksetzen des Indexes und umbenennen
df_umweltschutz_abs.reset_index(inplace=True)
df_umweltschutz_abs = df_umweltschutz_abs.rename(columns={'index': 'Jahr'})
# print(df_umweltschutz_abs)
# print(df_umweltschutz_abs.dtypes)

# Werte in float umwandeln und das Jahr als datetime
# Schleife über die Spalten ab der zweiten Spalte
for col in df_umweltschutz_abs.columns[1:]:
    df_umweltschutz_abs[col] = pd.to_numeric(df_umweltschutz_abs[col], errors='coerce') #pd.to_numeric() mit errors='coerce': Werte, die nicht in Float umgewandelt werden, werden NaN
df_umweltschutz_abs['Jahr'] = pd.to_datetime(df_umweltschutz_abs['Jahr'])
# print(df_umweltschutz_abs, df_umweltschutz_abs.dtypes)
#
# Die Jahre 2020 und 2021 haben nur wenige Daten, daher werden sie entfernt
df_umweltschutz_abs = df_umweltschutz_abs.drop([10, 11])
# print(df_umweltschutz_abs)

# Aus den Spaltenüberschriften das "MIO_EUR," entfernen, damit nur das Länderkürzel bleibt
df_umweltschutz_abs.columns = df_umweltschutz_abs.columns.str.replace('MIO_EUR,', '')
# print(df_umweltschutz_abs)


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
df_umweltschutz_abs = df_umweltschutz_abs.rename(columns=land)

# Spaltenüberschriften alphabetisch sortieren
sorted_columns = sorted(df_umweltschutz_abs.columns)
sorted_columns.remove('Jahr')
sorted_columns.insert(0, 'Jahr')
df_umweltschutz_abs = df_umweltschutz_abs.reindex(columns=sorted_columns)
print(df_umweltschutz_abs)


# in csv-Dateien schreiben
df_umweltschutz_abs.to_csv('umweltschutz_abs.csv', index=True)
