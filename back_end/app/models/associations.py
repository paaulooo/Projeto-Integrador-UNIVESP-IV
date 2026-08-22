from sqlalchemy import Column, ForeignKey, Integer, Table

from app.database import Base

aluno_responsavel = Table(
    "aluno_responsavel",
    Base.metadata,
    Column("aluno_id", Integer, ForeignKey("alunos.id"), primary_key=True),
    Column("responsavel_id", Integer, ForeignKey("responsaveis.id"), primary_key=True),
)
