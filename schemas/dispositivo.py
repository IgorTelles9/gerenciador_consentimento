from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DispositivoBase(BaseModel):
    nome: str
    localizacao: Optional[str] = None

class DispositivoCreate(DispositivoBase):
    pass

class Dispositivo(DispositivoBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

        
