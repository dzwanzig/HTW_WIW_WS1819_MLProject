if machineError:
# update last error
cursor.execute(&quot;UPDATE dbo.Machine_Status SET Last_Error = ? WHERE
Machine_ID = ?;&quot;,
machineError.Timestamp, machine.Machine_ID)
cnxn.commit()
# read latest data
cursor.execute(&quot;SELECT TOP 1 Drehzahl, Leistungsaufnahme, Vibration,
Lautstaerke, Temperatur, FehlerID, Produktionsprogramm FROM
dbo.Maschinendaten_20181206 WHERE Machine_ID = ? ORDER BY Timestamp DESC;&quot;,
machine.Machine_ID)
machineStatus = cursor.fetchone()
if machineStatus:
currentStatus = &quot;Running&quot;
if str(machineStatus.FehlerID).startswith(&quot;F&quot;):
currentStatus = &quot;Error&quot;
elif str(machineStatus.FehlerID).startswith(&quot;A&quot;):
currentStatus = &quot;Maintenance&quot;
# update machine status to latest data
cursor.execute(&quot;UPDATE dbo.Machine_Status SET Status = ?, Revolutions
= ?, Power_Consumption = ?, Vibration = ?, Volume = ?, Temperature = ?,
Error_ID = ?, Production_Program = ? WHERE Machine_ID = ?;&quot;,
currentStatus, machineStatus.Drehzahl,
machineStatus.Leistungsaufnahme, machineStatus.Vibration,
machineStatus.Lautstaerke, machineStatus.Temperatur, machineStatus.FehlerID,
machineStatus.Produktionsprogramm, machine.Machine_ID)
cnxn.commit()
# everything is up to date. return data to Power BI.
Machine_Status = pd.read_sql(&quot;SELECT * FROM dbo.Machine_Status&quot;, cnxn)
