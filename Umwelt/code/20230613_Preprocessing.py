'''Netto-Treibhausgasemissionen, nach Quellensektor (Quelle: EUA) Online Datencode SDG_13_10 Der Indikator misst die
gesamten nationalen Emissionen (von den ESD und ETS Sektoren) inklusive die des Internationalen Flugverkehrs des so
genannten „Kyoto Korbs“ von Treibhausgasen, einschließlich Kohlendioxid (CO2), Methan (CH4), Distickstoffoxid (N2O),
und die so genannten F-Gase (Fluorkohlenwasserstoffe, perfluorierte Kohlenwasserstoffe, Stickstofftriflouride (NF3)
und Schwefelhexafluorid (SF6)) von allen Sektoren des Treibhausgasinventars (einschliesslich Internationale Luftfahrt
und indirektes CO2). Der Indikator wird auf zwei Arten dargestellt: als Netto-Emissionen inklusive der Landnutzung,
Landnutzungsänderungen und Forstwirtschaft (LULUCF) bzw. exklusive dieser. Diese werden zu einem einzelnen Indikator
zusammengefasst, der in CO2-Äquivalenten ausgedrückt wird. Die Treibhausgasinventare werden jährlich von den
EU-Mitgliedstaaten im Rahmen der Berichterstattung gemäß dem Rahmenabkommen der Vereinten Nationen über den
Klimawandel (UNFCCC) übermittelt.'''

import pandas as pd

# Einladen der Datei von github in pandas dataframe
df_treibhausgase_raw = pd.read_csv('https://raw.githubusercontent.com/peterjthul/DataAnalyst_Project/main/sdg_13_10.tsv', sep='\t')
# print(df_treibhausgase_raw)

# Ersetze Buchstaben und Leerzeichen in allen Spalten außer der ersten
df_treibhausgase_raw.iloc[:, 1:] = df_treibhausgase_raw.iloc[:, 1:].astype(str).apply(lambda x: x.str.replace(r'[a-zA-Z\s]', '', regex=True))
# print(df_treibhausgase_raw)

# Beschränken der Daten auf ohne LULUCF (TOX4_MEMONIA)
df_treibhausgase = df_treibhausgase_raw[df_treibhausgase_raw["airpol,src_crf,unit,geo\\time"].str.contains(".*TOTX4_MEMONIA.*")]
# print(df_treibhausgase)

# Kürzen des Strings in Spalte 1 auf Index 90 bzw. T_HAB und Länderkürzel
df_treibhausgase.iloc[:, 0] = df_treibhausgase.iloc[:, 0].str.replace(r'GHG,TOTX4_MEMONIA,', '')
# print(df_treibhausgase)

#Auftrennung in Index 90 und absoluten Werten
df_treibhausgase_I90 = df_treibhausgase[df_treibhausgase["airpol,src_crf,unit,geo\\time"].str.contains(".*I90.*")]
df_treibhausgase_abs = df_treibhausgase[df_treibhausgase["airpol,src_crf,unit,geo\\time"].str.contains(".*T_HAB.*")]
# print(df_treibhausgase_I90)
# print(df_treibhausgase_abs)


### Abschnitt für die absoluten Werte
# Setze die Spalte 'airpol,src_crf,unit,geo\time' als Index
df_treibhausgase_abs.set_index('airpol,src_crf,unit,geo\\time', inplace=True)

# Transponiere den DataFrame
df_treibhausgase_abs = df_treibhausgase_abs.transpose()

# Zurücksetzen des Indexes und umbenennen
df_treibhausgase_abs.reset_index(inplace=True)
df_treibhausgase_abs = df_treibhausgase_abs.rename(columns={'index': 'Jahr'})
# print(df_treibhausgase_abs)

