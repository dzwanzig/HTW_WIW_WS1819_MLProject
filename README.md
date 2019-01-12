# HTW_WIW_WS1819_MLProject
## Table of Contents  

[**Project-Description**](#Project-Description)  

[**Source-Codes-TP**](#Source-Codes-TP)

[*Simulationsdaten*](#Simulationsdaten_1)

[*ML-Tools*](#ML-Tools_4)

[*Ausführung-ML-Tools*](#Ausführung-ML-Tools_4)

[*Datenbank-Tabellen_anlegen*](#Datenbank-Tabellen_anlegen)

[*Datenbank_lesen_schreiben*](#Datenbank_lesen_schreiben)

[*Helper*](#Helper)

[**Source-Codes-TA**](#Source-Codes-TA)

[*OEE-Kennzahl*](#OEE-Kennzahl)

[*Datenbank-Abruf*](#Datenbank-Abruf)

[*Power-BI-Upload*](#Power-BI-Upload)

[**Installation**](#Installation)

[**Start-Anwendung**](#Start-Anwendung)

[**Lizensierung**](#Lizensierung)

[**Acknowledgments**](#Acknowledgments)

[**Kontaktinformationen**](#Kontaktinformationen)

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

 
![alt text](https://user-images.githubusercontent.com/44892210/51022749-5dcc1400-1585-11e9-9a18-1df52a0161fe.PNG)
*Abb. 1: Aufgabenaufteilung und Schnittstellen der Projektteams*

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
  ![alt_text](https://user-images.githubusercontent.com/44892210/51033547-0e491080-15a4-11e9-9419-0cc4e87f47f8.png)
- Systematische Fehler:
  - Fehler 1 (F001): zu hohe Temperatur
  ![alt_text](https://user-images.githubusercontent.com/44892210/51023624-a08eeb80-1587-11e9-9c32-22ef31f5e627.png)
  *Abb. 2: Simulationsfehler F001*
  
  - Fehler 2 (F002): zu hoher Strombedarf
  ![alt text](https://user-images.githubusercontent.com/44892210/51023426-324a2900-1587-11e9-9dc2-3ec48bbbd6dc.png)
  *Abb. 3: Simulationsfehler F002*
  
Weiterhin kann man die Simulationsdaten im "Testbetrieb" ausführen. Im Unterschied zum Normalbetrieb, werden beim Testbetrieb häufiger Fehler erzeugt wodurch die Daten zu Testzwecken schneller ausgewertet werden können.

### ML-Tools_4
[tp_ml_tools.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_ml_tools.py)

Die aus der Simulation gewonnenen Maschinendaten können mit verschiedenen Machine Learning Mehtoden analysiert werden. Nachfolgend wird kurz beschrieben, wozu die angewandten ML-Methoden verwendet wurden. Genauere Erläuterungen findet man im *WIKI* unter [*Was ist Machine Learning*](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/wiki/Was-ist-Maschine-learning%3F). Wie die ML-Methoden ausgeführt werden können, wird im nächsten Abschnitt [(Ausführung-ML-Tools_4)](#Ausführung-ML-Tools_4) beschrieben.
-	*Linear Regression*:
  zur Ermittlung der Dauer der Überschreitung des jeweiligen Grenzwertes von den Parametern "Temperatur" oder "Leistungsaufnahme".    
  Dabei wird der niedrigere Zeitwert angegeben. Weitere Informationen zur *Linear Regression* siehe https://scikit-learn.org/stable/auto_examples/linear_model/plot_ols.html.
  
- *ARIMA* (*A*uto*R*egressive *I*ntegrated *M*oving *A*verage *M*odel): 
  Ermittlung der Leistungsaufnahme und Überschreitung des Grenzwertes. Weitere Informationen zur *ARIMA* siehe https://www.statsmodels.org/dev/generated/statsmodels.tsa.arima_model.ARIMA.html.

- *KNN (K-Nearest Neighbors)*:
  zur Klassifizierung neuer Datensätze zu *Leistungsaufnahme* und *Temperatur* anhand der *nächsten Nachbarn*. Mit der Fragestellung, ob in den nächsten 50 Messschritten, beziehungsweise 25 Minuten ein Leistungsausfall der Maschine stattfinden wird, werden die Datensätze in *TRUE* oder *FALSE* klassifiziert.  Das Modell wird einmalig aufgesetzt und in dem Ordner [*saved_models*](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/saved_models) gespeichert. Neue Datensätze werden anhand der bereits vorhandenen, klassifizierten Datensätze, die am nächsten liegen, ebenfalls als *TRUE* oder *FALSE* klassifiziert. Weitere Informationen zu *KNN* siehe https://scikit-learn.org/stable/modules/neighbors.html.
- *Logistic Regression*: 
  zur Klassiefizierung neuer Datensätz mit gleichen Maschinenparametern und gleicher Fragestellung, wie zuvor unter *KNN* erläutert. Anhand von Datensätzen wird eine *Logistischen Funktion* erzeugt, welche bezogen auf die Fragestellung eine Ebene zwischen *TRUE* oder *FALSE* darstellt. Neue Datensätze können, je nachdem auf welcher Seite der Ebene sie liegen, entsprechend klassifiziert werden. 
   Weitere Informationen zu *Logistic Regression* siehe https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html.
- *Polynomial Logistic Regression*: wie *Logistic Regression* mit anderer Funktion mit anderer Ebene.
- *Train Test Split*:
  zur Bewertung der Modelle anhand von Trainings- und Testdaten und der Ermittlung des Modelscores.
  Weitere Informationen zu *Train Test Split* siehe https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html.
 
 In Verbindung mit den Codes der zuvor genannten ML-Tools sind die Ordner [*saved_models*](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/saved_models) und [*scalers*](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/scalers) zu betrachten.
 In [*saved_models*](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/saved_models) sind die erstellten Modelle der jeweiligen ML-Methoden gespeichert. Bei [*scalers*](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/scalers) sind die normal skalierten Datensätze gespeichert, die zur Verwendung der jweiligen ML-Methoden *KNN*, *Polynominal logistic Regression* und *logistic Regression*notwendig sind.
 
### Ausführung-ML-Tools_4
[tp_start.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_start.py)

Mit dem Ausführungscode kann die Anwendung der ML-Methoden gestartet werden. Dafür werden die Funktionen aus den einzelnen Source-Codes der zuvor beschriebenen *ML-Tools* importiert. Weiterhin werden die Tabellen der Datenbank ausgelesen und die ML-Modelle erstellt. Es wird geprüft, ob innerhalb der nächsten 50 Messschritte beziehungsweise 25 min ein systematischer Fehler (F001, F002) festgestellt wird. Der vorausgesagte Zeitpunkt des Ausfalls wird dann in die Predictions-Tabelle geschrieben.

Die einzelnen ML-Methoden können über die *Jupyter-Notebooks* im Ordner [notebooks](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/notebooks) nachvollzogen werden. Anaconda liefert die Anwendung *Jupyter* automatisch bei der installation mit. Einstieg in *Jupiter-Notebook* findet man im Tutorial unter folgendem Link: https://jupyter-notebook-beginner-guide.readthedocs.io/en/latest/ 

Der Programmablauf der start.py ist mittels der nachvollgenden Grafik vereinfacht dargestellt.
![alt-text](https://user-images.githubusercontent.com/44399149/51070891-02fbf080-1649-11e9-92b6-a229c1fce39c.jpg)
*Abb. X: vereinfachter Programmablauf*

### Datenbank-Tabellen_anlegen
[tp_tab_db.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/source_code-tp/tp_tab_db.py)

Die SQL-Datenbank *PraediktiveAnalysenTest*, die auf dem HTW FB4 Server erstellt wurde beinhaltet die beiden Tabellen *Maschinendaten_20181206* für die simulierten Maschinendaten und *predictions*. Der Code *tp_tab_db.py* dient dazu, die Tabellen neu aufzusetzen und jeweils die erste Zeile zu erstellen.

### Datenbank_lesen_schreiben 
[tp_server.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_server.py)

Wie im Abschnitt [Simulationsdaten_1](#Simulationsdaten_1) beschrieben, werden die simulierten Maschinendaten in die Datenbank *PraediktiveAnalysenTest* in der Tabelle *Maschinendaten_20181206* geschrieben. Mit dem Code *tp_server.py* werden die letzten 20 Datensätze gelesen und für die Anwendung der ML-Methoden sowie zur Visualisierung in der App verwendet. Weiterhin werden die durch ML-Methoden ermittelten prädiktiven Daten in die zweite Tabelle *predictions* geschrieben.

### Helper
[tp_helper.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_helper.py)

Mit dem Code *tp_helper.py* werden die Daten bereinigt, die nicht für die Prediction gebraucht werden und ungeplante Stillstandzeiten entfernt.

## Source-Codes-TA

### OEE-Kennzahl 
[ap_PythonEditorWrapper.PY](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/ap_PythonEditorWrapper.PY)

Die in der Datenbank (Tabelle I) bereitgestellten Simulationsdaten werden ausgewertet, um die OEE-Kennzahl (Overall Equipment Effectiveness Kennzahl) zu ermitteln. Dafür werden folgende Faktoren berechnet:
- Nutzungsgradfaktor,
- Qualitätsfaktor,
- Effizienzfaktor.
OEE = Nutzungsgradfaktor * Qualitätsfaktor * Effizienzfaktor * 100

### Datenbank-Abruf

### Power-BI-Upload




## Installation-TP
Nachfolgend sind die notwendigen Installationen der Programme mit Link zum Download aufgeführt:

|Programm|Funktion|Download|
|:------------:|:-------------------:|:---------------------:|
|Python 3.7|Programmiersprache|https://www.anaconda.com/download/#windows|
|Anaconda|am meisten verwendete Python Data Science Plattform|http://docs.anaconda.com/anaconda/install/windows/|
|Bibliotheken|siehe File [Bibliotheken.md](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/Bibliotheken.md)|siehe File [Bibliotheken.md](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/Bibliotheken.md)|


## Start-Anwendung
### Start-Anwendung-TP
- Github 
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
