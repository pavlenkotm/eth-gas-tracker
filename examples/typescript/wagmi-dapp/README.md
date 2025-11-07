# ⚡ Wagmi DApp - TypeScript Web3 Frontend

Modern **Web3 DApp** built with **Wagmi**, **React**, and **TypeScript** for Ethereum interaction.

## What is Wagmi?

Wagmi is a collection of React Hooks for Ethereum, providing:
- 🪝 **React Hooks**: Easy wallet connection, transactions, and contract calls
- 🔌 **Multiple Wallets**: MetaMask, WalletConnect, Coinbase Wallet, etc.
- ⚡ **Optimized**: Automatic request deduplication and caching
- 🛡️ **Type-safe**: Full TypeScript support with viem
- 🧪 **Well-tested**: Comprehensive test coverage

## Features

- 👛 **Wallet Connection**: Connect with MetaMask and other wallets
- 💰 **Balance Display**: View ETH and token balances
- 💸 **Send Transactions**: Transfer ETH to other addresses
- 📜 **Smart Contracts**: Read from and write to contracts
- 🎨 **ENS Support**: Display ENS names
- ⚡ **Real-time Updates**: Auto-refresh on chain changes
- 🎯 **Type Safety**: Full TypeScript support

## Tech Stack

- **Wagmi**: React Hooks for Ethereum
- **Viem**: TypeScript Ethereum library
- **React 18**: Modern React with hooks
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool and dev server

## Project Structure

```
wagmi-dapp/
├── src/
│   ├── components/
│   │   ├── WalletConnect.tsx    # Wallet connection
│   │   ├── Balance.tsx          # Balance display
│   │   ├── SendTransaction.tsx  # Send ETH
│   │   └── ContractInteraction.tsx # Contract calls
│   ├── App.tsx                  # Main app component
│   ├── App.css                  # Styles
│   └── main.tsx                 # Entry point
├── package.json
├── tsconfig.json
└── vite.config.ts
```

## Setup & Installation

```bash
# Install dependencies
npm install
# or
yarn install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Usage

### 1. Connect Wallet

```typescript
import { useConnect, useAccount } from 'wagmi'

function ConnectButton() {
  const { connect, connectors } = useConnect()
  const { isConnected } = useAccount()

  return (
    <>
      {connectors.map((connector) => (
        <button key={connector.id} onClick={() => connect({ connector })}>
          Connect {connector.name}
        </button>
      ))}
    </>
  )
}
```

### 2. Get Balance

```typescript
import { useAccount, useBalance } from 'wagmi'

function Balance() {
  const { address } = useAccount()
  const { data, isLoading } = useBalance({
    address,
  })

  if (isLoading) return <div>Loading...</div>

  return (
    <div>
      Balance: {data?.formatted} {data?.symbol}
    </div>
  )
}
```

### 3. Send Transaction

```typescript
import { useSendTransaction, usePrepareSendTransaction } from 'wagmi'
import { parseEther } from 'viem'

function SendETH() {
  const { config } = usePrepareSendTransaction({
    to: '0x...',
    value: parseEther('0.01'),
  })

  const { sendTransaction } = useSendTransaction(config)

  return (
    <button onClick={() => sendTransaction?.()}>
      Send Transaction
    </button>
  )
}
```

### 4. Read from Contract

```typescript
import { useContractRead } from 'wagmi'

const contractAddress = '0x...'
const abi = [/* ... */]

function ReadContract() {
  const { data, isLoading } = useContractRead({
    address: contractAddress,
    abi: abi,
    functionName: 'balanceOf',
    args: ['0x...'],
  })

  return <div>Balance: {data?.toString()}</div>
}
```

### 5. Write to Contract

```typescript
import { useContractWrite, usePrepareContractWrite } from 'wagmi'

