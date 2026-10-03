export function MensagensEnviar({ aluno }){
    if (!aluno) return null

    const faltas = Number(aluno.faltas)
    const responsavel = aluno.responsavel || aluno.responsaveis?.[0]
    const nomeResponsavel = typeof responsavel === "string"
        ? responsavel
        : responsavel?.nome || "responsável"

    if (faltas >= 15) {
        return (
            <p className="msg-15">
                COMUNICADO OFICIAL: Olá, {nomeResponsavel}. Informamos que o(a) aluno(a) {aluno.nome} atingiu o limite máximo de 15 faltas sem justificativa.
                Conforme o regulamento escolar, a vaga do aluno foi cancelada. Para mais informações ou orientações, favor procurar a secretaria da escola.
            </p>
        )
    }

    if (faltas >= 4) {
        return (
            <p className="msg-4-14">
                AVISO IMPORTANTE: Olá, {nomeResponsavel}. O(a) aluno(a) {aluno.nome} atingiu {faltas} faltas sem justificativa e está em situação
                crítica de frequência. Lembramos que ao atingir 15 faltas não justificadas, ocorre o cancelamento automático da vaga. Compareça à coordenação
                ou insira a justificativa no aplicativo Sala do Futuro urgentemente.
            </p>
        )
    }

    if (faltas === 3) {
        return (
            <p className="msg-3">
                Olá, {nomeResponsavel}. Identificamos que o(a) aluno(a) {aluno.nome} já acumula {faltas} faltas sem justificativa. O acompanhamento das
                aulas é essencial para o seu desempenho escolar. Pedimos que entre em contato com a escola ou anexe a justificativa no Sala do Futuro o quanto
                antes para regularizar a situação.
            </p>
        )
    }

    if (faltas >= 1) {
        return (
            <p className="msg-1-2">
                Olá, {nomeResponsavel}. Notamos que o(a) aluno(a) {aluno.nome} faltou à aula sem justificativa. Caso haja uma justificativa para o não comparecimento,
                por favor, envie o comprovante diretamente pelo aplicativo Sala do Futuro para atualização da frequência.
            </p>
        )
    }

    return (
        <p className="msg-0">
            Olá, {nomeResponsavel}. Esta é uma mensagem do(a) professor(a) de {aluno.nome} sobre o acompanhamento escolar do(a) aluno(a).
        </p>
    )
}
