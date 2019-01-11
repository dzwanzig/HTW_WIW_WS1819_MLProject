from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
import pandas as pd
import pymssql
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import time as t
from datetime import datetime, timedelta
from tp_server import rul_write, get_df, get_latest
from sklearn.model_selection import train_test_split
from tp_helper import del_sort_add, filter_data, wait
from sklearn.linear_model import LogisticRegression
import joblib
import os
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error, mean_squared_log_error
import itertools
import warnings

warnings.filterwarnings("ignore")

# Linear regression

def lin_reg(df):
    """ function predicts RUL with the linear regression model, returns RUL in seconds """
    model_p = LinearRegression()
    model_p.fit(df[["Counter"]], df[["Leistungsaufnahme"]])
    coef_p = float(model_p.coef_[0])
    cur_p = float(df["Leistungsaufnahme"][0])
    rul_p = round((25.0 - cur_p) / coef_p * 0.5 * 60, 0)
    model_t = LinearRegression()
    model_t.fit(df[["Counter"]], df[["Temperatur"]])
    coef_t = float(model_t.coef_[0])
    cur_t = float(df["Temperatur"][0])
    try:
        rul_t = round((200.0 - cur_t) / coef_t * 0.5 * 60, 0)
    except:
        rul_t = -1.0
    if (rul_p > 0) and (rul_p < rul_t):
        rul = rul_p
    else:
        rul = rul_t
    return(rul)


# KNN

def knn_model(tts):
    """ function takes df and returns knn model"""
    # scale trainings data
    scaler = scale_data(tts[0])
    X_train = scaler.transform(tts[0])
    X_test = scaler.transform(tts[1])
    # save the scaler to disk
    joblib.dump(scaler, "scalers\\knn_scaler")
    # knN Model erstellen
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(X_train, tts[2])
    score = model.score(X_test, tts[3])
    # save the model to disk
    joblib.dump(model, "saved_models\\knn_model")
    print(score)
    return()


def knn_predict(df):
    """ function predicts RUL with the knn model, returns RUL in measuring steps """
    # load the model from disk
    model = joblib.load("saved_models\\knn_model")
    # load scaler from disk
    scaler = joblib.load("scalers\\knn_scaler")
    # Predictions des zuletzt gelieferten Wertes
    p = df[["Temperatur", "Leistungsaufnahme"]].values
    p = scaler.transform(p)
    p = model.predict(p)
    return(p)


# logistic regression

def log_reg_model(tts):
    """ function takes df and returns logistic regression model"""
    # scale trainings data
    scaler = scale_data(tts[0])
    X_train = scaler.transform(tts[0])
    X_test = scaler.transform(tts[1])
    # save the scaler to disk
    joblib.dump(scaler, "scalers\\log_reg_scaler")
    # Logistisches Regressionsmodel erstellen
    model = LogisticRegression()
    model.fit(X_train, tts[2])
    score = model.score(X_test, tts[3])
    # save the model to disk
    joblib.dump(model, "saved_models\\log_reg_model")
    print(score)
    return(model)


def log_reg_predict(df):
    """ function predicts RUL with the log regression model, returns RUL in measuring steps """
    # load model
    model = joblib.load("saved_models\\log_reg_model")
    # load scaler from disk
    scaler = joblib.load("scalers\\log_reg_scaler")
    # Predictions des/der zuletzt gelieferten Werte/s
    p = df.tail()
    p_data = p[["Temperatur", "Leistungsaufnahme"]].values
    p_scaled = scaler.transform(p_data)
    p_predicted = model.predict(p_scaled)
    return(p_predicted)


# polynominal logistic regression

def poly_log_reg_model(tts):
    """ function takes df and returns polynominal logistic regression model"""
    # scale trainings data
    scaler = scale_data(tts[0])
    X_train = scaler.transform(tts[0])
    X_test = scaler.transform(tts[1])
    # save the scaler to disk
    joblib.dump(scaler, "scalers\\poly_log_reg_scaler")
    # Logistisches Regressionsmodel erstellen
    model = LogisticRegression()
    model.fit(X_train, tts[2])
    score = model.score(X_test, tts[3])
    # save the model to disk
    joblib.dump(model, "saved_models\\poly_log_reg_model")
    print(score)
    return(model)


def poly_log_reg_predict(df):
    # load model
    model = joblib.load("saved_models\\poly_log_reg_model")
    # load scaler from disk
    scaler = joblib.load("scalers\\poly_log_reg_scaler")
    # Predictions des/der zuletzt gelieferten Werte/s
    p = df.tail(1)
    p = p[["Temperatur", "Leistungsaufnahme"]].values
    p = scaler.transform(p)
    p = model.predict(p)
    return(p)

# ARIMA Methode


