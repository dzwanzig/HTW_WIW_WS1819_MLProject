import pymssql
import pandas as pd
from datetime import timedelta


def get_df():
    """function returns whole machine data table as a pandas data frame"""
    conn = pymssql.connect("pcs.f4.htw-berlin.de",
                           "Masterprojekt", "Masterprojekt", "PraediktiveAnalysenTest")
    df = pd.read_sql('SELECT * FROM Maschinendaten_20181206', conn)
    conn.close()
    return(df)


def get_latest(menge):
    """function returns latest n row from machine data table on project db as a list"""
    menge_sql = str(menge)
    sql = str('SELECT TOP ' + menge_sql +
              ' * FROM Maschinendaten_20181206 ORDER BY ID DESC')
    conn = pymssql.connect("pcs.f4.htw-berlin.de",
                           "Masterprojekt", "Masterprojekt", "PraediktiveAnalysenTest")
    df = pd.read_sql(sql, conn)
    counter = []
    for x in range(menge, 0, -1):
        counter.append(x)
    df["Counter"] = counter
    conn.close()
    return(df)


def rul_write(df, rul, method="LinRegression", failure="not_defined"):
    """ rul_write stores the predicted useful life in the prediction table in the project database. \n
    df - Pandas DataFrame \n
    rul - remaining useful life in seconds as integer \n
    method - used prediction method to predict rul \n
    failure - predicted failure, "not_defined" by average """
    conn = pymssql.connect("pcs.f4.htw-berlin.de",
                           "Masterprojekt", "Masterprojekt", "PraediktiveAnalysenTest")
    cursor = conn.cursor()
    id_old = pd.read_sql(
        'SELECT TOP 1 ID FROM predictions ORDER BY ID DESC', conn)
    id_new = id_old['ID']
    id_new = id_new[0] + 1
    last_timestamp = df['Timestamp']
    time = last_timestamp[0]
    rul_time = time + timedelta(seconds=rul)
    new_row = tuple((str(id_new), time, str(method), "XL_400_1",
                     rul_time, str(failure), "5"))  # all elements in tuple have to be strings
    sql = "INSERT INTO Predictions VALUES (%d, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, new_row)
    conn.commit()
    print("Row for commit:" + str(new_row))
    conn.close()
