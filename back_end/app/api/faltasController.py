from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aluno import Aluno
from app.models.falta import Falta
from app.schemas.falta import FaltaCreate, FaltaRead, FaltaUpdate
from app.services.estatisticas import recalcular_estatisticas_aluno
from app.services.notificacoes import notificar_responsaveis_falta

router = APIRouter(prefix="/faltas", tags=["faltas"])

_DETALHE_DUPLICADA = "Já existe um registro de falta para esse aluno nessa data"


def _get_aluno_or_404(db: Session, aluno_id: int) -> Aluno:
    aluno = db.get(Aluno, aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


def _agendar_notificacao(background_tasks: BackgroundTasks, db: Session, aluno: Aluno) -> None:
    registros = recalcular_estatisticas_aluno(db, aluno)
    responsaveis = [
        {
            "nome": responsavel.nome,
            "email": responsavel.email,
            "telefone": responsavel.telefone,
            "whatsapp_apikey": responsavel.whatsapp_apikey,
        }
        for responsavel in aluno.responsaveis
    ]
    background_tasks.add_task(notificar_responsaveis_falta, aluno.nome, responsaveis, registros)


@router.post("/", response_model=FaltaRead, status_code=201)
def create_falta(falta: FaltaCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    aluno = _get_aluno_or_404(db, falta.aluno_id)
    db_falta = Falta(**falta.model_dump())
    db.add(db_falta)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=_DETALHE_DUPLICADA)
    db.refresh(db_falta)

    if not db_falta.presente:
        _agendar_notificacao(background_tasks, db, aluno)
    else:
        recalcular_estatisticas_aluno(db, aluno)

    return db_falta


@router.get("/", response_model=list[FaltaRead])
def list_faltas(db: Session = Depends(get_db)):
    return db.query(Falta).all()


@router.get("/{falta_id}", response_model=FaltaRead)
def get_falta(falta_id: int, db: Session = Depends(get_db)):
    falta = db.get(Falta, falta_id)
    if falta is None:
        raise HTTPException(status_code=404, detail="Falta não encontrada")
    return falta


@router.put("/{falta_id}", response_model=FaltaRead)
def update_falta(
    falta_id: int,
    falta_update: FaltaUpdate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    falta = db.get(Falta, falta_id)
    if falta is None:
        raise HTTPException(status_code=404, detail="Falta não encontrada")
    aluno = _get_aluno_or_404(db, falta_update.aluno_id)
    passou_a_faltar = falta.presente and not falta_update.presente
    for field, value in falta_update.model_dump().items():
        setattr(falta, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=_DETALHE_DUPLICADA)
    db.refresh(falta)

    if passou_a_faltar:
        _agendar_notificacao(background_tasks, db, aluno)
    else:
        recalcular_estatisticas_aluno(db, aluno)

    return falta


@router.delete("/{falta_id}", status_code=204)
def delete_falta(falta_id: int, db: Session = Depends(get_db)):
    falta = db.get(Falta, falta_id)
    if falta is None:
        raise HTTPException(status_code=404, detail="Falta não encontrada")
    aluno = db.get(Aluno, falta.aluno_id)
    db.delete(falta)
    db.commit()
    if aluno is not None:
        recalcular_estatisticas_aluno(db, aluno)
