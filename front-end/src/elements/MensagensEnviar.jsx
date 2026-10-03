export function MensagensEnviar({ aluno }){
    if (!aluno) return null

    const faltas = Number(aluno.faltas)
    const responsavel = aluno.responsavel || aluno.responsaveis?.[0]
    const nomeResponsavel = typeof responsavel === "string"
        ? responsavel
        : responsavel?.nome || "responsável"

    if (faltas >= 1 && faltas <= 2) {
        return (
            <p className="msg-1-2">
                Olá, {nomeResponsavel}. Notamos que o(a) aluno(a) {aluno.nome} faltou à aula hoje. Caso haja uma justificativa para o não comparecimento, 
                por favor, envie o comprovante diretamente pelo aplicativo Sala do Futuro para atualização da frequência.
            </p>
        )
    }

    if (faltas === 3) {
        return (
            <p className="msg-3">
                Olá, {nomeResponsavel}. Identificamos que o(a) aluno(a) {aluno.nome} já acumula {aluno.faltas} faltas sem justificativa. O acompanhamento das
                 aulas é essencial para o seu desempenho escolar. Pedimos que entre em contato com a escola ou anexe a justificativa no Sala do Futuro o quanto
                  antes para regularizar a situação.
            </p>
        )
    }

    if (faltas >= 4 && faltas <= 7) {
        return (
            <p className="msg-4-7">
                AVISO IMPORTANTE: Olá, {nomeResponsavel}. O(a) aluno(a) {aluno.nome} atingiu {aluno.faltas} faltas sem justificativa e está em situação 
                crítica de frequência. Lembramos que ao atingir 15 faltas não justificadas, ocorre o cancelamento automático da vaga. Compareça à coordenação 
                ou insira a justificativa no aplicativo Sala do Futuro urgentemente.
            </p>
        )
    }

    if (faltas === 15) {
        return (
            <p className="msg-15">
                COMUNICADO OFICIAL: Olá, {nomeResponsavel}. Informamos que o(a) aluno(a) {aluno.nome} atingiu o limite máximo de 15 faltas sem justificativa. 
                Conforme o regulamento escolar, a vaga do aluno foi cancelada. Para mais informações ou orientações, favor procurar a secretaria da escola.
            </p>
        )
    }

    return null
}