from pydantic import BaseModel

class Acta(BaseModel):
    code: str
    papeletsInAnfora: int
    papeletsDontUsed: int
    citicensAvailables: int
    validVotes: int
    whiteVotes: int
    nullVotes: int
    pdfSize: float
    tablee: int
    codeRecint: str
    tableCode: str
