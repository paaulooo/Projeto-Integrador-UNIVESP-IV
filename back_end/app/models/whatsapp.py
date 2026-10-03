import httpx
from pydantic import BaseModel

from app.config import settings

CALLMEBOT_URL = "https://api.callmebot.com/whatsapp.php"


class WhatsAppMessage(BaseModel):
    telefone: str
    apikey: str
    mensagem: str


def _normalizar_telefone(telefone: str) -> str:
    """Normaliza um telefone em formato livre (ex: "11999990001") para o
    padrao esperado pelo CallMeBot (DDI + numero, sem simbolos, sem "+")."""
    bruto = telefone.strip()
    digitos = "".join(ch for ch in bruto if ch.isdigit())

    if bruto.startswith("+"):
        return digitos

    if not digitos.startswith(settings.whatsapp_default_country_code):
        digitos = f"{settings.whatsapp_default_country_code}{digitos}"

    return digitos


async def sendWhatsApp(mensagem: WhatsAppMessage) -> None:
    numero = _normalizar_telefone(mensagem.telefone)

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.get(
            CALLMEBOT_URL,
            params={
                "phone": numero,
                "text": mensagem.mensagem,
                "apikey": mensagem.apikey,
            },
        )

    response.raise_for_status()
    corpo = response.text.lower()
    if "queued" not in corpo and "success" not in corpo:
        raise RuntimeError(f"Falha ao enviar WhatsApp via CallMeBot: {response.text}")
