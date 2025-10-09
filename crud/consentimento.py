from sqlalchemy.orm import Session
import models
import schemas
from datetime import datetime, timezone

def create_registro_consentimento(db: Session, consentimento: schemas.RegistroConsentimentoCreate):
    """ Cria um novo registro de consentimento e um log de auditoria. """
    db_consentimento = models.RegistroConsentimento(
        titular_id=consentimento.titular_id,
        dispositivo_id=consentimento.dispositivo_id,
        finalidade_id=consentimento.finalidade_id,
        opcao_tratamento_id=consentimento.opcao_tratamento_id,
        status=models.StatusConsentimento.ATIVO,
    )

    db.add(db_consentimento)
    db.flush()

    log_auditoria = models.LogAuditoriaConsentimento(
        registro_id=db_consentimento.id,
        acao="CONCESSÃO",
        detalhes=f"Usuario {consentimento.titular_id} concedeu consentimento para o dispositivo {consentimento.dispositivo_id} com a finalidade {consentimento.finalidade_id} e a opcao de tratamento {consentimento.opcao_tratamento_id}."
    )
    db.add(log_auditoria)

    db.commit()
    db.refresh(db_consentimento)
    return db_consentimento

def get_consentimentos_por_titular(db: Session, titular_id: int):
    """
    Busca todos os registros de consentimento ativos para um determinado titular.
    """
    return db.query(models.RegistroConsentimento).filter(
        models.RegistroConsentimento.titular_id == titular_id,
        models.RegistroConsentimento.status == models.StatusConsentimento.ATIVO
    ).all()

def revogar_consentimento(db: Session, consentimento_id: int):
    """
    Revoga um consentimento, atualizando seu status e criando um log de auditoria.
    """
    db_consentimento = db.query(models.RegistroConsentimento).filter(
        models.RegistroConsentimento.id == consentimento_id
    ).first()

    if not db_consentimento:
        return None

    db_consentimento.status = models.StatusConsentimento.REVOGADO
    db_consentimento.data_revogacao = datetime.now(timezone.utc)
    
    log_auditoria = models.LogAuditoriaConsentimento(
        registro_id=db_consentimento.id,
        acao="REVOGAÇÃO",
        detalhes=f"Consentimento revogado pelo titular."
    )
    db.add(log_auditoria)
    
    db.commit()
    db.refresh(db_consentimento)
    
    return db_consentimento