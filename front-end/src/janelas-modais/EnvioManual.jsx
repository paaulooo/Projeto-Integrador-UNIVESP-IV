import { useEffect, useRef, useState } from "react"
import { MensagensEnviar } from "../elements/MensagensEnviar"
import { enviarMensagemManual } from "../Api"
import "./styles/envioManual.css"

export function EnvioManual({ aluno, faltouHoje = false, onClose }){
    const [mensagemDigitada, setMensagemDigitada] = useState("")
    const [enviando, setEnviando] = useState(false)
    const [erro, setErro] = useState("")
    const [resultado, setResultado] = useState(null)
    const fechamentoTimer = useRef(null)

    useEffect(() => () => {
        if (fechamentoTimer.current) {
            clearTimeout(fechamentoTimer.current)
        }
    }, [])

    const handleEnviar = async () => {
        setEnviando(true)
        setErro("")
        try {
            const resposta = await enviarMensagemManual(aluno.id, mensagemDigitada.trim())
            setResultado(resposta)
            fechamentoTimer.current = setTimeout(onClose, 2000)
           
        } catch (err) {
            const detail = err?.response?.data?.detail
            setErro(detail || err?.message || "Erro ao enviar mensagem.")
        } finally {
            setEnviando(false)
        }
    }

    return(
        <div className="envioManualOverlay" onClick={onClose}>
            <section className="envioManualModal" onClick={(event) => event.stopPropagation()}>
                <div>
                    <svg xmlns="http://www.w3.org/2000/svg" width="72" height="67" viewBox="0 0 72 67" fill="none">
  <rect x="1.5" y="1.5" width="69" height="64" rx="32" stroke="#47765D" stroke-width="3"/>
  <path d="M21 23.0001L32.3667 32.7429C34.3223 34.419 37.0111 34.419 38.9667 32.7429L50.3333 23" stroke="#47765D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M49.2346 19H23.6543C21.6361 19 20 20.8548 20 23.1429V43.8571C20 46.1452 21.6361 48 23.6543 48H49.2346C51.2528 48 52.8889 46.1452 52.8889 43.8571V23.1429C52.8889 20.8548 51.2528 19 49.2346 19Z" stroke="#47765D" stroke-width="3" stroke-linecap="round"/>
</svg>
                    <h3>Enviar mensagem para o responsável</h3>
                    <h5><span>Aluno(a):</span> {aluno?.nome}</h5>
                </div>
                <div className="containerMsg">
                    <h3>Mensagem prévia para o responsável do Aluno:</h3>

                        <MensagensEnviar aluno={aluno} faltouHoje={faltouHoje}/>
                        {mensagemDigitada.trim() ? (
                            <p className="msg-observacao">
                                <strong>Observação do(a) professor(a):</strong>{" "}
                                {mensagemDigitada.trim()}
                            </p>
                        ) : null}

                </div>
                <div className="containerMsgDigitada">
                    <h3>Adicionar Observação:</h3>

                    <label htmlFor="mensagemDigitada">Caso queira enviar alguma mensagem sobre o aluno para seu responsável</label>
                    <textarea
                        id="mensagemDigitada"
                        name="mensagemDigitada"
                        rows="4"
                        cols="50"
                        placeholder="Digite aqui"
                        value={mensagemDigitada}
                        onChange={(event) => setMensagemDigitada(event.target.value)}
                        disabled={enviando}
                    />

                </div>
                {erro ? <p style={{ color: 'red' }}>{erro}</p> : null}
                {resultado ? (
                    <p style={{ color: '#519F76' }}>
                        {[
                            resultado.destinatarios_email?.length ? "email" : null,
                            resultado.destinatarios_whatsapp?.length ? "WhatsApp" : null,
                        ].filter(Boolean).join(" e ") || "mensagem"} enviado(a) com sucesso!
                    </p>
                ) : null}
                <div className="wrapperEnviarMsg">
                    <button className="btn-cancelarEnvio" type="button" onClick={onClose} disabled={enviando}>Cancelar</button>
                    <button className="btn-SalvarEnviarMsg" type="button" onClick={handleEnviar} disabled={enviando}>
                        {enviando ? "Enviando..." : "Salvar e Enviar"}
                        <svg xmlns="http://www.w3.org/2000/svg" width="22" height="19" viewBox="0 0 22 19" fill="none">
                            <path fillRule="evenodd" clipRule="evenodd" d="M0.591964 4.36162C0.291154 4.42647 0.0604737 4.6685 0.0101337 4.97209C-0.0402063 5.27567 0.100014 5.5792 0.363794 5.73768L6.88023 9.65249L13.0999 5.29744C13.4393 5.05986 13.9069 5.14232 14.1445 5.48162C14.3821 5.82093 14.2996 6.28859 13.9603 6.52617L7.74086 10.8811L9.19099 18.3443C9.24969 18.6464 9.48699 18.8819 9.78949 18.9385C10.092 18.995 10.3983 18.861 10.5621 18.6005L21.5374 1.14932C21.6981 0.893877 21.69 0.567037 21.5169 0.319857C21.3438 0.0726666 21.0395 -0.0467133 20.7445 0.0168767L0.591964 4.36162Z" fill="white"/>
                        </svg>
                    </button>
                </div>
            </section>
        </div>
    )
}
