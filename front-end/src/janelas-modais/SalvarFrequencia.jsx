import SalvarEnviar from '../assets/SalvarEnviar.svg'
import './styles/salvarFrequencia.css'

export function SalvarFrequencia ({ onClose, alunos, numeroAluno }){
    return(
        <div className="salvarFrequenciaOverlay" onClick={onClose}>
            <section className="salvarFrequenciaModal" onClick={(event) => event.stopPropagation()}>
                <div className='alertaFrequência'>
                    <svg xmlns="http://www.w3.org/2000/svg" width="56" height="56" viewBox="0 0 56 56" fill="none">
                        <circle cx="28" cy="28" r="25.5" stroke="#519F76" stroke-width="5"/>
                        <line x1="12.0781" y1="25.9012" x2="21.1687" y2="38.4008" stroke="#519F76" stroke-width="6" stroke-linecap="round"/>
                        <line x1="21.1457" y1="38.7358" x2="44.6664" y2="17.886" stroke="#519F76" stroke-width="6" stroke-linecap="round"/>
                    </svg>
                    <h2>
                        Salvar frequência
                    </h2>
                    <p className='alunosAtivos'>Total de alunos ativos:</p>
                    <p className='presençasAlunos'>Presenças: </p>
                    <p className='faltasAlunos'>Ausência: </p>
                    <p className='MesagensAuto'>Mensagens enviadas automaticamente: </p>
                    <p className='avisoSalvarEnviar'>
                        <span>Aviso:</span> Quando clicar em “salva e enviar” vai enviar uma mensagem automáticamente para o s responsáveis do aluno que não compareceu a sua aula
                    </p>
                </div>
                <div className='bnt-areaSave'>
                    
                    <button className='btn-cancelarSalveChamada' type="button" onClick={onClose}>Cancelar</button>
                    <button className='btn-SalvarChamada'>
                        Salvar
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none">
                            <path d="M2.5 20.5V6.5C2.5 5.39543 3.39543 4.5 4.5 4.5H15.6716C16.202 4.5 16.7107 4.71071 17.0858 5.08579L19.9142 7.91421C20.2893 8.28929 20.5 8.79799 20.5 9.32843V20.5C20.5 21.6046 19.6046 22.5 18.5 22.5H4.5C3.39543 22.5 2.5 21.6046 2.5 20.5Z" fill="#D9D9D9" stroke="white" stroke-width="1.5"/>
                            <circle cx="2.5" cy="2.5" r="2.5" transform="matrix(-1 0 0 1 13.5 15.5)" fill="#176FF6"/>
                            <path d="M6.5 7.875V12.5H16.5V7.875C16.5 7.66788 16.2762 7.5 16 7.5H7C6.72386 7.5 6.5 7.66788 6.5 7.875Z" fill="#176FF6" stroke="white" stroke-width="1.5"/>
                        </svg>
                    </button>
                    <button className='btn-salvarEnviar'>
                        Salvar e Enviar
                        <img src={SalvarEnviar} />
                    </button>

                </div>
            </section>
        </div>
    )
}