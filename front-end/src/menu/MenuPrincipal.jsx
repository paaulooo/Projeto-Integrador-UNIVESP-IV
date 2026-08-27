import ChapeuPolice from "../assets/chapeu-de-policia.png"
import Notificacoes from "../assets/notificações.svg"
import "./styles/menuPrincipal.css"
export function MenuPrincipal (){
 return(
    <>
        <header>
            <menu className="menu-list">
                <ul className="list-bt">
                    <li>
                        <img src={Notificacoes} alt="Sino de Notificações" />
                    </li>
                    <li className="nomeServidor">
                        <p>Maria de Jesus Santos</p>
                        <svg xmlns="http://www.w3.org/2000/svg" width="9" height="6" viewBox="0 0 9 6" fill="none">
                            <path d="M4.33014 6L8.66027 0H1.19209e-05L4.33014 6Z" fill="#3A4F75"/>
                        </svg>
                    </li>
                    <li>
                        Perfil Professor
                    </li>
                </ul>
                <ul className="bt-police">
                    <li>
                        <img src={ChapeuPolice}/>
                        Acionar Policia
                    </li>
                </ul>
                
            </menu>

        </header>
    </>
 )
}