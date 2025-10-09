from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud.dispositivo as crud_dispositivo
import schemas
from database import get_db

router = APIRouter(
    prefix="/dispositivos",
    tags=["Dispositivos"]
)

@router.post("/", response_model=schemas.Dispositivo)
def create_dispositivo(dispositivo: schemas.DispositivoCreate, db: Session = Depends(get_db)):
    """ Cria um novo dispositivo. """
    return crud_dispositivo.create_dispositivo(db=db, dispositivo=dispositivo)

@router.get("/", response_model=List[schemas.Dispositivo])
def get_dispositivos(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """ Busca todos os dispositivos com paginação. """
    dispositivos = crud_dispositivo.get_dispositivos(db, skip=skip, limit=limit)
    return dispositivos

@router.get("/{dispositivo_id}", response_model=schemas.Dispositivo)
def get_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    """ Busca um dispositivo específico pelo ID. """
    db_dispositivo = crud_dispositivo.get_dispositivo(db, dispositivo_id=dispositivo_id)
    if db_dispositivo is None:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado.")
    return db_dispositivo

@router.delete("/{dispositivo_id}")
def delete_dispositivo(dispositivo_id: int, db: Session = Depends(get_db)):
    """ Remove um dispositivo. """
    db_dispositivo = crud_dispositivo.get_dispositivo(db, dispositivo_id=dispositivo_id)
    if db_dispositivo is None:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado.")
    
    crud_dispositivo.delete_dispositivo(db=db, dispositivo_id=dispositivo_id)
    return {"message": "Dispositivo removido com sucesso."}
