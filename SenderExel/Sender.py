import requests 
import pandas as pd

archivo  = pd.ExcelFile(r"D:\UNIVERSIDAD\PROYECTOS\TREP 5GRUPO\SenderExel\Datos.xlsx", engine="openpyxl")

df = archivo.parse(sheet_name="ActasRapidas")

base_url="http://localhost:8000"

def get_recuento_TREP(
    code: str,
    papeletsInAnfora: int,
    papeletsDontUsed: int,
    citicensAvailables: int,
    validVotes: int,
    whiteVotes: int,
    nullVotes: int,
    tablee: int,
    codeRecint: str,
    tableCode: str,
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

    papeletsInAnfora = verificar_entero(papeletsInAnfora,"1" )
    papeletsDontUsed = verificar_entero(papeletsDontUsed,"2")
    citicensAvailables = verificar_entero(citicensAvailables,"3")
    validVotes = verificar_entero(validVotes,"4")
    whiteVotes = verificar_entero(whiteVotes,"5")
    nullVotes = verificar_entero(nullVotes,"6")
    tablee = verificar_entero(tablee,"7")
    pr1 = verificar_entero(pr1, 'pr1')
    pr2 = verificar_entero(pr2, 'pr2')
    pr3 = verificar_entero(pr3, 'pr3')
    pr4 = verificar_entero(pr4, 'pr4')

    if hay_negativos:
        errores_str = errores_str + "Error números negativos"
    if hay_decimales:
        errores_str = errores_str + "Error números negativos"
    
    params = {
        "code": code,
        "papeletsInAnfora": papeletsInAnfora,
        "papeletsDontUsed": papeletsDontUsed,
        "citicensAvailables": citicensAvailables,
        "validVotes": validVotes,
        "whiteVotes": whiteVotes,
        "nullVotes": nullVotes,
        "tablee": tablee,
        "codeRecint": codeRecint,
        "tableCode": tableCode,
        "pr1": pr1,
        "pr2": pr2,
        "pr3": pr3,
        "pr4": pr4,
        "Epdf":errores_str
    }

    response = requests.get(f"{base_url}/recuento-OFICIAL", params=params)

    if response.ok:
        return response.json()  
    else:
        try:
            raise Exception(f"Error {response.status_code}: {response.text}")
        except ValueError:
            print("algo anda mal")
        


for index, row in df.iterrows():
    get_recuento_TREP(
        code=row['CodigoMesa'],
        papeletsInAnfora=row['CantidadAnfora'],
        papeletsDontUsed=row['PapeletasNoUsadas'],
        citicensAvailables=row['CantidadHabilitada'],
        validVotes=row['Validos'],
        whiteVotes=row['Blancos'],
        nullVotes=row['Nulos'],
        tablee=row['Mesa'],
        codeRecint=row['CodigoRecintoElectoralD'],
        tableCode=row['CodigoMesa'],  # Si 'Mesa' es el código de la mesa
        pr1=row['Partido1'],
        pr2=row['Partido2'],
        pr3=row['Partido3'],
        pr4=row['Partido4']
    )

