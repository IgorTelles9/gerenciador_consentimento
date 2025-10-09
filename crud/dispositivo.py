from sqlalchemy.orm import Session
import models
import schemas 

def get_dispositivo(db: Session, dispositivo_id: int):
    """ Busca um único dispositivo através do ID. """
    return db.query(models.Dispositivo).filter(models.Dispositivo.id == dispositivo_id).first()

def get_dispositivos(db: Session, skip: int = 0, limit: int = 20):
    """ Busca todos os dispositivos com paginação. """
    return db.query(models.Dispositivo).offset(skip).limit(limit).all()

def create_dispositivo(db: Session, dispositivo: schemas.DispositivoCreate):
    """ Cria um novo dispositivo. """
    db_dispositivo = models.Dispositivo(
        nome=dispositivo.nome, 
        localizacao=dispositivo.localizacao
    )
    db.add(db_dispositivo)
    db.commit()
    db.refresh(db_dispositivo)
    return db_dispositivo

def delete_dispositivo(db: Session, dispositivo_id: int):
    """ Remove um dispositivo. """
    db_dispositivo = db.query(models.Dispositivo).filter(models.Dispositivo.id == dispositivo_id).first()
    if db_dispositivo:
        db.delete(db_dispositivo)
        db.commit()
    return db_dispositivo
