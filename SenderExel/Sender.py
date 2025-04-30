import requests 
import pandas as pd

archivo = pd.ExcelFile(r"D:\UNIVERSIDAD\PROYECTOS\TREP 5GRUPO\SenderExel\Datos.xlsx", engine="openpyxl")

# Cambiar el nombre de la hoja
df = archivo.parse(sheet_name="ActasElectoralesTranscripcion")

base_url = "http://localhost:8000"

def get_recuento_TREP(
    code: str,
    papeletsInAnfora: int,
    papeletsDontUsed: int,
    validVotes: int,
    whiteVotes: int,
    nullVotes: int,
    pr1: int,
    pr2: int,
    pr3: int,
    pr4: int,
):
    errores_str = "No"
    hay_negativos = False
    hay_decimales = False

    def verificar_entero(valor, nombre=''):
        nonlocal hay_negativos, hay_decimales
        try:
            valor = float(valor)
            if valor != int(valor):
                hay_decimales = True
            valor = int(valor)
            if valor < 0:
                hay_negativos = True
            return valor
        except ValueError:
            print(f"[ERROR] El valor '{valor}' del campo '{nombre}' no es numérico.")
            return None

    papeletsInAnfora = verificar_entero(papeletsInAnfora, "Anfora")
    papeletsDontUsed = verificar_entero(papeletsDontUsed, "NoUsadas")
    validVotes = verificar_entero(validVotes, "Validos")
    whiteVotes = verificar_entero(whiteVotes, "Blancos")
    nullVotes = verificar_entero(nullVotes, "Nulos")
    pr1 = verificar_entero(pr1, 'Partido1')
    pr2 = verificar_entero(pr2, 'Partido2')
    pr3 = verificar_entero(pr3, 'Partido3')
    pr4 = verificar_entero(pr4, 'Partido4')

    if hay_negativos:
        errores_str += " - Error números negativos"
    if hay_decimales:
        errores_str += " - Error números decimales"
    
    params = {
        "code": code,
        "papeletsInAnfora": papeletsInAnfora,
        "papeletsDontUsed": papeletsDontUsed,
        #"citicensAvailables": 0,  # Ya no está disponible, se pone 0 o se elimina del backend si no es necesario
        "validVotes": validVotes,
        "whiteVotes": whiteVotes,
        "nullVotes": nullVotes,
        #"tablee": 0,  # Ya no está disponible
        #"codeRecint": "",  # Ya no está disponible
        #"tableCode": code, #Ya no se usa
        "pr1": pr1,
        "pr2": pr2,
        "pr3": pr3,
        "pr4": pr4,
        "Epdf": errores_str
    }

    response = requests.get(f"{base_url}/recuento-OFICIAL", params=params)

    if response.ok:
        return response.json()  
    else:
        try:
            raise Exception(f"Error {response.status_code}: {response.text}")
        except ValueError:
            print("algo anda mal")

# Llamado a la función con los nuevos datos
for index, row in df.iterrows():
    get_recuento_TREP(
        code=row['CodigoMesa'],
        papeletsInAnfora=row['CantidadAnfora'],
        papeletsDontUsed=row['PapeletasNoUsadas'],
        validVotes=row['Validos'],
        whiteVotes=row['Blancos'],
        nullVotes=row['Nulos'],
        pr1=row['Partido1'],
        pr2=row['Partido2'],
        pr3=row['Partido3'],
        pr4=row['Partido4']
    )