# Werte in float umwandeln und das Jahr als datetime
# Schleife über die Spalten ab der zweiten Spalte
for col in df_treibhausgase_abs.columns[1:]:
    # Entfernen von Leerzeichen und nicht-numerischen Zeichen in der Spalte
    df_treibhausgase_abs[col] = df_treibhausgase_abs[col].str.replace(r'[^\d.]', '', regex=True).astype(float)
df_treibhausgase_abs['Jahr'] = pd.to_datetime(df_treibhausgase_abs['Jahr'])
# print(df_treibhausgase_abs, df_treibhausgase_abs.dtypes)

# Aus den Spaltenüberschriften entfernen, damit nur das Länderkürzel bleibt
df_treibhausgase_abs.columns = df_treibhausgase_abs.columns.str.replace('T_HAB,', '')
# print(df_treibhausgase_abs)

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
df_treibhausgase_abs = df_treibhausgase_abs.rename(columns=land)

# Spaltenüberschriften alphabetisch sortieren
sorted_columns = sorted(df_treibhausgase_abs.columns)
sorted_columns.remove('Jahr')
sorted_columns.insert(0, 'Jahr')
df_treibhausgase_abs = df_treibhausgase_abs.reindex(columns=sorted_columns)
# print(df_treibhausgase_abs)

# letzte  Zeile entfernen, weil die Schadstoffdaten nur bis 2020 gehen
df_treibhausgase_abs = df_treibhausgase_abs.iloc[:-1]
# print(df_treibhausgase_abs.dtypes)

### Abschnitt für den Index 90-Werte
# Setze die Spalte 'airpol,src_crf,unit,geo\time' als Index
df_treibhausgase_I90.set_index('airpol,src_crf,unit,geo\\time', inplace=True)

# Transponiere den DataFrame
df_treibhausgase_I90 = df_treibhausgase_I90.transpose()

# Zurücksetzen des Indexes und umbenennen
df_treibhausgase_I90.reset_index(inplace=True)
df_treibhausgase_I90 = df_treibhausgase_I90.rename(columns={'index': 'Jahr'})
# print(df_treibhausgase_I90)

# Werte in float umwandeln und das Jahr als datetime
# Schleife über die Spalten ab der zweiten Spalte
for col in df_treibhausgase_I90.columns[1:]:
    # Entfernen von Leerzeichen und nicht-numerischen Zeichen in der Spalte
    df_treibhausgase_I90[col] = df_treibhausgase_I90[col].str.replace(r'[^\d.]', '', regex=True).astype(float)
    df_treibhausgase_I90['Jahr'] = pd.to_datetime(df_treibhausgase_I90['Jahr'])
# print(df_treibhausgase_I90, df_treibhausgase_I90.dtypes)

# Aus den Spaltenüberschriften entfernen, damit nur das Länderkürzel bleibt
df_treibhausgase_I90.columns = df_treibhausgase_I90.columns.str.replace('I90,', '')
# print(df_treibhausgase_I90)

# Spaltenüberschriften austauschen
df_treibhausgase_I90 = df_treibhausgase_I90.rename(columns=land)

# Spaltenüberschriften alphabetisch sortieren
sorted_columns = sorted(df_treibhausgase_I90.columns)
sorted_columns.remove('Jahr')
sorted_columns.insert(0, 'Jahr')
df_treibhausgase_I90 = df_treibhausgase_I90.reindex(columns=sorted_columns)
# print(df_treibhausgase_I90)


# df_treibhausgase_gesamt = df_treibhausgase_abs.set_index('Jahr').join(df_treibhausgase_I90.set_index('Jahr'))
# print(df_treibhausgase_gesamt)
# print(df_treibhausgase_gesamt.dtypes)

# in csv-Dateien schreiben
df_treibhausgase_abs.to_csv('treibhausgase_abs.csv', index=True)
# df_treibhausgase_gesamt.to_csv('treibhausgase_gesamt.csv', index=True)
df_treibhausgase_I90.to_csv('treibhausgase_I90.csv', index=True)
