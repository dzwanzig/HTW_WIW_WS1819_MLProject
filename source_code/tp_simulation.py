import numpy as np
import sys
import random
from datetime import datetime, timedelta
import pymssql
import time as t

absolviert = 0

# Verbindung mit Datenbank herstellen
conn = pymssql.connect("pcs.f4.htw-berlin.de", "Masterprojekt",
                       "Masterprojekt", "PraediktiveAnalysenTest")
cursor = conn.cursor()

# letzten Datensatz abrufen
cursor.execute('SELECT TOP 1 * FROM Maschinendaten_20181206 ORDER BY ID DESC')
list_1 = cursor.fetchall()

# ID extrahieren
last_id = list_1[0]
last_id = last_id[0]
last_id = int(last_id.replace("ABC_01_", "")) - 1000000

# Uhrzeit extrahieren
last_time = list_1[0]
last_time = last_time[2]

# Startwerte (STartData):
drehzahl = 100           # Startdrehzahl
leistungsaufnahme = 18.5  # Startleistungsaufnahme
vibration = 0            # Startvibration
lautstaerke = 75         # Startlautstärke
# Startwert für die Datensatz ID, wird um "ABC_01_" am Anfang ergänzt
data_id_nr = 1000000 + last_id
temperatur = 100         # Starttemperatur
fehler_id = "leer"       # Fehlerwert bei Ausfall
time = last_time         # Startzeit der Simulation
datum = "leer"           # Simuliertes Datum
uhrzeit = "leer"         # Simulierte Uhrzeit
machine_id = "ABC_01"    # Identifikation der Maschine
prod_programm = "PP001"  # Produktionsprogramm
soll_menge = 2350        # Soll-Menge des Produktionsprogramm
ist_menge = 2350         # Tatsächlich produzierte Menge
ausschuss = 0            # Fehlerhafte Teile
neue_spalte = ()         # Neue Zeile für Serverübergabe

conn.close()

# Liste für Übergabe an DB vorbereiten und Übergabefunktion aufrufen


def write_data():
    global drehzahl, leistungsaufnahme, vibration, lautstaerke, data_id_nr, temperatur, fehler_id, ist_menge, ausschuss, neue_spalte, datum, uhrzeit, soll_menge, prod_programm, machine_id, time
    data_id_nr = data_id_nr + 1
    timer()
    neue_spalte = tuple(("ABC_01_" + str(data_id_nr), machine_id, time, datum, uhrzeit, drehzahl, leistungsaufnahme, vibration, lautstaerke, temperatur, fehler_id,
                         prod_programm, soll_menge, ist_menge, ausschuss, "5"))
    print("--------------------")
    print("neue_spalte" + str(neue_spalte))
    write_db()

# Liste an Datenbank übergeben


def write_db():
    global neue_spalte
    conn = pymssql.connect("pcs.f4.htw-berlin.de", "Masterprojekt",
                           "Masterprojekt", "PraediktiveAnalysenTest")
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO Maschinendaten_20181206 VALUES (%d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        [neue_spalte])
    conn.commit()
    print("--------------------")
    print("neue_spalte übermittelt")
    conn.close()
    wait()

# Zeitzähler


def timer():
    global time, datum, uhrzeit
    time = time + timedelta(seconds=30)
    now = str(time).split()
    datum = str(now[0])
    uhrzeit = str(now[1])

# Wartezeit


def wait():
    global wait_for
    # print("--------------------")
    # print("Waiting for " +  str(wait_for) + " seconds...")
    t.sleep(wait_for)

# Erstellung mehrerer Datensätze durch Schleife (Normalbetrieb)


def normalbetrieb():
    global drehzahl, leistungsaufnahme, vibration, lautstaerke, data_id_nr, temperatur, time, fehler_id, ist_menge, ausschuss
    x = 0
    y = random.randrange(50, 100)
    while x < y:
        drehzahl = 100
        leistungsaufnahme = round(np.random.normal(18.5, 0.1), 3)
        vibration = round(np.random.normal(0, 0.1), 3)
        lautstaerke = round(np.random.normal(75, 0.1), 3)
        temperatur = 100
        fehler_id = "x000"
        ist_menge = 2350
        ausschuss = random.randrange(0, 20)
        print("--------------------")
        print("Normalbetrieb")
        write_data()
        x = x + 1

# Erstellung mehrerer Datensätze durch Schleife (Wartung)


def zufallsfehler():
    global drehzahl, leistungsaufnahme, vibration, lautstaerke, data_id_nr, temperatur, time, fehler_id, ist_menge, ausschuss
    fehler_id = zufallsfehler_grund()
    x = 0
    y = random.randrange(10, 100)
    while x < y:
        drehzahl = 0
        leistungsaufnahme = round(np.random.normal(2, 0.1), 3)
        vibration = round(np.random.normal(0, 0.3), 3)
        lautstaerke = round(np.random.normal(25, 0.1), 3)
        temperatur = 100
        ist_menge = 0
        ausschuss = 0
        print("--------------------")
        print("Zufallsfehler/Wartung")
        write_data()
        x = x + 1

# Zufallsfehlergrund auswählen


