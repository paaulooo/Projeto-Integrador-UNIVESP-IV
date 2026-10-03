from sqlalchemy.orm import Session

from app.models.aluno import Aluno
from app.models.falta import Falta


def obter_registros_falta(db: Session, aluno_id: int) -> list[dict]:
    faltas = db.query(Falta).filter(Falta.aluno_id == aluno_id).all()
    return [
        {"data": f.data, "presente": f.presente, "justificada": f.justificada}
        for f in faltas
    ]


def recalcular_estatisticas_aluno(db: Session, aluno: Aluno) -> list[dict]:
    registros = obter_registros_falta(db, aluno.id)

    total = len(registros)
    nao_justificadas = sum(1 for r in registros if not r["presente"] and not r["justificada"])
    presentes = sum(1 for r in registros if r["presente"])

    aluno.faltas = nao_justificadas
    aluno.perc_presenca = (presentes / total * 100) if total else 100.0

    db.commit()
    db.refresh(aluno)

    return registros
