from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aluno import Aluno
from app.models.sala import Sala
from app.schemas.aluno import AlunoCreate, AlunoRead, AlunoUpdate

router = APIRouter(prefix="/alunos", tags=["alunos"])


def _to_read(aluno: Aluno) -> AlunoRead:
    aluno_read = AlunoRead.model_validate(aluno)
    nome_responsavel = aluno.responsaveis[0].nome if aluno.responsaveis else None
    return aluno_read.model_copy(update={"responsavel": nome_responsavel})


def _get_sala_or_404(db: Session, sala_id: int) -> Sala:
    sala = db.get(Sala, sala_id)
    if sala is None:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return sala


@router.post("/", response_model=AlunoRead, status_code=201)
def create_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    _get_sala_or_404(db, aluno.sala_id)
    db_aluno = Aluno(**aluno.model_dump())
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return _to_read(db_aluno)


@router.get("/", response_model=list[AlunoRead])
def list_alunos(db: Session = Depends(get_db)):
    return [_to_read(aluno) for aluno in db.query(Aluno).all()]


@router.get("/{aluno_id}", response_model=AlunoRead)
def get_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.get(Aluno, aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return _to_read(aluno)


@router.put("/{aluno_id}", response_model=AlunoRead)
def update_aluno(aluno_id: int, aluno_update: AlunoUpdate, db: Session = Depends(get_db)):
    aluno = db.get(Aluno, aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    _get_sala_or_404(db, aluno_update.sala_id)
    for field, value in aluno_update.model_dump().items():
        setattr(aluno, field, value)
    db.commit()
    db.refresh(aluno)
    return _to_read(aluno)


@router.delete("/{aluno_id}", status_code=204)
def delete_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.get(Aluno, aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(aluno)
    db.commit()
