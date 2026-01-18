from pydantic import BaseModel
from datetime import datetime

class OpcaoTratamentoBase(BaseModel):
    chave_politica: str
    titulo: str
    descricao: str

class OpcaoTratamentoCreate(OpcaoTratamentoBase):
    pass

class OpcaoTratamento(OpcaoTratamentoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True