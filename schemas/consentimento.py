from pydantic import BaseModel
from datetime import datetime
from .opcao_tratamento import OpcaoTratamento
from models.consentimento import StatusConsentimento

class RegistroConsentimentoBase(BaseModel):
    titular_id: int
    dispositivo_id: int
    finalidade_id: int
    opcao_tratamento_id: int

class RegistroConsentimentoCreate(RegistroConsentimentoBase):
    pass

class RegistroConsentimento(RegistroConsentimentoBase):
    id: int
    status: StatusConsentimento
    data_registro: datetime
    opcao_escolhida: OpcaoTratamento

    class Config:
        from_attributes = True