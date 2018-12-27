import pymssql
import pandas as pd
from datetime import timedelta


def get_df():
    """function returns whole machine data table as a pandas data frame"""
    password = "Masterprojekt"
    conn = pymssql.connect("pcs.f4.htw-berlin.de",
                           "Masterprojekt", password, "PraediktiveAnalysenTest")
    df = pd.read_sql('SELECT * FROM Maschinendaten_20181122', conn)
    conn.close()
    return(df)


def get_latest(menge):
    """function returns latest n row from machine data table on project db as a list"""
    menge = str(menge)
    sql = str('SELECT TOP ' + menge +
              ' * FROM Maschinendaten_20181122 ORDER BY ID DESC')
    password = "Masterprojekt"
    conn = pymssql.connect("pcs.f4.htw-berlin.de",
                           "Masterprojekt", password, "PraediktiveAnalysenTest")
    df = pd.read_sql(sql, conn)
    conn.close()
    return(df)


def write_sim_data(data_id_nr, machine_id, time, datum, uhrzeit, std_dz, std_la, std_vb, std_ls, std_te, fehler_id, prod_programm, soll_menge, ist_menge, ausschuss, machine_nr=5):
    """ function takes following variables:
    data_id_nr, machine_id, time, datum, uhrzeit, std_dz, std_la, std_vb, std_ls, std_te, fehler_id, prod_programm, soll_menge, ist_menge, ausschuss, machine_nr = 5
    and writes them as a new row in to the machine data table on project db"""
    password = "Masterprojekt"
    conn = pymssql.connect("pcs.f4.htw-berlin.de",
                           "Masterprojekt", password, "PraediktiveAnalysenTest")
    cursor = conn.cursor()
    new_row = tuple(("400_1_" + str(data_id_nr), machine_id, time, datum, uhrzeit, std_dz, std_la, std_vb, std_ls, std_te, fehler_id,
                     prod_programm, soll_menge, ist_menge, ausschuss, machine_nr))
    cursor.executemany(
        "INSERT INTO Maschinendaten_20181122 VALUES (%d, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
        [new_row])
    conn.commit()
    conn.close()


def read_db_20():
    """ This function connects to machine data table in the prediction database, reads the last 20 rows and stores them with a counter in a pandas data frame.
    The pandas data frame will be returned. """
    password = "Masterprojekt"
    conn = pymssql.connect("pcs.f4.htw-berlin.de",
                           "Masterprojekt", password, "PraediktiveAnalysenTest")
    df = pd.read_sql(
        'SELECT TOP 20 * FROM Maschinendaten_20181122 ORDER BY ID DESC', conn)
    # adding the counter
    counter = [20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8,
               7, 6, 5, 4, 3, 2, 1]
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
