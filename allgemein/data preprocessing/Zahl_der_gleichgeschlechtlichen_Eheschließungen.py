import pandas as pd
import matplotlib.pyplot as plt

# Daten einlesen
data = pd.read_csv('gleichgeschlechtliche-eheschließungen.csv', delimiter=';', encoding='ISO-8859-1')

# Spaltennamen anpassen
data.columns = ['Jahr', 'zwischen Männern', 'zwischen Frauen']
#print(data)

# Gesamtzahl berechnen
data['Gesamt'] = data['zwischen Männern'] + data['zwischen Frauen']

print(data.head())


# Plot erstellen
plt.plot(data['Jahr'], data['zwischen Männern'], label='Zwischen Männern', color='blue')
plt.plot(data['Jahr'], data['zwischen Frauen'], label='Zwischen Frauen', color='red')
plt.bar(data['Jahr'], data['Gesamt'], label='Gesamt',color='pink')
plt.xlabel('Jahr')
plt.ylabel('Anzahl')
plt.title('Zahl der gleichgeschlechtlichen Eheschließungen')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
# y-Achse begrenzen
plt.ylim(0, 30000)

plt.tight_layout()
plt.show()