def zufallsfehler_grund():
    random_choice = random.randrange(1, 100)
    if random_choice < 40:
        return "A001"   # Kein Material/ kein Auftrag/ kein Personal (A001)
    elif random_choice < 70:
        return "A002"   # ungeplanter Werkzeugwechsel/ Rüsten (A002)
    elif random_choice < 80:
        return "A003"   # ungeplante Wartung (A003)
    elif random_choice < 95:
        return "A004"   # ungeplante Reinigung (A004)
    else:
        return "A000"   # Sonstiger ungeplanter Grund (A000)

# Erstellung mehrerer Datensätze durch Schleife (Ausfall aufgrund zu hoher Motortemperatur)


def systematischerfehler_2():
    global drehzahl, leistungsaufnahme, vibration, lautstaerke, data_id_nr, temperatur, time, fehler_id, ist_menge, ausschuss
    fehler_id = "x000"

    # Motortemperatur steigt bis zum Ausfall
    while (temperatur < 200) and (leistungsaufnahme < 25):
        drehzahl = 100 + random.randrange(-4, 0)
        leistungsaufnahme = round(
            leistungsaufnahme + np.random.normal(0.05, 0.05), 3)
        vibration = round(np.random.normal(0, 0.1), 3)
        lautstaerke = round(np.random.normal(75, 0.1), 3)
        temperatur = round(temperatur + np.random.normal(1.5, 0.3), 1)
        ist_menge = int(drehzahl * 47 / 2)
        ausschuss = int(round(random.randrange(5, 30), 0))
        print("--------------------")
        print("Überhitzungsszenario")
        write_data()
    fehler_id = "F002"
    # Abkühlung bis Normaltemperatur bevor Maschine wieder angeschaltet wird
    while temperatur > 100:
        drehzahl = 0
        leistungsaufnahme = round(np.random.normal(4.5, 0.1), 3)
        vibration = round(np.random.normal(0, 0.05), 3)
        lautstaerke = round(np.random.normal(25, 0.1), 3)
        temperatur = round(temperatur - 1, 0)
        ist_menge = 0
        ausschuss = 0
        print("--------------------")
        print("Motorkühlung auf 100 °C")
        write_data()
    normalbetrieb()

# Erstellung mehrerer Datensätze durch Schleife (Ausfall aufgrund zu hoher Leistungsaufnahme)


def systematischerfehler_1():
    global drehzahl, leistungsaufnahme, vibration, lautstaerke, data_id_nr, temperatur, time, fehler_id, ist_menge, ausschuss
    fehler_id = "x000"
    # Strombedarf steigt bis zum Ausfall
    while (temperatur < 200) and (leistungsaufnahme < 25):
        drehzahl = 100 + random.randrange(-3, 1)
        leistungsaufnahme = round(
            leistungsaufnahme + np.random.normal(0.1, 0.1), 3)
        vibration = round(np.random.normal(0, 0.1), 3)
        lautstaerke = round(np.random.normal(75, 0.1), 3)
        temperatur = round(temperatur + np.random.normal(0.5, 0.2), 1)
        ist_menge = int(drehzahl * 47 / 2)
        ausschuss = int(round(random.randrange(5, 40), 0))
        print("--------------------")
        print("Stromverbrauchsszenario")
        write_data()
    fehler_id = "F001"
    # zufällige Ausfallzeit
    x = 0
    y = random.randrange(10, 100)
    while (y < x) and (temperatur != 100):
        drehzahl = 0
        leistungsaufnahme = round(np.random.normal(1.5, 0.1), 3)
        vibration = round(np.random.normal(0, 0.1), 3)
        lautstaerke = round(np.random.normal(25, 0.1), 3)
        if temperatur != 100:
            if temperatur < 100:
                temperatur = round(temperatur + 1, 0)
            else:
                temperatur = round(temperatur - 1, 0)
        ist_menge = 0
        ausschuss = 0
        print("--------------------")
        print("Motorkühlung auf 100 °C und " + str(y-x) + " Schritte warten")
        write_data()
        x = x + 1
        normalbetrieb()

# Für Test nur Normalbetrieb und Ausfall 1 eingeschaltet


def choose_test():
    global absolviert
    random_choice = random.randrange(1, 100)
    if random_choice < 50:
        systematischerfehler_2()
    else:
        systematischerfehler_1()
    absolviert += 1

# Auswahl zwischen den Events


def choose_normal():
    global absolviert
    random_choice = random.randrange(1, 100)
    if random_choice < 90:
        normalbetrieb()
    elif random_choice < 95:
        systematischerfehler_1()
    elif random_choice < 98:
        systematischerfehler_2()
    else:
        zufallsfehler()
    absolviert += 1


# Aufruf Auswahl
choice = input(
    "Für Testbetrieb bitte 'TEST' eingeben, andere Eingaben führen zum Normalbetrieb des Simulators: ")

# Wartezeit auswählen
wait_for = int(input("Wartezeit in Sekunden: "))

szenariendurchlaeufe = int(
    input("Anzahl der gewünschten Szenariendurchläufe angeben: "))

while szenariendurchlaeufe > absolviert:
    if choice == "TEST":
        choose_test()
    else:
        choose_normal()
