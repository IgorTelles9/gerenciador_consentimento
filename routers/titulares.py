from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db
router = APIRouter(
    prefix="/titulares",
    tags=["Titulares"]
)

@router.post("/", response_model=schemas.Titular)
def create_titular(titular: schemas.TitularCreate, db: Session = Depends(get_db)):
    """ Cria um novo titular de dados. """
    # Verifica se o titular já existe
    db_titular = crud.get_titular_by_email(db, email=titular.email)
    if db_titular:
        raise HTTPException(status_code=400, detail="Titular já cadastrado.")
    return crud.create_titular(db=db, titular=titular)

@router.get("/", response_model=List[schemas.Titular])
def get_titulares(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """ Busca todos os titulares com paginação. """
    titulares = crud.get_titulares(db, skip=skip, limit=limit)
    return titulares

@router.get("/{titular_id}", response_model=schemas.Titular)
def get_titular(titular_id: int, db: Session = Depends(get_db)):
    """ Busca um titular específico pelo ID. """
    db_titular = crud.get_titular(db, titular_id=titular_id)
    if db_titular is None:
        raise HTTPException(status_code=404, detail="Titular não encontrado.")
    return db_titular