import { useEffect, useState } from "react";
import { ListaAluno } from "./ListaAluno"
import Api from "../Api"
import "./styles/areaFrequencia.css"
export function AreaFrequencia(){
   const[isModalOpen, setIsModelOpen] = useState(false)
    const [alunos, setAlunos] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState("")

    const loadAlunos = async () => {
        setLoading(true)
        setError("")

        try {
            const response = await Api.get('/alunos')
            setAlunos(response.data?.alunos || [])
        } catch (err) {
            const status = err?.response?.status
            const detail = err?.response?.data?.detail
            const baseMessage = detail || err?.message || 'Erro ao carregar profissionais.'
            setError(status ? `${baseMessage} (HTTP ${status})` : baseMessage)
        } finally {
            setLoading(false)
        }
    }

    useEffect(() => {
        loadAlunos()
    }, [])

    const handleCreated = (novoAluno) => {
        if (novoAluno) {
            setAlunos((prev) => [novoAluno, ...prev])
        } else {
            loadAlunos()
        }
        setIsModelOpen(false)
    }
    return(
        <>
            <section className="containerAreaFrequencia">
                <div className="wrapperMarcarFrequencia">
                    <label className='labelCheckbox' htmlFor="replicar-frequencia">
                        <input type="checkbox" name="replicar-frequencia" />
                        Replicar frequência
                    </label>
                    <p className="marcacao">
                        Marcar todos como:
                        <span className="falta">F</span>
                        <span className="comparecimento">C</span>
                    </p>
                </div>
                <div className="wapperDivListAula">
                    <ul className="wrapperAluno">
                        <li>N°</li>
                        <li>Nome do Aluno </li>
                        <li>Presença</li>
                        <li>Mensagem</li>
                    </ul>
                    {error ? <p style={{ color: 'red' }}>{error}</p> : null}

            {loading ? (
                <p>Carregando alunos...</p>
            ) : (
                    <div>
                        {alunos.length === 0 ? (
                        <p>Nenhum aluno cadastrado ainda.</p>
                    ) : (
                        alunos.map((alunos) => (
                            <ListaAluno key={alunos.id} alunos={alunos} />
                        ))
                    )}

                    </div>
                 )}
                </div>
                <div className="wrapperBtnSalvar">

                <button className="btnSalvar">
                    Salvar
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                        <path d="M2.5 20.5V6.5C2.5 5.39543 3.39543 4.5 4.5 4.5H15.6716C16.202 4.5 16.7107 4.71071 17.0858 5.08579L19.9142 7.91421C20.2893 8.28929 20.5 8.79799 20.5 9.32843V20.5C20.5 21.6046 19.6046 22.5 18.5 22.5H4.5C3.39543 22.5 2.5 21.6046 2.5 20.5Z" fill="#D9D9D9" stroke="white" stroke-width="1.5"/>
                        <circle cx="2.5" cy="2.5" r="2.5" transform="matrix(-1 0 0 1 13.5 15.5)" fill="#176FF6"/>
                        <path d="M6.5 7.875V12.5H16.5V7.875C16.5 7.66788 16.2762 7.5 16 7.5H7C6.72386 7.5 6.5 7.66788 6.5 7.875Z" fill="#176FF6" stroke="white" stroke-width="1.5"/>
                    </svg>
                </button>
                </div>
            </section>
        </>
    )
}