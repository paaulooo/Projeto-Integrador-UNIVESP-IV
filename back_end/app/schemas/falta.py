from datetime import date

from pydantic import BaseModel, ConfigDict, field_validator


class FaltaBase(BaseModel):
    aluno_id: int
    data: date
    presente: bool = True
    justificada: bool = False

    @field_validator("data")
    @classmethod
    def data_deve_ser_dia_util(cls, valor: date) -> date:
        if valor.weekday() >= 5:
            raise ValueError("data deve ser de segunda a sexta-feira")
        return valor


class FaltaCreate(FaltaBase):
    pass


class FaltaUpdate(FaltaBase):
    pass


class FaltaRead(FaltaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
