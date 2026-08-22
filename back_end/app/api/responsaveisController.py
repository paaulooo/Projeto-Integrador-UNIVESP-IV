from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.aluno import Aluno
from app.models.responsavel import Responsavel
from app.schemas.responsavel import ResponsavelCreate, ResponsavelRead, ResponsavelUpdate

router = APIRouter(prefix="/responsaveis", tags=["responsaveis"])


def _get_alunos_or_404(db: Session, aluno_ids: list[int]) -> list[Aluno]:
    alunos = db.query(Aluno).filter(Aluno.id.in_(aluno_ids)).all()
    if len(alunos) != len(set(aluno_ids)):
        raise HTTPException(status_code=404, detail="Um ou mais alunos não encontrados")
    return alunos


def _to_read(responsavel: Responsavel) -> ResponsavelRead:
    return ResponsavelRead(
        id=responsavel.id,
        nome=responsavel.nome,
        telefone=responsavel.telefone,
        email=responsavel.email,
        parentesco=responsavel.parentesco,
        aluno_ids=[aluno.id for aluno in responsavel.alunos],
    )


@router.post("/", response_model=ResponsavelRead, status_code=201)
def create_responsavel(responsavel: ResponsavelCreate, db: Session = Depends(get_db)):
    alunos = _get_alunos_or_404(db, responsavel.aluno_ids)
    db_responsavel = Responsavel(
        nome=responsavel.nome,
        telefone=responsavel.telefone,
        email=responsavel.email,
        parentesco=responsavel.parentesco,
        alunos=alunos,
    )
    db.add(db_responsavel)
    db.commit()
    db.refresh(db_responsavel)
    return _to_read(db_responsavel)


@router.get("/", response_model=list[ResponsavelRead])
def list_responsaveis(db: Session = Depends(get_db)):
    return [_to_read(r) for r in db.query(Responsavel).all()]


@router.get("/{responsavel_id}", response_model=ResponsavelRead)
def get_responsavel(responsavel_id: int, db: Session = Depends(get_db)):
    responsavel = db.get(Responsavel, responsavel_id)
    if responsavel is None:
        raise HTTPException(status_code=404, detail="Responsável não encontrado")
    return _to_read(responsavel)


@router.put("/{responsavel_id}", response_model=ResponsavelRead)
def update_responsavel(
    responsavel_id: int, responsavel_update: ResponsavelUpdate, db: Session = Depends(get_db)
):
    responsavel = db.get(Responsavel, responsavel_id)
    if responsavel is None:
        raise HTTPException(status_code=404, detail="Responsável não encontrado")
    alunos = _get_alunos_or_404(db, responsavel_update.aluno_ids)
    responsavel.nome = responsavel_update.nome
    responsavel.telefone = responsavel_update.telefone
    responsavel.email = responsavel_update.email
    responsavel.parentesco = responsavel_update.parentesco
    responsavel.alunos = alunos
    db.commit()
    db.refresh(responsavel)
    return _to_read(responsavel)


@router.delete("/{responsavel_id}", status_code=204)
def delete_responsavel(responsavel_id: int, db: Session = Depends(get_db)):
    responsavel = db.get(Responsavel, responsavel_id)
    if responsavel is None:
        raise HTTPException(status_code=404, detail="Responsável não encontrado")
    db.delete(responsavel)
    db.commit()
