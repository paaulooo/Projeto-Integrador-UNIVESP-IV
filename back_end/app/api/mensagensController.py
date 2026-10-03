import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.aluno import Aluno
from app.models.email import sendTemplateEmail
from app.models.whatsapp import WhatsAppMessage, sendWhatsApp
from app.schemas.mensagem import MensagemManualCreate, MensagemManualRead
from app.services.estatisticas import obter_registros_falta
from app.services.mensagens import formatar_mensagem_whatsapp, montar_mensagem_falta

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alunos", tags=["mensagens"])


@router.post("/{aluno_id}/mensagens", response_model=MensagemManualRead, status_code=201)
async def enviar_mensagem_manual(
    aluno_id: int, payload: MensagemManualCreate, db: Session = Depends(get_db)
):
    aluno = db.get(Aluno, aluno_id)
    if aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    responsaveis = aluno.responsaveis
    if not responsaveis:
        raise HTTPException(status_code=422, detail="Aluno não possui responsável cadastrado")

    registros = obter_registros_falta(db, aluno.id)

    destinatarios_email: list[str] = []
    falhas_email: list[str] = []
    destinatarios_whatsapp: list[str] = []
    falhas_whatsapp: list[str] = []
    assunto = ""
    mensagem = ""

    for responsavel in responsaveis:
        msg = montar_mensagem_falta(aluno.nome, responsavel.nome, registros)
        assunto = msg.assunto
        mensagem = msg.mensagem

        try:
            await sendTemplateEmail(
                recipients=[responsavel.email],
                subject=msg.assunto,
                template_name="aviso_falta.html",
                context={
                    "titulo": msg.titulo,
                    "aluno_nome": aluno.nome,
                    "mensagem": msg.mensagem,
                    "observacao": payload.observacao,
                    "escola_nome": settings.mail_from_name,
                    "portal_url": settings.portal_url,
                },
            )
            destinatarios_email.append(responsavel.email)
        except Exception:
            logger.exception(
                "Falha ao enviar email manual para %s (responsavel %s)",
                aluno.nome,
                responsavel.email,
            )
            falhas_email.append(responsavel.email)

        if responsavel.telefone and responsavel.whatsapp_apikey:
            try:
                await sendWhatsApp(
                    WhatsAppMessage(
                        telefone=responsavel.telefone,
                        apikey=responsavel.whatsapp_apikey,
                        mensagem=formatar_mensagem_whatsapp(msg, payload.observacao),
                    )
                )
                destinatarios_whatsapp.append(responsavel.telefone)
            except Exception:
                logger.exception(
                    "Falha ao enviar whatsapp manual para %s (responsavel %s)",
                    aluno.nome,
                    responsavel.telefone,
                )
                falhas_whatsapp.append(responsavel.telefone)

    if not destinatarios_email and not destinatarios_whatsapp:
        raise HTTPException(
            status_code=502, detail="Falha ao enviar mensagem para os responsáveis"
        )

    return MensagemManualRead(
        destinatarios_email=destinatarios_email,
        falhas_email=falhas_email,
        destinatarios_whatsapp=destinatarios_whatsapp,
        falhas_whatsapp=falhas_whatsapp,
        assunto=assunto,
        mensagem=mensagem,
    )
