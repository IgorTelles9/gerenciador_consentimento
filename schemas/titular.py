from pydantic import BaseModel, EmailStr
from datetime import datetime

class TitularBase(BaseModel):
    email: EmailStr
    nome: str

class TitularCreate(TitularBase):
    pass

class Titular(TitularBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
