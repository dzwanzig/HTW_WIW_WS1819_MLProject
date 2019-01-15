from tp_ml_tools import lin_reg, log_reg_predict, knn_predict, poly_log_reg_predict, arimamodell, create_models
from tp_server import get_latest, rul_write
from tp_helper import wait
import warnings

warnings.filterwarnings("ignore")

create_models()

while True:
    # Überprüfung ob ein Ausfall in den nächsten 50 Messschritten zu erwarten ist
    df_latest = get_latest(1)
    prediction_log_reg = log_reg_predict(df_latest)
    # Durchführung wenn Ausfallprüfung positiv
    if prediction_log_reg == [True]:
          # ML Methoden durchführen
          prediction_knn = knn_predict(df_latest)
          df_lin_reg = get_latest(20)
          prediction_lin_reg = lin_reg(df_lin_reg)
          df_arima = get_latest(20)
          prediction_poly = poly_log_reg_predict(df_latest)
          # Arima für den erwarteten Fehler durchführen
          if prediction_poly == True:
                prediction_arima = arimamodell(df_arima,"Leistungsaufnahme", 25.0)
          else: 
                prediction_arima = arimamodell(df_arima, "Temperatur", 200.0)
          # RULs in Minuten berechnen
          rul = (int(prediction_knn[0]/2) + int(prediction_lin_reg/60)) / 2
          rul_knn = int(prediction_knn[0]/2)
          rul_lin = int(prediction_lin_reg/60)
          # RUL für Arima nur berechnen, wenn Berechnung möglich war
          if prediction_arima != 1000:
                rul_arima = int(prediction_arima)
          # Ausgaben für den Nutzer
          print("---------------------------------")
          print("Latest power consumption value: " +
                str(df_latest["Leistungsaufnahme"].values) + " // Latest temperatur value: " + str(df_latest["Temperatur"].values))
          print("---------------------------------")
          print("Log Reg Prediction: Failure in next 25 minutes ?" +
                str(prediction_log_reg))
          print("KNN Prediction : Failure in " +
                str(rul_knn) + " minutes")
          print("Lin Reg Prediction: Failure in " +
                str(rul_lin) + " minutes")
          if prediction_arima != 1000:
                print("Arima: Failure in " +
                      str(rul_arima) + " minutes")
          print("Polynominal Lin Reg Prediction: Next Failure is F001? " +
                str(prediction_poly))
          # Fehlercode ermitteln
          if prediction_poly == [0]:
                fail = "F002"
          else:
                fail = "F001"

          # Arima Wert nur schreiben, wenn die Berechung erfolgreich war
          # Berechnung des arithmetischen Mittels anhand der unterschiedlichen Methoden
          if prediction_arima != 1000:
                rul_mittel = (rul_lin + rul_knn + rul_arima)/3 
          else:
                rul_mittel = (rul_lin + rul_knn)/2
          # Ergebnisse der Berechnungen in die DB schreiben, wenn Ausfall in "Mittlerer Ausfall" in weniger als 1 Stunde
          if rul_mittel < 60:
                rul_write(df_lin_reg, rul_lin*60,
                          method="linear regression", failure=fail)
                rul_write(df_lin_reg, rul_knn*60, method="knn", failure=fail)
                rul_write(df_lin_reg, rul_mittel*60, method="mittel", failure=fail)        
          # Arima nur schreiben, wenn sie erfolgreich war
          if prediction_arima != 1000:
                rul_write(df_lin_reg, rul_arima*60, method="arima", failure=fail)
    else:
          print("Kein Ausfall in den nächsten 20 Minuten zu erwarten!")
          wait(5)
    
