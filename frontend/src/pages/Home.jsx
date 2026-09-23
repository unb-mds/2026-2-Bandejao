import Cardapio from '../components/Cardapio'
import BotoesCampus from '../components/BotoesCampus'

function Home() {
  return (
    <div style={{ textAlign: 'center', padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Bandejão UnB 🍽️</h1>
      <p>Cardápio e Informações em Tempo Real</p>

      {/* Componente responsável pela seleção de campus */}
      <BotoesCampus />

      {/* Componente do Cardápio */}
      <Cardapio />
    </div>
  )
}

export default Home