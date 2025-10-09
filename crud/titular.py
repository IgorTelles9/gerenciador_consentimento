from sqlalchemy.orm import Session
import models
import schemas 

def get_titular(db: Session, titular_id: int):
    """ Busca um único titular através do ID. """
    return db.query(models.Titular).filter(models.Titular.id == titular_id).first()

def get_titular_by_email(db: Session, email: str):
    """ Busca um único titular através do email. """
    return db.query(models.Titular).filter(models.Titular.email == email).first()

def get_titulares(db: Session, skip: int = 0, limit: int = 20):
    """ Busca todos todos os titulares com paginação. """
    return db.query(models.Titular).offset(skip).limit(limit).all()

def create_titular(db: Session, titular: schemas.TitularCreate):
    db_titular = models.Titular(email=titular.email, nome=titular.nome)
    db.add(db_titular)
    db.commit()
    db.refresh(db_titular)
    return db_titular