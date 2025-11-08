# 🦊 Svelte Web3 Wallet

Modern, reactive Web3 wallet interface built with **Svelte** and **Ethers.js**. Demonstrates the power of Svelte's reactivity for blockchain applications.

## 🌟 Features

- 👛 **MetaMask Integration**: Connect/disconnect wallet
- 💰 **Balance Display**: Real-time ETH balance
- 🔄 **Network Detection**: Auto-detect and display network
- 💸 **Send Transactions**: Transfer ETH to any address
- ⚡ **Reactive Updates**: Instant UI updates with Svelte stores
- 🎨 **Beautiful UI**: Modern gradient design

## 🚀 Quick Start

```bash
cd examples/svelte/web3-wallet

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## 📦 Tech Stack

- **Svelte 4**: Reactive UI framework
- **TypeScript**: Type-safe development
- **Ethers.js v6**: Ethereum interactions
- **Vite**: Fast build tool

## 🎯 Key Features

### Svelte Stores for Web3

```typescript
const provider = writable<ethers.BrowserProvider | null>(null);
const account = writable<string>('');
const isConnected = derived(account, ($account) => $account !== '');
```

### Reactive Balance Updates

```svelte
{#if $isConnected}
  <span>{Number($balance).toFixed(4)} ETH</span>
{/if}
```

### Event Handling

```typescript
onMount(() => {
  if (window.ethereum) {
    window.ethereum.on('accountsChanged', handleAccountsChanged);
    window.ethereum.on('chainChanged', () => window.location.reload());
  }
});
```

## 📖 Usage Examples

### Connect Wallet

```typescript
async function connectWallet() {
  const provider = new ethers.BrowserProvider(window.ethereum);
  await provider.send('eth_requestAccounts', []);
  const signer = await provider.getSigner();
  const address = await signer.getAddress();
  account.set(address);
}
```

### Send Transaction

```typescript
async function sendTransaction() {
  const tx = await $signer.sendTransaction({
    to: recipient,
    value: ethers.parseEther(amount),
  });
  await tx.wait();
}
```

## 🔧 Configuration

Update `CONTRACT_ADDRESS` in `App.svelte`:

```typescript
const CONTRACT_ADDRESS = '0xYourContractAddress';
const CONTRACT_ABI = [
  'function balanceOf(address) view returns (uint256)',
  'function transfer(address to, uint256 amount) returns (bool)',
];
```

## 🎨 Customization

### Change Theme Colors

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### Add Custom Chain

```typescript
const chains: Record<number, string> = {
  1: 'Ethereum Mainnet',
  137: 'Polygon',
  42161: 'Arbitrum One', // Add your chain
};
```

## 📊 Project Structure

```
svelte-web3-wallet/
├── src/
│   ├── App.svelte          # Main component
│   ├── main.ts             # App entry point
│   └── vite-env.d.ts       # Type definitions
├── public/
├── package.json
├── vite.config.ts
└── README.md
```

## ⚡ Why Svelte for Web3?

1. **Small Bundle**: Only ~3KB runtime
2. **True Reactivity**: No virtual DOM overhead
3. **Simple Syntax**: Easy to learn and maintain
4. **Fast Performance**: Compiles to vanilla JS
5. **Great DX**: TypeScript, hot reload, etc.

## 📄 License

MIT License
