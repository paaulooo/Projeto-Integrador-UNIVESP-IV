import axios from 'axios'

const API_URL = import.meta.env.VITE_APP_API_URL;

const api = axios.create({
  baseURL: API_URL,
  timeout: 15000,
});

export const getAlunos = async () => {
  const response = await api.get('/alunos');
  return response.data;
}
export const getFaltas = async () => {
  const response = await api.get('/faltas');
  return response.data;
}
export const getResponsaveis = async () => {
  const response = await api.get('/responsaveis/');
  return response.data;
}

export const criarFalta = async (falta) => {
  const response = await api.post('/faltas/', falta);
  return response.data;
}

export const atualizarFalta = async (faltaId, falta) => {
  const response = await api.put(`/faltas/${faltaId}`, falta);
  return response.data;
}

export const salvarFrequenciaDoDia = async (registros) => {
  const resultados = []
  for (const registro of registros) {
    try {
      resultados.push(await criarFalta(registro))
    } catch (err) {
      if (err?.response?.status === 409) {
        const faltas = (await api.get('/faltas')).data
        const existente = faltas.find((falta) => (
          falta.aluno_id === registro.aluno_id && falta.data === registro.data
        ))
        if (existente) {
          resultados.push(await atualizarFalta(existente.id, registro))
          continue
        }
      }
      throw err
    }
  }
  return resultados
}

export const enviarMensagemManual = async (alunoId, observacao) => {
  const response = await api.post(`/alunos/${alunoId}/mensagens`, { observacao: observacao || null });
  return response.data;
}

export default api