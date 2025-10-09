from sqlalchemy.orm import Session
import models
import schemas

def get_tipo_dado(db: Session, tipo_dado_id: int):
    return db.query(models.TipoDeDado).filter(models.TipoDeDado.id == tipo_dado_id).first()

def get_tipos_dados(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.TipoDeDado).offset(skip).limit(limit).all()

def create_tipo_dado(db: Session, tipo_dado: schemas.TipoDeDadoCreate):
    db_tipo_dado = models.TipoDeDado(**tipo_dado.model_dump())
    db.add(db_tipo_dado)
    db.commit()
    db.refresh(db_tipo_dado)
    return db_tipo_dado