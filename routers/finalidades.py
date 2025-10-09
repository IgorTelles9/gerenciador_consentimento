from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/finalidades", tags=["Finalidades"])

@router.post("/", response_model=schemas.Finalidade)
def create_finalidade(finalidade: schemas.FinalidadeCreate, db: Session = Depends(get_db)):
    return crud.create_finalidade(db=db, finalidade=finalidade)

@router.get("/", response_model=List[schemas.Finalidade])
def read_finalidades(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_finalidades(db, skip=skip, limit=limit)