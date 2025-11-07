import { WagmiConfig, createConfig, configureChains, mainnet } from 'wagmi'
import { publicProvider } from 'wagmi/providers/public'
import { InjectedConnector } from 'wagmi/connectors/injected'
import { WalletConnect } from './components/WalletConnect'
import { Balance } from './components/Balance'
import { SendTransaction } from './components/SendTransaction'
import { ContractInteraction } from './components/ContractInteraction'
import './App.css'

const { chains, publicClient, webSocketPublicClient } = configureChains(
  [mainnet],
  [publicProvider()],
)

const config = createConfig({
  autoConnect: true,
  connectors: [
    new InjectedConnector({
      chains,
      options: {
        name: 'MetaMask',
        shimDisconnect: true,
      },
    }),
  ],
  publicClient,
  webSocketPublicClient,
})

function App() {
  return (
    <WagmiConfig config={config}>
      <div className="app">
        <header className="app-header">
          <h1>⚡ Wagmi DApp Example</h1>
          <p>Web3 React Application with TypeScript</p>
        </header>

        <main className="app-main">
          <WalletConnect />

          <div className="features">
            <Balance />
            <SendTransaction />
            <ContractInteraction />
          </div>
        </main>

        <footer className="app-footer">
          <p>Built with Wagmi + TypeScript + React</p>
        </footer>
      </div>
    </WagmiConfig>
  )
}

export default App
