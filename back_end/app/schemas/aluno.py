from datetime import date

from pydantic import BaseModel, ConfigDict


class ResponsavelAlunoRead(BaseModel):
    id: int
    nome: str

    model_config = ConfigDict(from_attributes=True)


class AlunoBase(BaseModel):
    nome: str
    data_nascimento: date
    matricula: str
    sala_id: int
    faltas: int = 0
    perc_presenca: float = 100.0


class AlunoCreate(AlunoBase):
    pass


class AlunoUpdate(AlunoBase):
    pass


class AlunoRead(AlunoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    responsaveis: list[ResponsavelAlunoRead] = []
    responsavel: str | None = None
