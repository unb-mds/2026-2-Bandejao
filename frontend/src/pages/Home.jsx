import Cardapio from '../components/Cardapio'

function Home() {
  return (
    <div style={{ textAlign: 'center', padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Bandejão UnB 🍽️</h1>
      <p>Cardápio e Informações em Tempo Real</p>

      <div style={{ margin: '20px 0' }}>
        <button style={{ margin: '5px', padding: '10px 15px' }}>Darcy Ribeiro</button>
        <button style={{ margin: '5px', padding: '10px 15px' }}>Gama</button>
        <button style={{ margin: '5px', padding: '10px 15px' }}>Ceilândia</button>
        <button style={{ margin: '5px', padding: '10px 15px' }}>Planaltina</button>
      </div>

      {/* Aqui chamamos o nosso componente do Cardápio */}
      <Cardapio />
    </div>
  )
}

export default Home
