import logging

from app.config import settings
from app.models.email import sendTemplateEmail
from app.models.whatsapp import WhatsAppMessage, sendWhatsApp
from app.services.mensagens import formatar_mensagem_whatsapp, montar_mensagem_falta

logger = logging.getLogger(__name__)


async def notificar_responsaveis_falta(
    aluno_nome: str, responsaveis: list[dict], registros: list[dict]
) -> None:
    if not responsaveis:
        logger.warning(
            "Nenhum responsavel cadastrado para %s; notificacao de falta nao enviada", aluno_nome
        )
        return

    for responsavel in responsaveis:
        msg = montar_mensagem_falta(aluno_nome, responsavel["nome"], registros)

        try:
            await sendTemplateEmail(
                recipients=[responsavel["email"]],
                subject=msg.assunto,
                template_name="aviso_falta.html",
                context={
                    "titulo": msg.titulo,
                    "aluno_nome": aluno_nome,
                    "mensagem": msg.mensagem,
                    "observacao": None,
                    "escola_nome": settings.mail_from_name,
                    "portal_url": settings.portal_url,
                },
            )
        except Exception:
            logger.exception(
                "Falha ao enviar email de falta para %s (responsavel %s)",
                aluno_nome,
                responsavel.get("email"),
            )

        telefone = responsavel.get("telefone")
        apikey = responsavel.get("whatsapp_apikey")
        if telefone and apikey:
            try:
                await sendWhatsApp(
                    WhatsAppMessage(
                        telefone=telefone,
                        apikey=apikey,
                        mensagem=formatar_mensagem_whatsapp(msg),
                    )
                )
            except Exception:
                logger.exception(
                    "Falha ao enviar whatsapp de falta para %s (responsavel %s)",
                    aluno_nome,
                    telefone,
                )
        elif telefone:
            logger.info(
                "Responsavel %s nao fez opt-in no CallMeBot; whatsapp nao enviado",
                responsavel.get("email"),
            )
