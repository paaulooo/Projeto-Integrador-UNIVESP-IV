from datetime import date

from pydantic import BaseModel, ConfigDict


class AlunoBase(BaseModel):
    nome: str
    data_nascimento: date
    matricula: str
    sala_id: int


class AlunoCreate(AlunoBase):
    pass


class AlunoUpdate(AlunoBase):
    pass


class AlunoRead(AlunoBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
