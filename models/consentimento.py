import enum
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class StatusConsentimento(enum.Enum):
    ATIVO = "ativo"
    REVOGADO = "revogado"
    EXPIRADO = "expirado"

class RegistroConsentimento(Base):
    __tablename__ = "registros_consentimento"
    id = Column(Integer, primary_key=True, index=True)
    status = Column(Enum(StatusConsentimento), default=StatusConsentimento.ATIVO, nullable=False)
    data_registro = Column(DateTime(timezone=True), server_default=func.now())
    data_revogacao = Column(DateTime(timezone=True), nullable=True)
    data_expiracao = Column(DateTime(timezone=True), nullable=True)
    opcao_tratamento_id = Column(Integer, ForeignKey("opcoes_tratamento.id"), nullable=False)
    titular_id = Column(Integer, ForeignKey("titulares.id"), nullable=False)
    dispositivo_id = Column(Integer, ForeignKey("dispositivos.id"), nullable=False)
    tipo_de_dado_id = Column(Integer, ForeignKey("tipos_de_dados.id"), nullable=False)
    finalidade_id = Column(Integer, ForeignKey("finalidades.id"), nullable=False)
    opcao_tratamento = relationship("OpcaoDeTratamento")
    titular = relationship("Titular", back_populates="registros_consentimento")
    dispositivo = relationship("Dispositivo", back_populates="registros_consentimento")
    tipo_de_dado = relationship("TipoDeDado", back_populates="registros_consentimento")
    finalidade = relationship("Finalidade", back_populates="registros_consentimento")
    logs_auditoria = relationship("LogAuditoriaConsentimento", back_populates="registro_consentimento", cascade="all, delete-orphan")


class LogAuditoriaConsentimento(Base):
    __tablename__ = "logs_auditoria_consentimento"
    id = Column(Integer, primary_key=True, index=True)
    registro_id = Column(Integer, ForeignKey("registros_consentimento.id"), nullable=False)
    acao = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    detalhes = Column(String)
    registro_consentimento = relationship("RegistroConsentimento", back_populates="logs_auditoria")