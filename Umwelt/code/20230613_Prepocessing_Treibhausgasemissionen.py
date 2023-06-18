'''Greenhouse gas emissions by source sector (source: EEA)
Online data code: ENV_AIR_GGE
last update: 28/04/2023 23:00
This dataset includes data on greenhouse gas emissions inventory, as reported to the European Environment Agency (EEA).
Note that Eurostat is not the producer of these data, only re-publishes them. The European Union (EU) as a party to the
United Nations Framework Convention on Climate Change (UNFCCC) reports annually its greenhouse gas inventory for the
year t-2 and within the area covered by its Member States. The inventory contains data on carbon dioxide (CO2),
methane (CH4), nitrous oxide (N2O), perfluorocarbons (PFCs), hydrofluorocarbons (HFCs), sulphur hexafluoride (SF6) and
nitrogen trifluoride (NF3). The EU inventory is fully consistent with national greenhouse gas inventories compiled by
the EU Member States.'''

import pandas as pd

# Einladen der Datei von github in pandas dataframe
df_emission_raw = pd.read_csv(
    'https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/env_air_emis_ind.tsv', sep='\t')
# print(df_umweltschutz_raw)

# Ersetze Buchstaben und Leerzeichen in allen Spalten außer der ersten
df_emission = df_emission_raw
df_emission.iloc[:, 1:] = df_emission.iloc[:, 1:].astype(str).apply(
    lambda x: x.str.replace(r'[a-zA-Z\s]', '', regex=True))
# print(df_emission)

# Beschränken auf totalen Ausstoß
df_emission_total = df_emission[df_emission["unit,airpol,src_nfr,geo\\time"].str.contains(".*TOT.*")]
# print(df_emission_total)

# ### Transponieren
# # Setze die Spalte 'unit,geo\\time' als Index
df_emission_total.set_index('unit,airpol,src_nfr,geo\\time', inplace=True)

# Transponiere den DataFrame
df_emission_total = df_emission_total.transpose()

# Zurücksetzen des Indexes und umbenennen
df_emission_total.reset_index(inplace=True)
df_emission_total = df_emission_total.rename(columns={'index': 'Jahr'})
# print(df_emission_total)
# print(df_emission_total.dtypes)

# Werte in float umwandeln und das Jahr als datetime
# Schleife über die Spalten ab der zweiten Spalte
for col in df_emission_total.columns[1:]:
    df_emission_total[col] = pd.to_numeric(df_emission_total[col], errors='coerce') #pd.to_numeric() mit errors='coerce': Werte, die nicht in Float umgewandelt werden, werden NaN
df_emission_total['Jahr'] = pd.to_datetime(df_emission_total['Jahr'])
# print(df_emission_total, df_emission_total.dtypes)

### Auftrennung der einzelnen Emissionen
# Liste der Spalten mit dem Teilsting "NH3" erstellen
nh3_columns = [col for col in df_emission_total.columns if 'NH3' in col]
# DataFrame df_NH3 erstellen, der die ausgewählten Spalten enthält
df_NH3 = df_emission_total[['Jahr'] + nh3_columns]
# print(df_NH3)
# Aus den Spaltenüberschriften entfernen, damit nur das Länderkürzel bleibt
df_NH3.columns = df_NH3.columns.str.replace('T,NH3,NFR_TOT_NAT,', '')
# print(df_NH3)

# übrigen Schadstoffemissionen
NMVOC_columns = [col for col in df_emission_total.columns if 'NMVOC' in col]
df_NMVOC = df_emission_total[['Jahr'] + NMVOC_columns]
df_NMVOC.columns = df_NMVOC.columns.str.replace('T,NMVOC,NFR_TOT_NAT,', '')
NOX_columns = [col for col in df_emission_total.columns if 'NOX' in col]
df_NOX = df_emission_total[['Jahr'] + NOX_columns]
df_NOX.columns = df_NOX.columns.str.replace('T,NOX,NFR_TOT_NAT,', '')
PM10_columns = [col for col in df_emission_total.columns if 'PM10' in col]
df_PM10 = df_emission_total[['Jahr'] + PM10_columns]
df_PM10.columns = df_PM10.columns.str.replace('T,PM10,NFR_TOT_NAT,', '')

# Länderkürzel AT,BE,BG,CH,CY,CZ,DE,DK,EE,EL,ES,EU27_2020,FI,FR,HR,HU,IE,IS,IT,LI,LT,LU,LV,MT,NL,NO,PL,PT,RO,SE,SI,SK,TR
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
df_NH3 = df_NH3.rename(columns=land)
df_NMVOC = df_NMVOC.rename(columns=land)
df_NOX = df_NOX.rename(columns=land)
df_PM10 = df_PM10.rename(columns=land)

# Spaltenüberschriften alphabetisch sortieren
sorted_columns = sorted(df_NH3.columns)
sorted_columns.remove('Jahr')
sorted_columns.insert(0, 'Jahr')
df_NH3 = df_NH3.reindex(columns=sorted_columns)
# print(df_NH3)
sorted_columns = sorted(df_NMVOC.columns)
sorted_columns.remove('Jahr')
sorted_columns.insert(0, 'Jahr')
df_NMVOC = df_NMVOC.reindex(columns=sorted_columns)

sorted_columns = sorted(df_NOX.columns)
sorted_columns.remove('Jahr')
sorted_columns.insert(0, 'Jahr')
df_NOX = df_NOX.reindex(columns=sorted_columns)

sorted_columns = sorted(df_PM10.columns)
sorted_columns.remove('Jahr')
sorted_columns.insert(0, 'Jahr')
df_PM10 = df_PM10.reindex(columns=sorted_columns)


# # # in csv-Dateien schreiben
df_NH3.to_csv('NH3.csv', index=True)
df_NMVOC.to_csv('NMVOC.csv', index=True)
df_NOX.to_csv('NOX.csv', index=True)
df_PM10.to_csv('PM10.csv', index=True)
