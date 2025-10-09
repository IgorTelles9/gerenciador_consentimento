from sqlalchemy.orm import Session
import models
import schemas

def get_opcao_tratamento(db: Session, opcao_tratamento_id: int):
    return db.query(models.OpcaoDeTratamento).filter(models.OpcaoDeTratamento.id == opcao_tratamento_id).first()

def get_opcoes_tratamento(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.OpcaoDeTratamento).offset(skip).limit(limit).all()

def create_opcao_tratamento(db: Session, opcao_tratamento: schemas.OpcaoTratamentoCreate):
    db_opcao_tratamento = models.OpcaoDeTratamento(**opcao_tratamento.model_dump())
    db.add(db_opcao_tratamento)
    db.commit()
    db.refresh(db_opcao_tratamento)
    return db_opcao_tratamento