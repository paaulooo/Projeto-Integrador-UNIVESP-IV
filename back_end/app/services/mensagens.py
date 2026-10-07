from dataclasses import dataclass

from app.models.regra_res_falta import regra_faltas_consecutivas, regra_perc_falta

LIMITE_SEGURO_WHATSAPP = 600  # caracteres; o CallMeBot trunca mensagens longas sem avisar
LIMITE_FALTAS_CONSECUTIVAS = 3
LIMITE_PERC_FALTAS_DIAS = 30
LIMITE_PERC_FALTAS = 0.025
LIMITE_CANCELAMENTO_VAGA = 15
LIMITE_SITUACAO_CRITICA = 4
LIMITE_ACOMPANHAMENTO = 3


@dataclass
class MensagemFalta:
    titulo: str
    emoji: str
    assunto: str
    aluno_nome: str
    descricao: str
    acao: str
    mensagem: str  # descricao + acao combinados, usado no corpo do email


def _contar_faltas_nao_justificadas(registros: list[dict]) -> int:
    return sum(1 for r in registros if not r["presente"] and not r["justificada"])


def montar_mensagem_falta(
    aluno_nome: str, responsavel_nome: str, registros: list[dict]
) -> MensagemFalta:
    faltas_total = _contar_faltas_nao_justificadas(registros)
    consecutivas = regra_faltas_consecutivas(registros, lim=LIMITE_FALTAS_CONSECUTIVAS)
    percentual = regra_perc_falta(
        registros, dias=LIMITE_PERC_FALTAS_DIAS, lim=LIMITE_PERC_FALTAS
    )

    if faltas_total >= LIMITE_CANCELAMENTO_VAGA:
        titulo = "Comunicado oficial"
        emoji = "🚨"
        descricao = (
            f"COMUNICADO OFICIAL: Olá, {responsavel_nome}. Informamos que o(a) aluno(a) "
            f"{aluno_nome} atingiu o limite máximo de {LIMITE_CANCELAMENTO_VAGA} faltas sem "
            "justificativa. Conforme o regulamento escolar, a vaga do aluno foi cancelada."
        )
        acao = "Para mais informações ou orientações, favor procurar a secretaria da escola."
    elif faltas_total >= LIMITE_SITUACAO_CRITICA:
        titulo = "Aviso importante de frequência"
        emoji = "🚨"
        descricao = (
            f"AVISO IMPORTANTE: Olá, {responsavel_nome}. O(a) aluno(a) {aluno_nome} atingiu "
            f"{faltas_total} faltas sem justificativa e está em situação crítica de "
            f"frequência. Lembramos que ao atingir {LIMITE_CANCELAMENTO_VAGA} faltas não "
            "justificadas, ocorre o cancelamento automático da vaga."
        )
        acao = "Compareça à coordenação ou insira a justificativa no aplicativo Sala do Futuro urgentemente."
    elif faltas_total >= LIMITE_ACOMPANHAMENTO:
        titulo = "Aviso de frequência"
        emoji = "⚠️"
        descricao = (
            f"Olá, {responsavel_nome}. Identificamos que o(a) aluno(a) {aluno_nome} já "
            f"acumula {faltas_total} faltas sem justificativa. O acompanhamento das aulas é "
            "essencial para o seu desempenho escolar."
        )
        acao = (
            "Entre em contato com a escola ou anexe a justificativa no Sala do Futuro "
            "o quanto antes para regularizar a situação."
        )
    elif faltas_total >= 1:
        titulo = "Aviso de falta"
        emoji = "⚠️"
        descricao = (
            f"Olá, {responsavel_nome}. Notamos que o(a) aluno(a) {aluno_nome} faltou à aula "
            "sem justificativa."
        )
        acao = (
            "Caso haja uma justificativa para o não comparecimento, envie o comprovante "
            "diretamente pelo aplicativo Sala do Futuro para atualização da frequência."
        )
    else:
        titulo = "Contato da escola"
        emoji = "💬"
        descricao = (
            f"Olá, {responsavel_nome}. Esta é uma mensagem do(a) professor(a) de "
            f"{aluno_nome} sobre o acompanhamento escolar do(a) aluno(a)."
        )
        acao = "Nenhuma ação necessária no momento."

    if consecutivas.disparada and faltas_total < LIMITE_CANCELAMENTO_VAGA:
        descricao += (
            f" Atenção: já são {int(consecutivas.peso)} faltas consecutivas sem "
            "justificativa, o que indica um padrão preocupante de ausências seguidas."
        )

    if percentual.disparada and faltas_total < LIMITE_CANCELAMENTO_VAGA:
        descricao += (
            f" O(a) aluno(a) também ultrapassou o limite de faltas recentes "
            f"({percentual.detalhe} nos últimos {LIMITE_PERC_FALTAS_DIAS} dias)."
        )

    assunto = f"{titulo} - {aluno_nome}"
    mensagem = f"{descricao} {acao}"
    return MensagemFalta(
        titulo=titulo,
        emoji=emoji,
        assunto=assunto,
        aluno_nome=aluno_nome,
        descricao=descricao,
        acao=acao,
        mensagem=mensagem,
    )


def _truncar(texto: str, tamanho: int) -> str:
    if tamanho <= 0:
        return ""
    if len(texto) <= tamanho:
        return texto
    return texto[: max(tamanho - 1, 0)].rstrip() + "…"


def formatar_mensagem_whatsapp(msg: MensagemFalta, observacao: str | None = None) -> str:
    rodape = (
        f"💡 Você recebeu esta mensagem por ser responsável cadastrado(a) por "
        f"{msg.aluno_nome} no sistema escolar."
    )

    def montar(descricao: str, obs: str | None, incluir_rodape: bool) -> str:
        partes = [
            f"{msg.emoji} *{msg.titulo.upper()}*",
            f"*{msg.aluno_nome}*",
            "",
            "📋 *Descrição:*",
            descricao,
            "",
            "📌 *O que fazer:*",
            msg.acao,
        ]
        if obs:
            partes += ["", "📝 *Observação do(a) professor(a):*", obs]
        if incluir_rodape:
            partes += ["", rodape]
        return "\n".join(partes)

    texto = montar(msg.descricao, observacao, incluir_rodape=True)
    if len(texto) <= LIMITE_SEGURO_WHATSAPP:
        return texto

    # O rodape e dispensavel; corta primeiro pra tentar caber no limite seguro.
    texto = montar(msg.descricao, observacao, incluir_rodape=False)
    if len(texto) <= LIMITE_SEGURO_WHATSAPP:
        return texto

    # Ainda nao coube: encurta a descricao (a parte mais variavel), preservando
    # acao e observacao, que sao as partes mais importantes pro responsavel.
    excesso = len(texto) - LIMITE_SEGURO_WHATSAPP
    descricao_truncada = _truncar(msg.descricao, max(len(msg.descricao) - excesso, 0))
    texto = montar(descricao_truncada, observacao, incluir_rodape=False)
    if len(texto) <= LIMITE_SEGURO_WHATSAPP:
        return texto

    # Caso extremo: ate a observacao do professor e grande demais pra caber. Encurta ela tambem.
    excesso = len(texto) - LIMITE_SEGURO_WHATSAPP
    obs_truncada = _truncar(observacao or "", max(len(observacao or "") - excesso, 0))
    return montar(descricao_truncada, obs_truncada, incluir_rodape=False)
