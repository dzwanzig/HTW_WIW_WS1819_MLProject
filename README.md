# HTW_WIW_WS1819_MLProject
## Handling 
## Table of Contents  

[Project-Description](#Project-Description)  

[Source-Codes](#Source-Codes)

[Simulationsdaten](#(1) Simulationsdaten)

[ML-Tools](#ML-Tools)

[Datenbanken](#Datenbanken)

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

## Source-Codes
([source_code LINK](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/tree/master/source_code))

Im weiteren Verlauf dieses READMEs werden die im Repository unter *source_code* aufgeführten Codes erläutert. Die Abkürzungen *tp* und *ta* zu beginn der Codefiles weisen daruf hin, ob der Code vom *Team Predictive (tp)* oder *Team App (ta)* entwickelt wurde. Die nachfolgenden Titel zu den Codes sind analog zur Übersicht der *Aufgabenaufteilung und Schnittstellen der Projektteams* (Abb. 1) nummeriert, um herleiten zu können, welcher Code für welche Aufgabe verwendet wird.

### (1) Simulationsdaten 
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

### ML-Tools
[tp_ml_tools.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_ml_tools.py)
Die aus der Simulation gewonnenen Maschinendaten können mit verschiedenen Machine Learning Mehtoden analysiert werden. Folgende ML-Methoden werden hierbei verwendet:
-	Lineare Regression:
  zur Ermittlung der Dauer der Überschreitung des jeweiligen Grenzwertes von den Parametern "Temperatur" oder "Leistungsaufnahme".    
  Dabei wird der niedrigere Zeitwert angegeben.
- KNN (K-Nearest Neighbors):
  
- logistic regression,
-	ARIMA,
- KNN.

### Datenbanken ([tp_server.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_server.py))

Sowohl die Simulationsdaten, als auch die Analysedaten werden kontinuierlich in SQL-Datenbanken übertragen, welche auf einem Server der HTW Berlin zur Verfügung gestellt wurden. Somit stehen die Daten für das App Team bereit zur Visualisierung. 

### OEE-Kennzahl ([ap_PythonEditorWrapper.PY](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/ap_PythonEditorWrapper.PY))

Die in der Datenbank (Tabelle I) bereitgestellten Simulationsdaten werden ausgewertet, um die OEE-Kennzahl (Overall Equipment Effectiveness Kennzahl) zu ermitteln. Dafür werden folgende Faktoren berechnet:
- Nutzungsgradfaktor,
- Qualitätsfaktor,
- Effizienzfaktor.
OEE = Nutzungsgradfaktor * Qualitätsfaktor * Effizienzfaktor * 100


## Installation

## Start-Anwendung

## Lizensierung

## Acknowledgments
An dieser Stelle möchten wir uns bei Frau Prof. Dr.-Ing. Ute Dietrich (HTW Berlin) dafür danken, dass Sie unser Projekt betreut hat. Ihr konstruktive Feedback und stetige Unterstützung bei der Entwicklung von zum Beispiel Datenbanken, haben maßgeblich dazu beigetragen, dass die Projektergebnisse in dieser Form vorliegen.

Auch möchten wir uns bei unseren Komilitonen bedanken, die nicht in unserer Projektgruppe waren und dennoch Interesse an unseren Arbeiten gezigt hatten. Durch ihre Hinterfragungen und Ideen konnten wir unsere Arbeitsweise und Ergebnisse stetig optimieren.


## Kontaktinformationen
Frau Prof. Dr.-Ing. Ute Dietrich 
Ute.Dietrich@HTW-Berlin.de
