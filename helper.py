import time as t
import pandas as pd

def wait(n):
    """ wait for n seconds and print a statement abot waiting time """
    print("--------------------")
    print("Waiting for " + str(n) + " seconds...")
    t.sleep(n)

def del_sort_add(df):
    # umgekehrt sortieren
    df = df.sort_index(ascending=False)
    # unnötige Spalten entfernen
    df.pop('Timestamp')
    df.pop('Produktionsprogramm')
    df.pop('SollMenge')
    df.pop('IstMenge')
    df.pop('Ausschuss')
    df.pop('Machine_ID')
    df.pop('Maschine')
    df.pop('Datum')
    df.pop('Uhrzeit')
    df.pop('ID')
    # ... ungeplanten Stillständen (Zufallsfehler) entfernen
    df = df.query('FehlerID != "A000"')
    df = df.query('FehlerID != "A001"')
    df = df.query('FehlerID != "A002"')
    df = df.query('FehlerID != "A003"')
    df = df.query('FehlerID != "A004"')
    # FehlerID durchsuchen und Zähler anlegen, der angibt wie lang es bis zu nächsten Ausfall dauert
    x = []
    y = 0
    for row in df['FehlerID']:
        if row == "x000":
            y += 1
            x.append(y)
        else:
            y = 0
            x.append(y)
    # "Ausfallentfernung" an df_s anhängen
    df['NaechsterAusfall'] = x
    # Nächste FehlerID durchsuchen, neue Spalte mit Nächster FehlerID (nF001) erzeugen
    x = []
    y = "NaN"
    for row in df['FehlerID']:
        if row == "F001":
            y = "F001"
        elif row == "F002":
            y = "F002"
        else:
            y = y
        x.append(y)
    # Fehler ID entfernen
    df.pop('FehlerID')
    # "Nächster FehlerID" an df_s anhängen und in zwei Spalten aufsplitten
    df['nFail'] = x
    df = df.query('nFail != "NaN"')
    df = pd.get_dummies(df[['Drehzahl', 'Leistungsaufnahme', 'Vibration',
                            'Lautstaerke', 'Temperatur', 'NaechsterAusfall', 'nFail']])
    # Nächster Ausfall in 20/50 Schritten
    df['nA20'] = df['NaechsterAusfall'] < 20
    df['nA50'] = df['NaechsterAusfall'] < 50
    return(df)

def filter_data(df):
    df = df.query('Leistungsaufnahme > 18')
    df = df.query('NaechsterAusfall < 100')
    df = df.query('Temperatur > 99')
    return(df)
