# Bibliotheken

|**Name der Bibliothek**|**In welchem Code verwendet**|**Funktion**|**Falls noch nicht installiert, über *Anaconda > Environment* Bibliothek raussuchen und installieren in Anaconda, importieren aus**|
|:----------------------:|:----------------------:|:----------------------:|
|matplotlib|tp_arima.py;tp_ml_tools.py|Datenvisualisierung|
|pandas|tp_arima.py; tp_helper.py; tp_ml_tools.py; tp_server.py|Datenanalyse Tools|
|numpy|tp_arima.py; tp_simulation.py|Matrizen, lineare Algebra|
|pymssql|tp_arima.py; tp_ml_tools.py; tp_server.py; tp_simulation.py|Kommunikation mit SQL-Server|
|os|tp_arima.py;tp_ml_tools.py|Löschen von Bilddateien|
|itertools|tp_arima.py|Iterationsfunktion für p-d-q-Parameter-Kombinationen|
|time|tp_arima.py; tp_helper.py; tp_ml_tools.py; tp_simulation.py|Zeitfunktion|
|warnings|tp_arima.py|Fehlerbehandlung|
|warnings.filterwarnings|tp_arima.py|Abstellen von Warnungen|
|statsmodels.tsa.arima_model|tp_arima.py|Berechnung der ARIMA|
|sklearn.metrics|tp_arima.py|MSE-Berechnung|
|sklearn.neighbors|tp_ml_tools.py|Klassifizierung nach KNN|
|sklearn.preprocessing|tp_ml_tools.py|Normalskalierung der Daten zur Verwendung für ML_Klassifizierungsmodelle|
|sklearn.linear|tp_ml_tools.py|Anwendung der Linearen Regression|
|datetime|tp_ml_tools.py|Datum, Zeit, Zeitdifferenz|
|sklearn.model_selection|tp_ml_tools.py|Anwendung Train Test Split|
|sklearn.linear_model|tp_ml_tools.py|Anwendung Logistic Regression|
|joblib|tp_ml_tools.py|Parallelisierung, Memorization sowie Speichern und Laden von Objekten|
|sys|tp_simulation.py|Konstanten, Funktionen|
|random|tp_simulation.py|Zufallsgenerator|
