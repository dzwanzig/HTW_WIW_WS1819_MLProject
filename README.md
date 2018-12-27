# HTW_WIW_WS1819_MLProject
## Table of Contents  

[Project Description](#Project description)  
 
[File list](#File list)

[Codes](#Codes)

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
Im Rahmen eines WIW-Projekts an der HTW-Berlin (Wintersemester 18/19), wurden das Thema Predictive Maintenance behnadelt. Ziel war es, ein gesamtheitliches Verständnis zu dem Thema zu gewinnen und Anwendungen von Machine Learning Methoden sowie einen App-Prototypen zu entwickeln.
Die Projektgruppe wurde in zwei Teams aufgeteilt: Team Prediction (tp) und Team App (ta). Um ein agiles Projektmanagement und regelmäßige Abstimmungen in und zwischen den Teams zu gewährleisten, wurde sich an dem Modell von Scrum orientiert.

Projektdurchführung:
Scrum


Im Rahmen eines WIW-Projekts zum Thema Predictive Maintenance an der HTW Berlin) wurde eine Gruppe von Studenten in zwei Teams unterteilt: Team Prediction und Team App. Ersteres war dafür zuständig, Maschinendaten zu simulieren und mittels ML-Methoden zu analysieren. Für die Visualisierung in einer App, wurden die Simulations- und Analysedaten dem App Team per Datenbanken zur Verfügung gestellt. 

 
![alt text](https://github.com/Hawky12/HTW_WIW_WS1819_MLProject/blob/master/Aufteilung%20der%20Teams.PNG?raw=true)
Abb. 1: Aufgabenaufteilung und Schnittstellen der Projektteams

Die entwickelten Codes des Teams Prediction können verwendet werden, um die Simulation und ML-Analysen im eigenen Programm live zu nehmen.

## File list

## Codes

### Simulation
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
