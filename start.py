from ml_tools import lin_reg, log_reg_predict, knn_predict, poly_log_reg_predict
from server import get_latest, read_db_20, rul_write
from helper import wait

while True:
    df_latest = get_latest(1)
    df_lin_reg = read_db_20()
    prediction_lin_reg = lin_reg(df_lin_reg)
    prediction_log_reg = log_reg_predict(df_latest)
    prediction_knn = knn_predict(df_latest)
    prediction_poly = poly_log_reg_predict(df_latest)
    print("---------------------------------")
    print("Log Reg Prediction: " + str(prediction_log_reg))
    print("KNN Prediction : " + str(prediction_knn))
    print("Lin Reg Prediction :" + str(prediction_lin_reg))
    print("Next Failure is F001 :" + str(prediction_poly))
    print("Latest power consumption value: " +
          str(df_latest["Leistungsaufnahme"].values))
    print("Latest temperatur value: " + str(df_latest["Temperatur"].values))
    if prediction_log_reg == [True]:
        if prediction_poly == [0]:
            fail = "F002"
        else:
            fail = "F001"
        rul_write(df_lin_reg, prediction_lin_reg, failure=fail)
        print("Successfully added predicted Value to the prediction table :-)")
    wait(5)
