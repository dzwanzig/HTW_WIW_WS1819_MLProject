# -*- coding: utf-8 -*-
"""
Created on Fri Dec 14 16:24:26 2018

@author: Peter Lenge
"""


import matplotlib.pyplot as plt  # Bibliothek zur Datenvisualisierung    
import pandas as pd  # Aufrufen der Pandas Bibliothek (Daten Analyse Tools)
import numpy as np  # Aufrufen numerisches Python (Matrizen, lineare Algebra)
import pymssql  # Import der Kommunikation mit SQL-Server
import os  # Zum Löschen der Bilddatei
import time  # Import der Zeitfunktionen für While-Schleife
import itertools  # Import der Iterationsfunktion für p-d-q-Parameter-Kombinationen
import warnings  # Modul zur Fehlerbehandlung
warnings.filterwarnings("ignore") # Abstellen von Warnungen

from statsmodels.tsa.arima_model import ARIMA  # Bibliothek zur Berechnung der Arima
from sklearn.metrics import mean_squared_error, mean_squared_log_error # Modul zur MSE-Berechnung 



# Forecastwert in Intervallen, gf * 0.5=Minuten
gf= 30
    
    
def arimamodell():
    
    # Befehl zum Löschen der existierenden Bilddatei, da ansonsten die 
    # Bilddateien gemerged/zusammengefügt werden
    if os.path.exists('C:/Users/bassmaniac/Desktop/HTW Berlin/2. Semester/06_Projekt/Spyder Scripts/Arima/arima1.png'):
        os.remove('C:/Users/bassmaniac/Desktop/HTW Berlin/2. Semester/06_Projekt/Spyder Scripts/Arima/arima1.png')
        print('Bild gelöscht')
    
    print('Start Arima Berechnung')
    print('Eingelesene Daten: %s' %data.size)
    # Erstellung einer Liste mit möglichen p-d-q-Parametern von 0 bis 4
    p = d = q = range(0, 4)
    pdq = list(itertools.product(p, d, q))
    # print(pdq)
    # Definition von Listen für die weitere Verarbeitung
    # aic für AIC-Parameter, paramlist für p-d-q-Parameter
    aic = list()
    paramlist=list()
    aiclist=list()
    # Definition der Parameterauswahl als Pandas DataFrame
    parameterauswahl=pd.DataFrame()
    # for-Schleife, die die p-d-q-Kombination aus der pdq-Liste testet
    # Für jede Kombination wird der AIC-Wert ermittelt und in die aiclist geschrieben
    for param in pdq:
        try:
            mod = ARIMA(data, order=param)
            results = mod.fit()
            print('ARIMA{} - AIC:{}'.format(param, results.aic))
            paramlist.append(param)
            aiclist.append(abs(results.aic))
        except:
            continue
    # Zusammenfügen der Parameterlisten mit den jeweiligen AIC-Werten in ein Array
    parameterauswahl['paramlist']=paramlist
    parameterauswahl['aiclist']=aiclist
    print('Parameterauswahl :' %parameterauswahl)
    # Identifikation und des niedrigsten (besten) AIC-Wertes
    # Anschließend werden die Parameter in neue Variablen übertragen
    aicminindex=parameterauswahl['aiclist'].idxmin()
    parammin= parameterauswahl.at[aicminindex, 'paramlist']
    pvaluemin=parammin[0]
    dvaluemin=parammin[1]
    qvaluemin=parammin[2]
    print('Best-Match Parameter')
    print('pmin =%s'%pvaluemin) 
    print('dmin= %s'%dvaluemin)
    print('qmin= %s'%qvaluemin)
    
    # Definition fiktiver Grenzwerte    
    posGrenze = 28
    negGrenze = 18
    p=pvaluemin
    d=dvaluemin
    q=qvaluemin
    
    # Berechnung der Arima-Prediction für existierende Werte  
    # Übertragen der reinen Werte in Variable X (besseres Handling)
    X = data.values
    # Aufsplitten der Werte in Trainings- und Testdaten
    size = int(len(X) * 0.3)
    train, test = X[0:size], X[size:len(X)]
    print(len(train))
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
        print('predicted=%f, expected=%f' % (yhat, obs))
    error = mean_squared_error(test, predictions)
    aic=model_fit.aic
    print('Test MSE: %.3f' % error)
    print(model_fit.summary())
    print('Lag: %s' % model_fit.k_ar)
    print('Coefficients: %s' % model_fit.params)
    print(len(predictions))
    

    # Arima-Model für vorausgesagte Werte 
    # model1 = ARIMA(history, order=(int(p), int(d), int(q)))                  
    model1 = ARIMA(X, order=(int(p), int(d), int(q)))
    model_fit = model1.fit(disp=False)
    forecast = model_fit.forecast(steps=int(gf))
    forecastt = forecast[0]
    forecastpd=pd.DataFrame(forecastt)
    print(forecastpd)
    # print(model_fit.summary())
    print('First five predictions: ')
    print(forecastpd.iloc[:5])
    print('Last five predictions:')
    print(forecastpd.iloc[-5:])
        
    # Vorhersage Ausfallzeitpunkt
    # Erstellung Pandas-Array mit Werten über Grenzwert
    ausfallpos = forecastpd[forecastpd[0]>=posGrenze]
    print('Werte über positivem Grenzwert')
    print(ausfallpos)
    print('Länge Ausfallarray:%s' %(len(ausfallpos)))
    ausfallinpos = (int(gf)-(len(ausfallpos)))*0.5
    if (int(gf)-len(ausfallpos)) == int(gf):
        print('Keine Grenzwertüberschreitung')
    else:
        print('Grenzwertüberschreitung in Minuten:')
        # Wertübergabe auf Server?
        print(ausfallinpos)
    ausfallneg = forecastpd[forecastpd[0]<=negGrenze]
    print('Werte unter negativem Grenzwert')
    print(ausfallneg)
    print('Länge Ausfallarray:%s' %(len(ausfallneg)))
    ausfallinneg = (int(gf)-(len(ausfallneg)))*0.5
    if (int(gf)-len(ausfallneg)) == int(gf):
        print('Keine Grenzwertunterschreitung')
    else:
        print('Grenzwertunterschreitung in Minuten:')
        # Wertübergabe auf Server?
        print(ausfallinneg)
     
    
        
   
    # Darstellung der Prediction-Linie
    # Wandlung der predictions in PandasArray
    predictionspd=pd.DataFrame(predictions)
    # Anfügen der forecast-Werte an predictions
    datapred=predictionspd.append(forecastpd, ignore_index=True)
    
    #fig = plt.figure()
    plt.plot(datapred, 'r--', color='red', linewidth=1.0)
    plt.axhline(y=posGrenze, color='darkblue', linewidth=1.0)
    plt.axhline(y=negGrenze, color='darkblue', linewidth=1.0)
    plt.xlabel('Zeit in Intervallen')
    plt.ylabel('Leistungsaufnahme')
    
