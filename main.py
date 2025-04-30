from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from database_cluster_a import *
from database_cluster_b import *
from models import *

app = FastAPI()

@app.get("/")
def root():
    return {"mensaje": "API en funcionamiento"}    

@app.get("/recuento-TREP")
def recuento_TREP(
    code: str,
    papeletsInAnfora: int,
    papeletsDontUsed: int,
    citicensAvailables: int,
    validVotes: int,
    whiteVotes: int,
    nullVotes: int,
    pdfSize: float,
    tablee: int,
    codeRecint: str,
    tableCode: str,
    pr1:str,
    pr2:str,
    pr3:str,
    pr4:str,
    Eimagen:str
):
    errores = []
    pr_values = [pr1, pr2, pr3, pr4]
    parsed_values = []
    Isletter = False

    if not Eimagen.strip():
       errores.append((4,f"{Eimagen}"))

    acta = Acta(
        code=code,
        papeletsInAnfora=papeletsInAnfora,
        papeletsDontUsed=papeletsDontUsed,
        citicensAvailables=citicensAvailables,
        validVotes=validVotes,
        whiteVotes=whiteVotes,
        nullVotes=nullVotes,
        pdfSize=pdfSize,
        tablee=tablee,
        codeRecint=codeRecint,
        tableCode=tableCode
    )
    try:
        if existe_en_voting_actA(acta.tableCode, codeRecint) :
            if not existe_en_voting_recordA(acta.code):
                for value in pr_values:
                    try:
                        parsed_values.append(int(value.strip()))
                    except ValueError:
                        Isletter = True
                        errores.append((4, f"Letra detectada: {value}"))
                if Isletter:
                    insertar_acta_invalidaA(acta, errores)
                    return {"errors": errores}
                
                validado, errores = validar_acta(acta.dict(),parsed_values)

                if validado:
                    insertar_acta_validaA(acta,parsed_values)
                    return {"message": "Acta válida y lista para inserción"}
                else:
                    insertar_acta_invalidaA(acta, errores)
                    return {"errors": errores}
            else:
                Insert_ErrorA(acta.code) 
        else:
            try:
                errores.append((2, f"No existe el acta y/o mesa"))
                InsertFantasmaA(acta, errores)
            except ValueError:
                return {"error"}
    except ValueError:
        return {"error"}


@app.get("/recuento-OFICIAL")
def recuento_OFICIAL(
    code: str,
    papeletsInAnfora: int,
    papeletsDontUsed: int,
    #citicensAvailables: int,
    validVotes: int,
    whiteVotes: int,
    nullVotes: int,
    #tablee: int,
    #codeRecint: str,
    #tableCode: str,
    pr1:str,
    pr2:str,
    pr3:str,
    pr4:str,
    Epdf:str
):
    errores = []
    pr_values = [pr1, pr2, pr3, pr4]
    parsed_values = []
    Isletter = False    

    citicensAvailables, tablee, codeRecint, tableCode, = conseguir_datos(code)

    acta = Acta(
        code=code,
        papeletsInAnfora=papeletsInAnfora,
        papeletsDontUsed=papeletsDontUsed,
        citicensAvailables=citicensAvailables,
        validVotes=validVotes,
        whiteVotes=whiteVotes,
        nullVotes=nullVotes,
        pdfSize=0,
        tablee=tablee,
        codeRecint=codeRecint,
        tableCode=tableCode
    )

    if Epdf != "No":
        Isletter=True
        errores.append((4, f"{Epdf}"))
        insertar_acta_invalidaB(acta, errores)

    try:
        if existe_en_voting_actB(acta.tableCode, codeRecint) :
            if not existe_en_voting_recordB(acta.code):
                for value in pr_values:
                    try:
                        parsed_values.append(int(value.strip()))
                    except ValueError:
                        Isletter = True
                        errores.append((4, f"Dato incorrecto {value}"))
                if Isletter:
                    insertar_acta_invalidaB(acta, errores)
                    return {"errors": errores}
                
                validado, errores = validar_acta(acta.dict(),parsed_values)

                if validado:
                    insertar_acta_validaB(acta,parsed_values)
                    return {"message": "Acta válida y lista para inserción"}
                else:
                    insertar_acta_invalidaB(acta, errores)
                    return {"errors": errores}
            else:
                Insert_ErrorB(acta.code) 
        else:
            try:
                errores.append((2, f"No existe el acta y/o mesa"))
                InsertFantasmaB(acta, errores)
            except ValueError:
                return {"error"}
    except ValueError:
        return {"error"}



def validar_acta(acta,parsed_values):
    errores = []
    pr1 = parsed_values[0]
    pr2 = parsed_values[1]
    pr3 = parsed_values[2]
    pr4 = parsed_values[3]

    habilitados = acta["citicensAvailables"]
    boletas = acta["papeletsInAnfora"]
    no_usadas = acta["papeletsDontUsed"]
    if habilitados != boletas + no_usadas:
        diferencia = habilitados - (boletas + no_usadas)
        errores.append((1,
            f"Ciudadanos habilitados: {habilitados}, boletas: {boletas}, no usadas: {no_usadas} Diferencia de {diferencia} papeletas."
        ))
    votos_blancos = acta["whiteVotes"]
    votos_validos = acta["validVotes"]
    votos_nulos = acta["nullVotes"]
    votos_partidos = pr1 + pr2 +pr3 +pr4

    if acta["papeletsInAnfora"] != votos_validos + votos_nulos:
        diferencia = acta["papeletsInAnfora"] - (votos_validos + votos_nulos)
        errores.append((1,
            f"Votos validos: {votos_validos}, nulos: {votos_nulos} No coinciden con boletas en ánfora. Diferencia de {diferencia}."
        ))
    if votos_validos != votos_partidos + votos_blancos:
        diferencia = votos_validos - (votos_partidos + votos_blancos)
        errores.append((1,
            f"Votos de partidos {votos_partidos}, Votos blancos {votos_blancos} No coinciden con una diferencia de {diferencia}"
        ))

    if errores:
        return False, errores
    return True, ["Acta válida y lista para inserción"]