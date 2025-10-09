from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import datetime

class Finalidade(Base):
    __tablename__ = "finalidades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False, unique=True)
    descricao = Column(String)
    base_legal = Column(String, default="Consentimento")
    created_at = Column(DateTime, default=datetime.now)
    registros_consentimento = relationship("RegistroConsentimento", back_populates="finalidade")