# Bild als png speichern und auf Server ablegen    
    
    # plt.text((len(test)-20), 30, r'Ausfall in ' + str(ausfallin) + ' min.')
    plt.plot(data, color='blue', linewidth=1.0)
    plt.text((len(test)-int(gf)), (posGrenze-1), r'Test MQA: %.3f' % error)
    plt.text((len(test)-int(gf)), (posGrenze-2), r'Test AIC: %.3f' % aic)
    plt.title('Ausfallzeitpunkt')
    plt.grid(True)
    
    # Erstellung der Bilddatei
    plt.savefig('C:/Users/bassmaniac/Desktop/HTW Berlin/2. Semester/06_Projekt/Spyder Scripts/Arima/arima1.png')
    print('Bild erstellt')
    # plt.show()
    # plt.pause(0.0001)

    

i=0
seconds = 1
while True:
    print('Start in %s ' %(seconds) + ' Sekunden')
    time.sleep(seconds)
    print('Daten werden aktualisiert')
    password = "Masterprojekt"
    conn = pymssql.connect("pcs.f4.htw-berlin.de", "Masterprojekt", password, "PraediktiveAnalysenTest")
    df = pd.read_sql('SELECT TOP 30 * FROM Maschinendaten_20181206 ORDER BY ID DESC', conn)
    # adding the counter
    counter = [30, 29, 28, 27, 26, 25 ,24 , 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8,
           7, 6, 5, 4, 3, 2, 1]
    df["Counter"] = counter
    data = pd.DataFrame(df.loc[:,'Leistungsaufnahme'])
    print(df.head())
    print('Eingelesene Daten: %s' %data.size)
    arimamodell()
    i = i + 1
    print('Iteration %s' %i)
    if(i > 0):
        break
    
    

