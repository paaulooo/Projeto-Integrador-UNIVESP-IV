import { useState } from 'react'
import  {MenuPrincipal}  from './menu/MenuPrincipal'
import  {MenuLateral}  from './menu/MenuLateral'
import {AreaFrequencia} from './elements/AreaFrequencia'
import Aviso from "./assets/Aviso.svg"
function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <section>
        <MenuPrincipal/>
        <div>
          <MenuLateral/>
          <div>
            <span>
              <img src={Aviso}/>
              Aviso!
            </span>
            <p>
              O prazo ara lançamento de frequência para o seu perfil, será de até 8 dias corridos
            </p>
          </div>
          <AreaFrequencia/>
        </div>
      </section>

    </>
  )
}

export default App
