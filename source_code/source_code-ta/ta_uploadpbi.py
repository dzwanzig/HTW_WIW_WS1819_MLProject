import pyodbc
from datetime import datetime
from datetime import timedelta
import pandas as pd

server = &#39;pcs.f4.htw-berlin.de&#39;

database = &#39;PraediktiveAnalysenTest&#39;
username = &#39;Masterprojekt&#39;
password = &#39;Masterprojekt&#39;
cnxn = pyodbc.connect(&#39;DRIVER={ODBC Driver 17 for SQL Server};SERVER=&#39; + server +
&#39;;PORT=1443;DATABASE=&#39; + database + &#39;;UID=&#39; + username + &#39;;PWD=&#39; + password)
cursor = cnxn.cursor()

# read status from all machines
cursor.execute(
&quot;SELECT Machine_ID, Status, Error_ID, Production_Program FROM dbo.Machine_Status;&quot;)
machines = cursor.fetchall()
for machine in machines:
#print(&quot;Machine:&quot;, machine)
# read latest prediction of the machine
cursor.execute(&quot;SELECT TOP 1 Ausfallzeitpunkt FROM dbo.Predictions WHERE Machine_ID = ?
ORDER BY Timestamp DESC;&quot;,
machine.Machine_ID)
prediction = cursor.fetchone()
if prediction:
now = datetime.now()
nextMaintenance = prediction.Ausfallzeitpunkt - timedelta(days=14)
if nextMaintenance &lt; now:
# set next maintenance to 1 year in future
nextMaintenance = nextMaintenance + timedelta(days=365)
# update next maintenance
cursor.execute(&quot;UPDATE dbo.Machine_Status SET Next_Maintenance = ? WHERE Machine_ID =
?;&quot;,
nextMaintenance, machine.Machine_ID)
cnxn.commit()
# read last error
cursor.execute(&quot;SELECT TOP 1 Timestamp FROM dbo.Maschinendaten_20181206 WHERE
Machine_ID = ? AND FehlerID LIKE &#39;F%&#39; ORDER BY Timestamp DESC;&quot;,
machine.Machine_ID)

machineError = cursor.fetchone()
if machineError:
# update last error
cursor.execute(&quot;UPDATE dbo.Machine_Status SET Last_Error = ? WHERE Machine_ID = ?;&quot;,
machineError.Timestamp, machine.Machine_ID)
cnxn.commit()
# read latest data
cursor.execute(&quot;SELECT TOP 1 Drehzahl, Leistungsaufnahme, Vibration, Lautstaerke, Temperatur,
FehlerID, Produktionsprogramm FROM dbo.Maschinendaten_20181206 WHERE Machine_ID = ?
ORDER BY Timestamp DESC;&quot;,
machine.Machine_ID)
machineStatus = cursor.fetchone()
if machineStatus:
currentStatus = &quot;Running&quot;
if str(machineStatus.FehlerID).startswith(&quot;F&quot;):
currentStatus = &quot;Error&quot;
elif str(machineStatus.FehlerID).startswith(&quot;A&quot;):
currentStatus = &quot;Maintenance&quot;
# update machine status to latest data
cursor.execute(&quot;UPDATE dbo.Machine_Status SET Status = ?, Revolutions = ?,
Power_Consumption = ?, Vibration = ?, Volume = ?, Temperature = ?, Error_ID = ?,
Production_Program = ? WHERE Machine_ID = ?;&quot;,
currentStatus, machineStatus.Drehzahl, machineStatus.Leistungsaufnahme,
machineStatus.Vibration, machineStatus.Lautstaerke, machineStatus.Temperatur,
machineStatus.FehlerID, machineStatus.Produktionsprogramm, machine.Machine_ID)
cnxn.commit()

# everything is up to date. return data to Power BI.
Machine_Status = pd.read_sql(&quot;SELECT * FROM dbo.Machine_Status&quot;, cnxn)
