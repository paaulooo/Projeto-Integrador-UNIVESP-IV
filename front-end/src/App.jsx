import { useState } from 'react'
import  {MenuPrincipal}  from './menu/MenuPrincipal'
import  {MenuLateral}  from './menu/MenuLateral'
import {AreaFrequencia} from './elements/AreaFrequencia'
import { Footer } from './elements/Footer'
import Aviso from "./assets/Aviso.svg"
import "./app.css"

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <section>
        <MenuPrincipal/>
        <div className='wrapperAreaFrequencia'>
          <MenuLateral/>
          <div className='wrapperFrequencia'>
            <div className='wapperAviso'>

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
        </div>
      </section>
      <Footer />
    </>
  )
}

export default App
