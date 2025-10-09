from pydantic import BaseModel
from datetime import datetime

class FinalidadeBase(BaseModel):
    nome: str
    descricao: str
    base_legal: str = "Consentimento"

class FinalidadeCreate(FinalidadeBase):
    pass

class Finalidade(FinalidadeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True