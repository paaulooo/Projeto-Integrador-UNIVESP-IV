from pydantic import BaseModel


class MensagemManualCreate(BaseModel):
    observacao: str | None = None


class MensagemManualRead(BaseModel):
    destinatarios_email: list[str]
    falhas_email: list[str]
    destinatarios_whatsapp: list[str]
    falhas_whatsapp: list[str]
    assunto: str
    mensagem: str
