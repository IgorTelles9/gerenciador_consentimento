from pydantic import BaseModel
from datetime import datetime

class TipoDeDadoBase(BaseModel):
    nome: str
    descricao: str

class TipoDeDadoCreate(TipoDeDadoBase):
    pass 

class TipoDeDado(TipoDeDadoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True