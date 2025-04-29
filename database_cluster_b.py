import pyodbc

def get_connectionB():
    conn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server};'
        'SERVER=SAC;'
        'DATABASE=dbTREP;'
        'UID=sa;'
        'PWD=sa;'    
    )
    return conn