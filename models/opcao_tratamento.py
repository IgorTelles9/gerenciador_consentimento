from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from database import Base
from datetime import datetime

class OpcaoDeTratamento(Base):
    __tablename__ = "opcoes_tratamento"
    id = Column(Integer, primary_key=True, index=True)
    chave_politica = Column(String, nullable=False, unique=True, index=True)
    titulo = Column(String, nullable=False, comment="Ex: Enviar todos os dados coletados em tempo real.")
    descricao = Column(String, nullable=False, comment="Ex: Os dados são coletados a cada 5 segundos e enviados em seguida, sem nenhum tipo de filtro ou tratamento.")
    created_at = Column(DateTime, default=datetime.now)