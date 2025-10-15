from pydantic import BaseModel
from datetime import datetime
from models.finalidade import BaseLegal

class FinalidadeBase(BaseModel):
    nome: str
    descricao: str
    base_legal: BaseLegal

class FinalidadeCreate(FinalidadeBase):
    pass

class Finalidade(FinalidadeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True