function WriteContract() {
  const { config } = usePrepareContractWrite({
    address: '0x...',
    abi: abi,
    functionName: 'transfer',
    args: ['0x...', 1000n],
  })

  const { write } = useContractWrite(config)

  return (
    <button onClick={() => write?.()}>
      Transfer Tokens
    </button>
  )
}
```

## Configuration

### Wagmi Config

```typescript
import { createConfig, configureChains, mainnet } from 'wagmi'
import { publicProvider } from 'wagmi/providers/public'
import { InjectedConnector } from 'wagmi/connectors/injected'

const { chains, publicClient } = configureChains(
  [mainnet],
  [publicProvider()],
)

const config = createConfig({
  autoConnect: true,
  connectors: [
    new InjectedConnector({ chains }),
  ],
  publicClient,
})
```

### Multiple Networks

```typescript
import { mainnet, polygon, arbitrum } from 'wagmi/chains'

const { chains, publicClient } = configureChains(
  [mainnet, polygon, arbitrum],
  [publicProvider()],
)
```

### With Alchemy Provider

```typescript
import { alchemyProvider } from 'wagmi/providers/alchemy'

const { chains, publicClient } = configureChains(
  [mainnet],
  [alchemyProvider({ apiKey: 'your-api-key' })],
)
```

## Common Hooks

| Hook | Purpose |
|------|---------|
| `useAccount` | Get connected account info |
| `useBalance` | Get account balance |
| `useConnect` | Connect wallet |
| `useDisconnect` | Disconnect wallet |
| `useNetwork` | Get current network |
| `useSwitchNetwork` | Switch networks |
| `useContractRead` | Read from contract |
| `useContractWrite` | Write to contract |
| `useSendTransaction` | Send ETH |
| `useWaitForTransaction` | Wait for tx confirmation |
| `useEnsName` | Get ENS name |
| `useEnsAvatar` | Get ENS avatar |

## Development

### Type Checking

```bash
npm run type-check
```

### Linting

```bash
npm run lint
```

### Testing

```bash
npm test
```

## Environment Variables

Create `.env` file:

```env
VITE_ALCHEMY_ID=your_alchemy_api_key
VITE_WALLETCONNECT_PROJECT_ID=your_project_id
```

## Best Practices

### 1. Handle Loading States

```typescript
if (isLoading) return <div>Loading...</div>
if (error) return <div>Error: {error.message}</div>
```

### 2. Prepare Transactions

```typescript
// Always prepare before sending
const { config } = usePrepareSendTransaction({...})
const { sendTransaction } = useSendTransaction(config)
```

### 3. Wait for Confirmations

```typescript
const { data: txData, sendTransaction } = useSendTransaction()

const { isLoading, isSuccess } = useWaitForTransaction({
  hash: txData?.hash,
})
```

### 4. Error Handling

```typescript
const { write, error } = useContractWrite({...})

if (error) {
  console.error('Transaction failed:', error)
}
```

## Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Vercel

```bash
npm i -g vercel
vercel
```

### Deploy to Netlify

```bash
npm run build
# Upload dist/ folder to Netlify
```

## Wagmi vs Ethers.js

| Feature | Wagmi | Ethers.js |
|---------|-------|-----------|
| **React Integration** | Built-in hooks | Manual setup |
| **TypeScript** | First-class | Good support |
| **Caching** | Automatic | Manual |
| **Wallet Support** | Multiple connectors | Manual setup |
| **Learning Curve** | Easy | Moderate |
| **Bundle Size** | Optimized | Larger |

## Troubleshooting

### MetaMask Not Detected

```typescript
if (!window.ethereum) {
  alert('Please install MetaMask!')
}
```

### Wrong Network

```typescript
const { chain } = useNetwork()
const { switchNetwork } = useSwitchNetwork()

if (chain?.id !== 1) {
  switchNetwork?.(1) // Switch to mainnet
}
```

## Resources

- [Wagmi Documentation](https://wagmi.sh/)
- [Viem Documentation](https://viem.sh/)
- [Wagmi Examples](https://wagmi.sh/examples)
- [React Docs](https://react.dev/)

## License

MIT License - See LICENSE file for details
