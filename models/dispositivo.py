
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship
from database import Base

class Dispositivo(Base):
    __tablename__ = "dispositivos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    localizacao = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now)
    registros_consentimento = relationship("RegistroConsentimento", back_populates="dispositivo")

