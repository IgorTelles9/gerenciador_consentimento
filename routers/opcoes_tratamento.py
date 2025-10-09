from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from routers.titulares import get_db

router = APIRouter(prefix="/opcoes_tratamento", tags=["Opções de Tratamento"])

@router.post("/", response_model=schemas.OpcaoTratamento)
def create_opcao_tratamento(opcao: schemas.OpcaoTratamentoCreate, db: Session = Depends(get_db)):
    return crud.create_opcao_tratamento(db=db, opcao=opcao)

@router.get("/", response_model=List[schemas.OpcaoTratamento])
def read_opcoes_tratamento(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    return crud.get_opcoes_tratamento(db, skip=skip, limit=limit)