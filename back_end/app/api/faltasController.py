from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aluno import Aluno
from app.models.falta import Falta
from app.schemas.falta import FaltaCreate, FaltaRead, FaltaUpdate

router = APIRouter(prefix="/faltas", tags=["faltas"])

_DETALHE_DUPLICADA = "Já existe um registro de falta para esse aluno nessa data"


def _get_aluno_or_404(db: Session, aluno_id: int) -> Aluno:
    aluno = db.get(Aluno, aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


@router.post("/", response_model=FaltaRead, status_code=201)
def create_falta(falta: FaltaCreate, db: Session = Depends(get_db)):
    _get_aluno_or_404(db, falta.aluno_id)
    db_falta = Falta(**falta.model_dump())
    db.add(db_falta)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=_DETALHE_DUPLICADA)
    db.refresh(db_falta)
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
def update_falta(falta_id: int, falta_update: FaltaUpdate, db: Session = Depends(get_db)):
    falta = db.get(Falta, falta_id)
    if falta is None:
        raise HTTPException(status_code=404, detail="Falta não encontrada")
    _get_aluno_or_404(db, falta_update.aluno_id)
    for field, value in falta_update.model_dump().items():
        setattr(falta, field, value)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail=_DETALHE_DUPLICADA)
    db.refresh(falta)
    return falta


@router.delete("/{falta_id}", status_code=204)
def delete_falta(falta_id: int, db: Session = Depends(get_db)):
    falta = db.get(Falta, falta_id)
    if falta is None:
        raise HTTPException(status_code=404, detail="Falta não encontrada")
    db.delete(falta)
    db.commit()
