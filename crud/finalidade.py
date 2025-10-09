from sqlalchemy.orm import Session
import models
import schemas

def get_finalidade(db: Session, finalidade_id: int):
    return db.query(models.Finalidade).filter(models.Finalidade.id == finalidade_id).first()

def get_finalidades(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Finalidade).offset(skip).limit(limit).all()

def create_finalidade(db: Session, finalidade: schemas.FinalidadeCreate):
    db_finalidade = models.Finalidade(**finalidade.model_dump())
    db.add(db_finalidade)
    db.commit()
    db.refresh(db_finalidade)
    return db_finalidade
