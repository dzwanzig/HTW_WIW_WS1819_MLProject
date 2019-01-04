import pymssql
import pandas as pd
from datetime import timedelta


def get_df():
    """function returns whole machine data table as a pandas data frame"""
    password = "Masterprojekt"
    conn = pymssql.connect("pcs.f4.htw-berlin.de",
                           "Masterprojekt", password, "PraediktiveAnalysenTest")
    df = pd.read_sql('SELECT * FROM Maschinendaten_20181206', conn)
    conn.close()
    return(df)


def get_latest(menge):
    """function returns latest n row from machine data table on project db as a list"""
    menge = str(menge)
    sql = str('SELECT TOP ' + menge +
              ' * FROM Maschinendaten_20181206 ORDER BY ID DESC')
    password = "Masterprojekt"
    conn = pymssql.connect("pcs.f4.htw-berlin.de",
                           "Masterprojekt", password, "PraediktiveAnalysenTest")
    df = pd.read_sql(sql, conn)
    counter = []
    for x in range(20, 0, -1):
        counter.append(x)
    df["Counter"] = counter
    conn.close()
    return(df)

def read_db_20():
    """ This function connects to machine data table in the prediction database, reads the last 20 rows and stores them with a counter in a pandas data frame.
    The pandas data frame will be returned. """
    password = "Masterprojekt"
    conn = pymssql.connect("pcs.f4.htw-berlin.de",
                           "Masterprojekt", password, "PraediktiveAnalysenTest")
    df = pd.read_sql(
        'SELECT TOP 20 * FROM Maschinendaten_20181206 ORDER BY ID DESC', conn)
    # adding the counter
    counter = []
    for x in range(20, 0, -1):
        counter.append(x)
    df["Counter"] = counter
    return(df)


def rul_write(df, rul, method="LinRegression", failure="not_defined"):
    """ rul_write stores the predicted useful life in the prediction table in the project database. \n
    df - Pandas DataFrame \n
    rul - remaining useful life in seconds as integer \n
    method - used prediction method to predict rul \n
    failure - predicted failure, "not_defined" by average """
    password = "Masterprojekt"
    conn = pymssql.connect("pcs.f4.htw-berlin.de",
                           "Masterprojekt", password, "PraediktiveAnalysenTest")
    cursor = conn.cursor()
    id_old = pd.read_sql(
        'SELECT TOP 1 ID FROM predictions ORDER BY ID DESC', conn)
    id_new = id_old['ID']
    id_new = id_new[0] + 1
    last_timestamp = df['Timestamp']
    time = last_timestamp[0]
    rul_time = time + timedelta(seconds=rul)
    new_row = tuple((str(id_new), str(time), str(method), "XL_400_1", str(
        rul_time), str(failure), "5"))  # all elements in tuple have to be strings
    sql = "INSERT INTO Predictions VALUES (%d, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, new_row)
    conn.commit()
    print("Row for commit:" + str(new_row))
    conn.close()
