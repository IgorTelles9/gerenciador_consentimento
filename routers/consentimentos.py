from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import schemas
from database import get_db

router = APIRouter(prefix="/consentimentos", tags=["Consentimentos"])

@router.post("/", response_model=schemas.RegistroConsentimento)
def create_registro_consentimento(registro: schemas.RegistroConsentimentoCreate, db: Session = Depends(get_db)):
    """ Registra uma nova escolha de consentimento de um titular. """
    titular = crud.get_titular(db, id=registro.titular_id)
    if not titular:
        raise HTTPException(status_code=404, detail="Titular não encontrado.")
    dispositivo = crud.get_dispositivo(db, id=registro.dispositivo_id)
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado.")
    finalidade = crud.get_finalidade(db, id=registro.finalidade_id)
    if not finalidade:
        raise HTTPException(status_code=404, detail="Finalidade não encontrada.")
    opcao_tratamento = crud.get_opcao_tratamento(db, id=registro.opcao_tratamento_id)
    if not opcao_tratamento:
        raise HTTPException(status_code=404, detail="Opção de tratamento não encontrada.")
    return crud.create_registro_consentimento(db=db, registro=registro)

@router.get("/titular/{titular_id}", response_model=List[schemas.RegistroConsentimento])
def read_consentimentos_do_titular(titular_id: int, db: Session = Depends(get_db)):
    """
    Busca todas as permissões de consentimento ativas para um titular específico.
    """
    return crud.get_consentimentos_por_titular(db=db, titular_id=titular_id)

@router.patch("/{consentimento_id}/revogar", response_model=schemas.RegistroConsentimento)
def revoke_consentimento(consentimento_id: int, db: Session = Depends(get_db)):
    """
    Revoga um consentimento específico.
    """
    consentimento_revogado = crud.revogar_consentimento(db=db, consentimento_id=consentimento_id)
    if consentimento_revogado is None:
        raise HTTPException(status_code=404, detail="Registro de consentimento não encontrado")
    return consentimento_revogado