import "./styles/listaAluno.css"
import {EnvioManual} from "../janelas-modais/EnvioManual"

export function ListaAluno({alunos}){
    if (!alunos) return null;
    return(
        <>
            <ul className="listaAluno">
                <li className="sequeciaNumericaChamada">
                    1
                </li>
                <li className="nomeAluno">
                    {alunos.nome}
                    <div className="wrapper-ativoN-falta">
                        <span className="alunoAtivoouNao"><svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" viewBox="0 0 8 8" fill="none">
  <circle cx="4" cy="4" r="4" fill="#2FC06D"/>
</svg></span>
                        <span className="faltasAluno"><svg xmlns="http://www.w3.org/2000/svg" width="8" height="8" viewBox="0 0 8 8" fill="none">
  <circle cx="4" cy="4" r="4" fill="#3A4F75"/>
</svg>Faltas: </span>
                    </div>
                </li>
                <li className="presenca">

                </li>
                <li className="mensagem" to="">
                    <svg xmlns="http://www.w3.org/2000/svg" width="35" height="29" viewBox="0 0 35 29" fill="none">
  <path d="M8.36951 8.3948L15.4456 13.8023C16.663 14.7326 18.3369 14.7326 19.5543 13.8023L26.6304 8.39474" stroke="#3A4F75" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M25.8695 6.10526H9.89125C8.6306 6.10526 7.60864 7.13029 7.60864 8.39473V19.8421C7.60864 21.1065 8.6306 22.1316 9.89125 22.1316H25.8695C27.1302 22.1316 28.1521 21.1065 28.1521 19.8421V8.39473C28.1521 7.13029 27.1302 6.10526 25.8695 6.10526Z" stroke="#3A4F75" stroke-width="2" stroke-linecap="round"/>
</svg>
                </li>
            </ul>


            
        </>
    )
}