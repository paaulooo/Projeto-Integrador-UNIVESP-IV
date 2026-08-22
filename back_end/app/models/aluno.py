from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.associations import aluno_responsavel

class Aluno(Base):
    __tablename__ = "alunos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    data_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    matricula: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    sala_id: Mapped[int] = mapped_column(Integer, ForeignKey("salas.id"), nullable=False)

    sala = relationship("Sala", back_populates="alunos")
    responsaveis = relationship("Responsavel", secondary=aluno_responsavel, back_populates="alunos")
