from pydantic import BaseModel, ConfigDict


class ResponsavelBase(BaseModel):
    nome: str
    telefone: str
    email: str
    parentesco: str


class ResponsavelCreate(ResponsavelBase):
    aluno_ids: list[int] = []


class ResponsavelUpdate(ResponsavelBase):
    aluno_ids: list[int] = []


class ResponsavelRead(ResponsavelBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    aluno_ids: list[int]
