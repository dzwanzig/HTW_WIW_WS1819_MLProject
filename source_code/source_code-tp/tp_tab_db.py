# Starten der Tabellen der Datenbank "PraediktiveAnalysenTest"
# Tabelle 1: Maschinendaten_20181206

CREATE TABLE [dbo].[Maschinendaten_20181206] (
    [ID]                  NVARCHAR (255) NULL,
    [Maschine]            NVARCHAR (255) NULL,
    [Timestamp]           DATETIME       NULL,
    [Datum]               DATE           NULL,
    [Uhrzeit]             TIME (7)       NULL,
    [Drehzahl]            FLOAT (53)     NULL,
    [Leistungsaufnahme]   FLOAT (53)     NULL,
    [Vibration]           FLOAT (53)     NULL,
    [Lautstaerke]         FLOAT (53)     NULL,
    [Temperatur]          FLOAT (53)     NULL,
    [FehlerID]            NVARCHAR (255) NULL,
    [Produktionsprogramm] NVARCHAR (255) NULL,
    [SollMenge]           FLOAT (53)     NULL,
    [IstMenge]            FLOAT (53)     NULL,
    [Ausschuss]           FLOAT (53)     NULL,
    [Machine_ID]          INT            DEFAULT ('5') NULL
);

#Schreiben der 1. Zeile
INSERT INTO [dbo].[Maschinendaten_20181206] ([ID], [Maschine], [Timestamp], [Datum], [Uhrzeit], [Drehzahl], [Leistungsaufnahme], [Vibration], [Lautstaerke], [Temperatur], [FehlerID], [Produktionsprogramm], [SollMenge], [IstMenge], [Ausschuss], [Machine_ID]) VALUES (N'ABC_01_1000047', N'ABC_01', N'2018-01-06 12:24:30', N'2018-01-06', N'12:24:30', 100, 18.469, -0.135, 74.952, 100, N'x000', N'PP001', 2350, 2350, 0, 5)

# Tabelle 2: Predictions
CREATE TABLE [dbo].[Predictions] (
    [Id]               INT           NULL,
    [Timestamp]        DATETIME      NULL,
    [Methode]          NVARCHAR (50) NULL,
    [Maschine]         NVARCHAR (50) NULL,
    [Ausfallzeitpunkt] DATETIME      NULL,
    [Ausfallgrund]     NVARCHAR (50) NULL,
    [Machine_ID]       INT           DEFAULT (NULL) NULL
);

#Schreiben der 1. Zeile
INSERT INTO [dbo].[Predictions] ([Id], [Timestamp], [Methode], [Maschine], [Ausfallzeitpunkt], [Ausfallgrund], [Machine_ID]) VALUES (26113, N'2018-03-04 21:21:00', N'lin_reg', N'XL_400_1', N'2018-03-04 21:26:08', N'F001', 5)

