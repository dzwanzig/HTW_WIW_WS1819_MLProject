# HTW_WIW_WS1819_MLProject
## Handling 
## Table of Contents  

[Project-Description](#Project-Description)  

[Source-Codes-TP](#Source-Codes-TP)

[Simulationsdaten](#Simulationsdaten_1)

[ML-Tools](#ML-Tools_4)

[Ausführung-ML-Tools](#Ausführung-ML-Tools_4)

[Arima](#Arima)

[Datenbanken](#Datenbanken)

[Helper](#Helper)

[Source-Codes-TA](#Source-Codes-TA)

[OEE-Kennzahl](#OEE-Kennzahl)

[Installation](#Installation)

[Start-Anwendung](#Start-Anwendung)

[Lizensierung](#Lizensierung)

[Acknowledgments](#Acknowledgments)

[Kontaktinformationen](#Kontaktinformationen)

<a name="headers"/>

## Project-Description
Im Rahmen eines WIW-Projekts an der HTW-Berlin (Wintersemester 18/19), wurden die Themen *Predictive Maintenance* und *Machine Learning* behandelt. Ziel war es, ein gesamtheitliches Verständnis zu den Themen zu gewinnen und Machine Learning Methoden anzuwenden sowie einen App-Prototypen zu entwickeln. Das Projektergebnis ist eine programmierte Anwendung, die es ermöglicht:

- Maschinendaten zu simulieren und in einer SQL Server Datenbank bereitzustellen,
- Maschinendaten aus der SQL Server Datenbank abzurufen und mit Machine Learning Mehthoden darzustellen,
- den nächsten Leistungsausfall der Maschine zeitlich vorauszusagen,
- OEE Daten (Overall Equipment Effectiveness) zu berechnen,
- OEE Daten und die Voraussage des nächsten Leistungsausfalls in einer App zu visualisieren.

Die Projektgruppe wurde in zwei Teams aufgeteilt: Team Prediction (tp) und Team App (ta).  Mithilfe der App, sollte ein Leistungsausfall einer Maschine vorhergesagt werden können. Aus Abbildung 1 geht hervor, welche Entwicklungen die Teams jeweils durchführten und wie die Maschinendaten von der Datengewinnung bis zur Visualisierung in der App verarbeitet werden. 

In Rahmen von weiteren Projekten der HTW Berlin können die zuvor beschriebenen Ergebnisse weiterentwickelt und für weitere Projekte verwendet genutzt. So könnten beispielsweise Daten von realen Maschinen implementiert und somit reale Analysen durchgeführt werden.

 
![alt text](https://github.com/Hawky12/HTW_WIW_WS1819_MLProject/blob/master/Aufteilung%20der%20Teams.PNG?raw=true)
Abb. 1: Aufgabenaufteilung und Schnittstellen der Projektteams

## Source-Codes-TP
([source_code LINK](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/source_code))

Im weiteren Verlauf dieses READMEs werden die im Repository unter *source_code* aufgeführten Codes erläutert. Die Abkürzungen *tp* und *ta* zu beginn der Codefiles weisen daruf hin, ob der Code vom *Team Predictive (tp)* oder *Team App (ta)* entwickelt wurde. Die nachfolgenden Titel zu den Codes sind analog zur Übersicht der *Aufgabenaufteilung und Schnittstellen der Projektteams* (Abb. 1) nummeriert, um herleiten zu können, welcher Code für welche Aufgabe verwendet wird.

### Simulationsdaten_1 
[tp_simulation.py LINK](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_simulation.py)

Da während der Projektzeit keine realen Maschinendaten vorhanden waren, hat das *Team Predictive* Maschinendaten simuliert, welche in der Datenbank *PraediktiveAnalysenTest* in der Tabelle *Maschinendaten_20181206* auf dem HTW FB4 Server hochgeladen werden. Mit dem Code werden folgende Maschinenparameter erstellt:
-	Drehzahl,
-	Leistungsaufnahme,
-	Vibration,
-	Lautstärke,
-	Temperatur,
-	Fehler ID,
-	Produktionsprogramm,
-	Ist-Menge.

Die Werte der Parameter ändern sich analog zu festgelegten Szenarien, welche durch einen definierten Zufallsgenerator gewählt werden. Folgende Szenarien stehen für den Zufallgenerator zur Auswahl:
- Normalbetrieb
- Zufallsfehler: 
  ungeplante Wartung, ungeplanter Werkzeugwechsel, ungeplante Wartung, ungeplante Reinigung, sonstiger ungeplanter Grund
- Systematische Fehler:
  - Fehler 1 (F001): zu hohe Temperatur
  - Fehler 2 (F002): zu hoher Strombedarf
 
Weiterhin kann man die Simulationsdaten im "Testbetrieb" ausführen. Im Unterschied zum Normalbetrieb, werden beim Testbetrieb häufiger Fehler erzeugt wodurch die Daten zu Testzwecken schneller ausgewertet werden können.

### ML-Tools_4
[tp_ml_tools.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_ml_tools.py)

Die aus der Simulation gewonnenen Maschinendaten können mit verschiedenen Machine Learning Mehtoden analysiert werden. Nachfolgend wird kurz beschrieben, wozu die angewandten ML-Methoden verwendet wurden. Wie die ML-Methoden ausgeführt werden können, wird im nächsten abschnitt [(Ausführung-ML-Tools_4)](#Ausführung-ML-Tools_4) beschrieben.
-	*Linear Regression*:
  zur Ermittlung der Dauer der Überschreitung des jeweiligen Grenzwertes von den Parametern "Temperatur" oder "Leistungsaufnahme".    
  Dabei wird der niedrigere Zeitwert angegeben.
- *KNN (K-Nearest Neighbors)*:
  zur Klassifizierung neuer Datensätze zu *Leistungsaufnahme* und *Temperatur* anhand der *nächsten Nachbarn*. Mit der Fragestellung, ob 
  in den nächsten 50 Messschritten, beziehungsweise 25 Minuten ein Leistungsausfall der Maschine stattfinden wird, werden die Datensätze 
  in *JA* oder *NEIN* klassifiziert.  Das Modell wird einmalig aufgesetzt und in dem Ordner [*saved_models*](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/saved_models) gespeichert. Neue Datensätze 
  werden anhand der bereits vorhandenen, klassifizierten Datensätze, die am nächsten liegen, ebenfalls als *JA* oder *NEIN* 
  klassifiziert. 
- *Logistic Regression*:
  zur Klassiefizierung neuer Datensätz mit gleichen Maschinenparametern und gleicher Fragestellung, wie zuvor unter *KNN* erläutert. Anhand von Datensätzen wird eine *Logistischen Funktion* erzeugt, welche bezogen auf die Fragestellung eine Ebene zwischen *JA* und *NEIN* darstellt. Neue Datensätze können, je nachdem auf welcher Seite der Ebene sie liegen, entsprechend klassifiziert werden.  
- *Polynomial Logistic Regression*:
- *Train Test Split*:
  zur Bewertung der Modelle anhand von Trainings- und Testdaten und der Ermittlung des Modelscores.
 
 In Verbindung mit den Codes der zuvor genannten ML-Tools sind die Ordner [*saved_models*](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/saved_models) und [*scalers*](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/scalers) zu betrachten.
 In [*saved_models*](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/saved_models) sind die erstellten Modelle der jeweiligen ML-Methoden gespeichert. Bei https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/scalers sind die normal skalierten Datensätze gespeichert, die zur Verwendung der jweiligen ML-Methoden *KNN*, *Polynominal logistic Regression* und *logistic Regression*notwendig sind.
 
### Ausführung-ML-Tools_4
[tp_start.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_start.py)

Mit dem Ausführungscode kann die Anwendung der ML-Methoden gestartet werden. Dafür werden die Funktionen aus den einzelnen Source-Codes der zuvor beschriebenen *ML-Tools* importiert. Weiterhin werden die Tabellen der Datenbank ausgelesen und die ML-Modelle erstellt. Es wird geprüft, ob innerhalb der nächsten 50 Messschritte beziehungsweise 25 min ein systematischer Fehler (F001, F002) festgestellt wird. Der vorausgesagte Zeitpunkt des Ausfalls wird dann in die Predictions-Tabelle geschrieben.

### ARIMA
(*A*uto*R*egressive *I*ntegrated *M*oving *A*verage *M*odel)
[tp_arima.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_arima.py)

Die *ARIMA*-Methode ist nicht, wie die anderen ML-Methoden im Code *tp_ml_tools.py* integriert.

### Datenbanken 
[tp_server.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_server.py)

Wie im Abschnitt [Simulationsdaten_1](#Simulationsdaten_1) beschrieben, werden die simulierten Maschinendaten in die Datenbank *PraediktiveAnalysenTest* in der Tabelle *Maschinendaten_20181206* geschrieben. Mit dem Code *tp_server.py* werden die letzten 20 Datensätze gelesen und für die Anwendung der ML-Methoden sowie zur Visualisierung in der App verwendet. Weiterhin werden die durch ML-Methoden ermittelten prädiktiven Daten in die zweite Tabelle *predictions* geschrieben.

### Helper
[tp_helper.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_helper.py)

Mit dem Code *tp_helper.py* werden die Daten bereinigt, die nicht für die Prediction gebraucht werden und ungeplante Stillstandzeiten entfernt.

## Source-Codes-TA

### OEE-Kennzahl ([ap_PythonEditorWrapper.PY](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/ap_PythonEditorWrapper.PY))

Die in der Datenbank (Tabelle I) bereitgestellten Simulationsdaten werden ausgewertet, um die OEE-Kennzahl (Overall Equipment Effectiveness Kennzahl) zu ermitteln. Dafür werden folgende Faktoren berechnet:
- Nutzungsgradfaktor,
- Qualitätsfaktor,
- Effizienzfaktor.
OEE = Nutzungsgradfaktor * Qualitätsfaktor * Effizienzfaktor * 100


## Installation
- Anaconda
- Bibliotheken (siehe File *Bibliotheken*)
- 
- 


## Start-Anwendung
### Start-Anwendung-TP
- Start Tabellen
- Start Simulationsdaten
- Start ML-Methoden

### Start-Anwendung-TA


## Lizensierung

## Acknowledgments
An dieser Stelle möchten wir uns bei Frau Prof. Dr.-Ing. Ute Dietrich (HTW Berlin) dafür danken, dass Sie unser Projekt betreut hat. Ihr konstruktive Feedback und stetige Unterstützung bei der Entwicklung von zum Beispiel Datenbanken, haben maßgeblich dazu beigetragen, dass die Projektergebnisse in dieser Form vorliegen.

Auch möchten wir uns bei unseren Komilitonen bedanken, die nicht in unserer Projektgruppe waren und dennoch Interesse an unseren Arbeiten gezigt hatten. Durch ihre Hinterfragungen und Ideen konnten wir unsere Arbeitsweise und Ergebnisse stetig optimieren.


## Kontaktinformationen
Frau Prof. Dr.-Ing. Ute Dietrich 
Ute.Dietrich@HTW-Berlin.de
