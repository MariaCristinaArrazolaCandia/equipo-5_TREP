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


def insertar_acta_validaB(acta,parsed_values):
    conn = get_connectionB()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO VotingRecord (
            code, papeletsInAnfora, papeletsDontUsed, citicensAvailables,
            validVotes, whiteVotes, nullVotes, pdfSize, tablee,
            status, codeRecint, tableCode
        )
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        acta.code,
        acta.papeletsInAnfora,
        acta.papeletsDontUsed,
        acta.citicensAvailables,
        acta.validVotes,
        acta.whiteVotes,
        acta.nullVotes,
        acta.pdfSize,
        acta.tablee,
        1,        # status
        acta.codeRecint,
        acta.tableCode
    ))

    voting_record_id = cursor.fetchone()[0]

    aux = 1
    for votos in parsed_values:
            cursor.execute("""
                INSERT INTO Votes (
                    quantity,status,idParty ,idVotingRecord
                )
                VALUES (?, ?, ?, ?)
            """, (votos, 1, aux, voting_record_id))
            aux = aux + 1
    conn.commit()
    conn.close()

def insertar_acta_invalidaB(acta, errores):
    conn = get_connectionB()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO VotingRecord (
            code, papeletsInAnfora, papeletsDontUsed, citicensAvailables,
            validVotes, whiteVotes, nullVotes, pdfSize, tablee,
            status, codeRecint, tableCode
        )
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        acta.code,
        acta.papeletsInAnfora,
        acta.papeletsDontUsed,
        acta.citicensAvailables,
        acta.validVotes,
        acta.whiteVotes,
        acta.nullVotes,
        acta.pdfSize,
        acta.tablee,
        2,        # status
        acta.codeRecint,
        acta.tableCode
    ))
    voting_record_id = cursor.fetchone()[0]

    for id_categoria, mensaje in errores:
            cursor.execute("""
                INSERT INTO VotingError (
                    observation, idVotingRecord, idError
                )
                VALUES (?, ?, ?)
            """, (mensaje, voting_record_id, id_categoria))

    conn.commit()
    conn.close()



def existe_en_voting_actB(tableCode, codeRecint):
    conn = get_connectionB()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM VotingAct
        WHERE tableCode = ? AND codeRecint = ?
    """, (tableCode, codeRecint))

    resultado = cursor.fetchone()
    conn.close()

    return resultado is not None

def existe_en_voting_recordB(Code):
    conn = get_connectionB()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM VotingRecord
        WHERE code = ?
    """, (Code))

    resultado = cursor.fetchone()
    conn.close()

    return resultado is not None

def existe_en_voting_actB(tableCode, codeRecint):
    conn = get_connectionB()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM VotingAct
        WHERE tableCode = ? AND codeRecint = ?
    """, (tableCode, codeRecint))

    resultado = cursor.fetchone()
    conn.close()

    return resultado is not None

def Insert_ErrorB(Code):
    conn = get_connectionB()
    cursor = conn.cursor()

    # Buscar el ID en VotingRecord según el código
    cursor.execute("""
        SELECT id FROM VotingRecord WHERE code = ?
    """, (Code))
    row = cursor.fetchone()

    if row is None:
        conn.close()

    voting_record_id = row[0]

    # Insertar el error usando el ID obtenido
    cursor.execute("""
        INSERT INTO VotingError (
            observation, idVotingRecord, idError
        )
        VALUES (?, ?, 3)
    """, ("Papeleta ya fue registrada", voting_record_id))

    conn.commit()
    conn.close()

def conseguir_datos(code):
    conn = get_connectionB()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT va.papeletsInAnfora, va.nTable, r.code AS recintCode, va.tableCode
            FROM VotingAct va
            JOIN Recint r ON va.codeRecint = r.code
            WHERE va.tableCode = ?
        """, (code,))
        
        result = cursor.fetchone()

        if result:
            citicensAvailables, tablee, codeRecint, tableCode = result
        else:
            print(f"[AVISO] No se encontró información para el código de mesa: {code}")
            citicensAvailables, tablee, codeRecint, tableCode = 0, 0, "", code

    except Exception as e:
        print(f"[ERROR] Fallo al obtener datos de la base para {code}: {e}")
        citicensAvailables, tablee, codeRecint, tableCode = 0, 0, "", code

    finally:
        conn.close()

    return citicensAvailables, tablee, codeRecint, tableCode

def InsertFantasmaB(acta, errores):
    conn = get_connectionB()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO VotingRecord (
            code, papeletsInAnfora, papeletsDontUsed, citicensAvailables,
            validVotes, whiteVotes, nullVotes, pdfSize, tablee,
            status, codeRecint, tableCode
        )
        OUTPUT INSERTED.id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        acta.code,
        acta.papeletsInAnfora,
        acta.papeletsDontUsed,
        acta.citicensAvailables,
        acta.validVotes,
        acta.whiteVotes,
        acta.nullVotes,
        acta.pdfSize,
        acta.tablee,
        2,        # status
        "ERROR",
        acta.tableCode
    ))
    voting_record_id = cursor.fetchone()[0]

    for id_categoria, mensaje in errores:
            cursor.execute("""
                INSERT INTO VotingError (
                    observation, idVotingRecord, idError
                )
                VALUES (?, ?, ?)
            """, (mensaje, voting_record_id, id_categoria))

    conn.commit()
    conn.close()
