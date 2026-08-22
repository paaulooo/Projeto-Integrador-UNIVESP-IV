from pydantic import BaseModel, ConfigDict


class SalaBase(BaseModel):
    nome: str
    capacidade: int
    turno: str


class SalaCreate(SalaBase):
    pass


class SalaUpdate(SalaBase):
    pass


class SalaRead(SalaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