def arimamodell(data, spalte, grenze):
    """Funktion erstellt ein Arima Model und gibt zurück, in wie vielen Minuten der angegebene Grenzwert überschritten wird.
    \n Parameter: 
    \n data - erwartet Dataframe mit den historischen Daten, 20 Zeilen lang 
    \n spalte - Name der Spalte, welche die Untersuchungsdaten enthält
    \n grenze - Grenzwert"""
    try:
        data = pd.DataFrame(data.loc[:, spalte])
        # Forecastwert in Intervallen, gf * 0.5=Minuten
        gf = 30

        # Erstellung einer Liste mit möglichen p-d-q-Parametern von 0 bis 4
        p = d = q = range(0, 4)
        pdq = list(itertools.product(p, d, q))
        # print(pdq)
        # Definition von Listen für die weitere Verarbeitung
        # aic für AIC-Parameter, paramlist für p-d-q-Parameter
        aic = list()
        paramlist = list()
        aiclist = list()
        # Definition der Parameterauswahl als Pandas DataFrame
        parameterauswahl = pd.DataFrame()
        # for-Schleife, die die p-d-q-Kombination aus der pdq-Liste testet
        # Für jede Kombination wird der AIC-Wert ermittelt und in die aiclist geschrieben
        for param in pdq:
            try:
                mod = ARIMA(data, order=param)
                results = mod.fit()
                #print('ARIMA{} - AIC:{}'.format(param, results.aic))
                paramlist.append(param)
                aiclist.append(abs(results.aic))
            except:
                continue
        # Zusammenfügen der Parameterlisten mit den jeweiligen AIC-Werten in ein Array
        parameterauswahl['paramlist'] = paramlist
        parameterauswahl['aiclist'] = aiclist
        # Identifikation und des niedrigsten (besten) AIC-Wertes
        # Anschließend werden die Parameter in neue Variablen übertragen
        aicminindex = parameterauswahl['aiclist'].idxmin()
        parammin = parameterauswahl.at[aicminindex, 'paramlist']
        pvaluemin = parammin[0]
        dvaluemin = parammin[1]
        qvaluemin = parammin[2]
        # Definition fiktiver Grenzwerte
        posGrenze = grenze
        negGrenze = 18
        p = pvaluemin
        d = dvaluemin
        q = qvaluemin

        # Berechnung der Arima-Prediction für existierende Werte
        # Übertragen der reinen Werte in Variable X (besseres Handling)
        X = data.values
        # Aufsplitten der Werte in Trainings- und Testdaten
        size = int(len(X) * 0.3)
        train, test = X[0:size], X[size:len(X)]

        history = [x for x in train]
        # Definition der Predictions-Werte als Liste
        predictions = list()
        # Arima-Model als for-Schleife für existierende Werte,
        # weil nur je ein Prediction-Schritt erstellt werden kann.
        # Die jeweilige Prediction wird in der Liste angefügt, die Schleife berechnet
        # dann von dem neuen Wert ausgehend.
        for t in range(len(test)):
            model = ARIMA(history, order=(int(p), int(d), int(q)))
            model_fit = model.fit(disp=False)
            output = model_fit.forecast()
            yhat = output[0]
            predictions.append(yhat)
            obs = test[t]
            history.append(obs)

        # error = mean_squared_error(test, predictions)
        aic = model_fit.aic

        # Arima-Model für vorausgesagte Werte
        # model1 = ARIMA(history, order=(int(p), int(d), int(q)))
        model1 = ARIMA(X, order=(int(p), int(d), int(q)))
        model_fit = model1.fit(disp=False)
        forecast = model_fit.forecast(steps=int(gf))
        forecastt = forecast[0]
        forecastpd = pd.DataFrame(forecastt)

        # Vorhersage Ausfallzeitpunkt
        # Erstellung Pandas-Array mit Werten über Grenzwert
        ausfallpos = forecastpd[forecastpd[0] >= posGrenze]
        ausfallinpos = (int(gf)-(len(ausfallpos)))*0.5
        # ausfallneg = forecastpd[forecastpd[0]<=negGrenze]

        # ausfallinneg = (int(gf)-(len(ausfallneg)))*0.5

        # Darstellung der Prediction-Linie
        # Wandlung der predictions in PandasArray
        predictionspd = pd.DataFrame(predictions)
        # Anfügen der forecast-Werte an predictions
        datapred = predictionspd.append(forecastpd, ignore_index=True)
        plt.figure()
        plt.plot(datapred, 'r--', color='red', linewidth=1.0)
        plt.plot(datapred, 'r--', color='red', linewidth=1.0)
        plt.axhline(y=posGrenze, color='darkblue', linewidth=1.0)
        plt.axhline(y=negGrenze, color='darkblue', linewidth=1.0)
        plt.xlabel('Zeit in Intervallen')
        plt.ylabel('Leistungsaufnahme')

        return (ausfallinpos)
    except:
        return (float(1000))

# train test split

def tts(df, aim="NaechsterAusfall"):
    """ Split data for training and testing for knn, argument "aim" takes a string with column name """
    X = df[["Temperatur", "Leistungsaufnahme"]].values
    y = df[aim].values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    tts = [X_train, X_test, y_train, y_test]
    return(tts)


# scale data

def scale_data(X_train):
    # create scaler
    scaler = StandardScaler()
    scaler.fit(X_train)
    return(scaler)


# create new models and scaler
df = get_df()
df = del_sort_add(df)
df = filter_data(df)

tts_plg = tts(df, aim="nFail_F001")
poly_log_reg_model(tts_plg)

tts_lg = tts(df, aim="nA50")
log_reg_model(tts_lg)

tts_knn = tts(df, aim="NaechsterAusfall")
knn_model(tts_knn)
