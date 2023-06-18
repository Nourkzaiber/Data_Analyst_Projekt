import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import plotly.express as px
import plotly.graph_objs as go

# Daten einlesen
raw_data = pd.read_csv('erwerbstaetigkeit-eltern.csv', encoding='ISO-8859-1', delimiter=';', skiprows=1,
                       names=['Jahr', 'Mütter', 'Väter'])

# Umwandlung der Spalten in numerische Werte
raw_data['Mütter'] = raw_data['Mütter'].str.replace(',', '.').astype(float)

# X und y Variablen für die Regression erstellen
X = sm.add_constant(raw_data['Jahr'])  # Konstante hinzufügen
y = raw_data['Mütter']

# Lineare Regression erstellen
model = sm.OLS(y, X)
results = model.fit()
# print(results.summary())
# ylre = -999.5238 +0.5137*X
# Vorhersage für zukünftige Werte
future_years = np.arange(2022, 2030)  # Annahme für die nächsten 8 Jahre
future_X = sm.add_constant(future_years)
predictions = results.predict(future_X)

df_pred = pd.DataFrame({'Jahre': future_years, 'Quote': predictions})
raw_data["fitted_mut"] = results.fittedvalues.values


# Daten und Regressionlinie plotten
plt.scatter(raw_data['Jahr'], raw_data['Mütter'], label='Mütter', color='red', marker='o')
plt.plot(raw_data['Jahr'], results.fittedvalues, label='Regression', linestyle='--', color='blue')
plt.plot(future_years, predictions, label='Vorhersage', linestyle=':', color='green')
plt.xlabel('Jahr')
plt.ylabel('Erwerbstätigenquote')
plt.title('Erwerbstätigenquote von Müttern')
plt.legend()

plt.ylim(0, 100)  # Begrenzung der y-Achse auf 0-100

plt.grid(True, linestyle='--', alpha=0.5)  # Raster hinzufügen
plt.tight_layout()  # Platz für Achsenbeschriftungen und Titel schaffen

plt.show()

# Vorhersagewerte ausgeben
future_predictions = pd.DataFrame({'Jahr': future_years, 'Vorhersage': predictions})
print(future_predictions)

# Berechnung des R²-Werts
predicted_values = results.predict()
r2 = r2_score(raw_data['Mütter'], predicted_values)
print("Bestimmtheitsmaß (R²):", r2)
