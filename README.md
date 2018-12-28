# HTW_WIW_WS1819_MLProject
## Handling 
## Table of Contents  

[Project Description](#Project)  
 
[File list](#File)

[Erläuterungen zu den Codes](#Erläuterungen)

[Simulation](#Simulation)

[Analysen](#Analysen)

[Datenbanken](#Datenbanken)

[Installation](#Installation)

[Lizensierung](#Lizensierung)

[Tests](#Tests)

[Acknowledgments](#Acknowledgments)

[Kontaktinformationen](#Kontaktinformationen)

<a name="headers"/>

## Project description
Im Rahmen eines WIW-Projekts an der HTW-Berlin (Wintersemester 18/19), wurden die Themen *Predictive Maintenance* und *Machine Learning* behnadelt. Ziel war es, ein gesamtheitliches Verständnis zu den Themen zu gewinnen und Machine Learning Methoden anzuwenden sowie einen App-Prototypen zu entwickeln. Das Projektergebnis ist eine programmierte Anwendung, die es ermöglicht:

- Maschinendaten zu simulieren und in einer SQL Server Datenbank bereitzustellen,
- Maschinendaten aus der SQL Server Datenbank abzurufen und mit Machine Learning Mehthoden darzustellen,
- den nächsten Leistungsausfall der Maschine zeitlich vorauszusagen,
- OEE Daten (Overall Equipment Effectiveness) zu berechnen,
- OEE Daten und die Voraussage des nächsten Leistungsausfalls in einer App zu visualisieren.

Die Projektgruppe wurde in zwei Teams aufgeteilt: Team Prediction (tp) und Team App (ta).  Mithilfe der App, sollte ein Leistungsausfall einer Maschine vorhergesagt werden können. Aus Abbildung 1 geht hervor, welche Entwicklungen die Teams jeweils durchführten und wie die Maschinendaten von der Datengewinnung bis zur Visualisierung in der App verarbeitet werden. 

In Rahmen von weiteren Projekten der HTW Berlin können die zuvor beschriebenen Ergebnisse weiterentwickelt und für weitere Projekte verwendet genutzt. So könnten beispielsweise Daten von realen Maschinen implementiert und somit reale Analysen durchgeführt werden.

 
![alt text](https://github.com/Hawky12/HTW_WIW_WS1819_MLProject/blob/master/Aufteilung%20der%20Teams.PNG?raw=true)
Abb. 1: Aufgabenaufteilung und Schnittstellen der Projektteams


## File list

## Erläuterungen zu den Codes

### Simulationsdaten ([tp_helper.py](https://github.com/dorianzwanzig/HTW_WIW_WS1819_MLProject/blob/master/source_code/tp_helper.py))
Um Analysen nach ML-Methoden durchführen zu können, müssen vorab Maschinendaten simuliert werden. Hierfür können mit dem Code zur Simulation kontinuierlich (alle 30 Sekunden) per Zufallsgenerator Daten zu folgenden Maschinenparametern erstellt werden:
-	Drehzahl,
-	Leistungsaufnahme,
-	Vibration,
-	Lautstärke,
-	Temperatur,
-	Fehler ID,
-	Produktionsprogramm,
-	Ist-Menge.

### Analysen
Die aus der Simulation gewonnenen Maschinendaten können mit verschiedenen Codes analysiert werden. Dabei werden folgende ML-Methoden verwendet:
-	Lineare Regression,
-	ARIMA.

## Datenbanken

Sowohl die Simulationsdaten, als auch die Analysedaten werden kontinuierlich in SQL-Datenbanken übertragen, welche auf einem Server der HTW Berlin zur Verfügung gestellt wurden. Somit stehen die Daten für das App Team bereit zur Visualisierung. 

## Installation

## Lizensierung

## Tests

## Acknowledgments

## Kontaktinformationen
