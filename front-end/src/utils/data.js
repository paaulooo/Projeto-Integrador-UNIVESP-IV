export function diaUtilAtualISO() {
    const hoje = new Date()
    const diaSemana = hoje.getDay()

    if (diaSemana === 0) hoje.setDate(hoje.getDate() - 2)
    if (diaSemana === 6) hoje.setDate(hoje.getDate() - 1)

    const ano = hoje.getFullYear()
    const mes = String(hoje.getMonth() + 1).padStart(2, "0")
    const dia = String(hoje.getDate()).padStart(2, "0")
    return `${ano}-${mes}-${dia}`
}
