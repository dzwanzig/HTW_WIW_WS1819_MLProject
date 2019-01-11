from tp_ml_tools import lin_reg, log_reg_predict, knn_predict, poly_log_reg_predict, arimamodell
from tp_server import get_latest, rul_write
from tp_helper import wait
import warnings

warnings.filterwarnings("ignore")

while True:
    df_latest = get_latest(1)
    prediction_log_reg = log_reg_predict(df_latest)
    if prediction_log_reg == [True]:
            prediction_knn = knn_predict(df_latest)
            df_lin_reg = get_latest(20)
            prediction_lin_reg = lin_reg(df_lin_reg)
            df_arima = get_latest(20)
            prediction_poly = poly_log_reg_predict(df_latest)
            prediction_arima = arimamodell(df_arima)
            rul = (int(prediction_knn[0]/2) + int(prediction_lin_reg/60)) / 2
            rul_knn = int(prediction_knn[0]/2)
            rul_lin = int(prediction_lin_reg/60)
            if prediction_arima != "fail":
                  rul_arima = int(prediction_arima)
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
            if prediction_arima != "fail":
                  print("Arima: Failure in " +
                        str(rul_arima) + " minutes")
            print("Polynominal Lin Reg Prediction: Next Failure is F001? " +
                  str(prediction_poly))
            if prediction_poly == [0]:
                  fail = "F002"
            else:
                  fail = "F001"
            rul_write(df_lin_reg, rul_lin*60, method = "linear regression", failure=fail)
            rul_write(df_lin_reg, rul_knn*60, method = "knn", failure = fail)
            if prediction_arima != "fail":
                  rul_write(df_lin_reg, rul_arima*60, method = "arima", failure=fail)
    else:
          print("Kein Ausfall in den nächsten 25 Minuten zu erwarten!")
      
    wait(5)
