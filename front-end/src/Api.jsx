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

export default api