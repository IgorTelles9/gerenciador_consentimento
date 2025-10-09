from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class TipoDeDado(Base):
    __tablename__ = "tipos_de_dados"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.now)
    descricao = Column(String)
    registros_consentimento = relationship("RegistroConsentimento", back_populates="tipo_de_dado")