from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.sala import Sala
from app.schemas.sala import SalaCreate, SalaRead, SalaUpdate

router = APIRouter(prefix="/salas", tags=["salas"])


@router.post("/", response_model=SalaRead, status_code=201)
def create_sala(sala: SalaCreate, db: Session = Depends(get_db)):
    db_sala = Sala(**sala.model_dump())
    db.add(db_sala)
    db.commit()
    db.refresh(db_sala)
    return db_sala


@router.get("/", response_model=list[SalaRead])
def list_salas(db: Session = Depends(get_db)):
    return db.query(Sala).all()


@router.get("/{sala_id}", response_model=SalaRead)
def get_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.get(Sala, sala_id)
    if sala is None:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    return sala


@router.put("/{sala_id}", response_model=SalaRead)
def update_sala(sala_id: int, sala_update: SalaUpdate, db: Session = Depends(get_db)):
    sala = db.get(Sala, sala_id)
    if sala is None:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    for field, value in sala_update.model_dump().items():
        setattr(sala, field, value)
    db.commit()
    db.refresh(sala)
    return sala


@router.delete("/{sala_id}", status_code=204)
def delete_sala(sala_id: int, db: Session = Depends(get_db)):
    sala = db.get(Sala, sala_id)
    if sala is None:
        raise HTTPException(status_code=404, detail="Sala não encontrada")
    db.delete(sala)
    db.commit()
