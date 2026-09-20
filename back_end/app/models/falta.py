from datetime import date

from sqlalchemy import Boolean, Date, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Falta(Base):
    __tablename__ = "faltas"
    __table_args__ = (UniqueConstraint("aluno_id", "data", name="uq_falta_aluno_data"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    aluno_id: Mapped[int] = mapped_column(Integer, ForeignKey("alunos.id"), nullable=False)
    data: Mapped[date] = mapped_column(Date, nullable=False)
    presente: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    justificada: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    aluno = relationship("Aluno", back_populates="registros_faltas")
