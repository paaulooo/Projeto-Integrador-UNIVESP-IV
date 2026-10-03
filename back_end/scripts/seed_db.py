"""Popula database.db com dados de teste (salas, alunos, responsaveis e faltas).

Uso: python -m scripts.seed_db
"""

from datetime import date, timedelta

from app import models  # noqa: F401 - registra os models no metadata
from app.database import Base, SessionLocal, engine
from app.models.aluno import Aluno
from app.models.falta import Falta
from app.models.responsavel import Responsavel
from app.models.sala import Sala
from app.services.estatisticas import recalcular_estatisticas_aluno


def _dias_uteis_anteriores(quantidade: int, a_partir_de: date | None = None) -> list[date]:
    """Retorna as `quantidade` datas de dias úteis (seg-sex) mais recentes, mais antiga primeiro."""
    referencia = a_partir_de or date.today()
    dias: list[date] = []
    cursor = referencia
    while len(dias) < quantidade:
        cursor -= timedelta(days=1)
        if cursor.weekday() < 5:
            dias.append(cursor)
    return list(reversed(dias))


def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        sala_a = Sala(nome="Sala A", capacidade=30, turno="manha")
        db.add(sala_a)
        db.flush()

        lucas = Aluno(
            nome="Lucas Silva",
            data_nascimento=date(2015, 3, 12),
            matricula="2026001",
            sala_id=sala_a.id,
        )
        beatriz = Aluno(
            nome="Beatriz Rocha",
            data_nascimento=date(2014, 11, 2),
            matricula="2026002",
            sala_id=sala_a.id,
        )
        gabriel = Aluno(
            nome="Gabriel Santos",
            data_nascimento=date(2015, 7, 19),
            matricula="2026003",
            sala_id=sala_a.id,
        )
        sofia = Aluno(
            nome="Sofia Almeida",
            data_nascimento=date(2014, 5, 30),
            matricula="2026004",
            sala_id=sala_a.id,
        )
        db.add_all([lucas, beatriz, gabriel, sofia])
        db.flush()

        resp_lucas = Responsavel(
            nome="Patricia Silva",
            telefone="11999990001",
            email="paulorobertofer98+lucas@gmail.com",
            parentesco="mae",
        )
        resp_beatriz = Responsavel(
            nome="Marcelo Rocha",
            telefone="11999990002",
            email="paulorobertofer98+beatriz@gmail.com",
            parentesco="pai",
        )
        resp_gabriel = Responsavel(
            nome="Roberto Santos",
            telefone="11999990003",
            email="paulorobertofer98+gabriel@gmail.com",
            parentesco="pai",
        )
        resp_sofia = Responsavel(
            nome="Camila Almeida",
            telefone="11999990004",
            email="paulorobertofer98+sofia@gmail.com",
            parentesco="mae",
        )
        resp_lucas.alunos.append(lucas)
        resp_beatriz.alunos.append(beatriz)
        resp_gabriel.alunos.append(gabriel)
        resp_sofia.alunos.append(sofia)
        db.add_all([resp_lucas, resp_beatriz, resp_gabriel, resp_sofia])
        db.flush()

        dias = _dias_uteis_anteriores(10)

        faltas = []
        # Lucas Silva: 2 faltas nao consecutivas -> tier "Aviso de falta"
        faltas.append(Falta(aluno_id=lucas.id, data=dias[0], presente=False, justificada=False))
        faltas.append(Falta(aluno_id=lucas.id, data=dias[2], presente=True, justificada=False))
        faltas.append(Falta(aluno_id=lucas.id, data=dias[4], presente=False, justificada=False))

        # Beatriz Rocha: nenhuma falta
        faltas.append(Falta(aluno_id=beatriz.id, data=dias[1], presente=True, justificada=False))
        faltas.append(Falta(aluno_id=beatriz.id, data=dias[3], presente=True, justificada=False))

        # Gabriel Santos: 4 faltas consecutivas -> tier "situacao critica" + aviso de consecutivas
        for dia in dias[4:8]:
            faltas.append(Falta(aluno_id=gabriel.id, data=dia, presente=False, justificada=False))

        # Sofia Almeida: 6 faltas (3 consecutivas) -> tier "situacao critica"
        for dia in dias[0:3]:
            faltas.append(Falta(aluno_id=sofia.id, data=dia, presente=False, justificada=False))
        faltas.append(Falta(aluno_id=sofia.id, data=dias[3], presente=True, justificada=False))
        for dia in dias[4:7]:
            faltas.append(Falta(aluno_id=sofia.id, data=dia, presente=False, justificada=False))

        db.add_all(faltas)
        db.commit()

        for aluno in (lucas, beatriz, gabriel, sofia):
            recalcular_estatisticas_aluno(db, aluno)

        print("Banco populado com sucesso:")
        print(f"  Salas: {db.query(Sala).count()}")
        print(f"  Alunos: {db.query(Aluno).count()}")
        print(f"  Responsaveis: {db.query(Responsavel).count()}")
        print(f"  Faltas: {db.query(Falta).count()}")
        for aluno in (lucas, beatriz, gabriel, sofia):
            print(f"    {aluno.nome}: faltas={aluno.faltas} perc_presenca={aluno.perc_presenca:.1f}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
