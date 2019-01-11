from tp_ml_tools import lin_reg, log_reg_predict, knn_predict, poly_log_reg_predict
from tp_server import get_latest, rul_write
from tp_helper import wait

while True:
    df_latest = get_latest(1)
    df_lin_reg = get_latest(20)
    prediction_lin_reg = lin_reg(df_lin_reg)
    prediction_log_reg = log_reg_predict(df_latest)
    prediction_knn = knn_predict(df_latest)
    prediction_poly = poly_log_reg_predict(df_latest)
    rul = (int(prediction_knn[0]/2) + int(prediction_lin_reg/60)) / 2
    print("---------------------------------")
    print("Latest power consumption value: " +
          str(df_latest["Leistungsaufnahme"].values) + " // Latest temperatur value: " + str(df_latest["Temperatur"].values))
    print("---------------------------------")
    print("Log Reg Prediction: Failure in next 25 minutes ?" +
          str(prediction_log_reg))
    if prediction_log_reg == [True]:
        print("KNN Prediction : Failure in " +
              str(prediction_knn[0]/2) + " minutes")
        print("Lin Reg Prediction: Failure in " +
              str(prediction_lin_reg/60) + " minutes")
        print("Polynominal Lin Reg Prediction: Next Failure is F001? " +
              str(prediction_poly))
        if prediction_poly == [0]:
            fail = "F002"
        else:
            fail = "F001"
        rul_write(df_lin_reg, rul, failure=fail)
    wait(5)