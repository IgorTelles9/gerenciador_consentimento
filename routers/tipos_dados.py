from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/tipos_dados", tags=["Tipos de Dados"])

@router.post("/", response_model=schemas.TipoDeDado)
def create_tipo_de_dado(tipo_dado: schemas.TipoDeDadoCreate, db: Session = Depends(get_db)):
    return crud.create_tipo_dado(db=db, tipo_dado=tipo_dado)

@router.get("/", response_model=List[schemas.TipoDeDado])
def read_tipos_de_dados(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_tipos_dados(db, skip=skip, limit=limit)