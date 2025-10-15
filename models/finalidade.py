from sqlalchemy import Column, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime
import enum

class BaseLegal(enum.Enum):
    CONSENTIMENTO = "Consentimento"
    OBRIGACAO_LEGAL = "Obrigação Legal"
    EXECUCAO_CONTRATO = "Execução de Contrato"
    PROTECAO_VIDA = "Proteção da Vida"
    LEGITIMO_INTERESSE = "Legítimo Interesse"

class Finalidade(Base):
    __tablename__ = "finalidades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(String)
    base_legal = Column(Enum(BaseLegal), nullable=False, default=BaseLegal.CONSENTIMENTO)
    created_at = Column(DateTime, default=datetime.now)
    registros_consentimento = relationship("RegistroConsentimento", back_populates="finalidade")
