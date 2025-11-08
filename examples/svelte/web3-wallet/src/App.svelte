<script lang="ts">
  import { onMount } from 'svelte';
  import { writable, derived } from 'svelte/store';
  import { ethers } from 'ethers';

  // Stores
  const provider = writable<ethers.BrowserProvider | null>(null);
  const signer = writable<ethers.JsonRpcSigner | null>(null);
  const account = writable<string>('');
  const balance = writable<string>('0');
  const chainId = writable<number>(0);
  const isConnected = derived(account, ($account) => $account !== '');

  // Contract interface
  const CONTRACT_ADDRESS = '0x...';
  const CONTRACT_ABI = [
    'function balanceOf(address) view returns (uint256)',
    'function transfer(address to, uint256 amount) returns (bool)',
  ];

  let recipient = '';
  let amount = '';
  let loading = false;
  let error = '';

  onMount(() => {
    checkConnection();

    if (window.ethereum) {
      window.ethereum.on('accountsChanged', handleAccountsChanged);
      window.ethereum.on('chainChanged', () => window.location.reload());
    }
  });

  async function checkConnection() {
    if (window.ethereum) {
      const web3Provider = new ethers.BrowserProvider(window.ethereum);
      provider.set(web3Provider);

      try {
        const accounts = await web3Provider.listAccounts();
        if (accounts.length > 0) {
          await connectWallet();
        }
      } catch (err) {
        console.error('Error checking connection:', err);
      }
    }
  }

  async function connectWallet() {
    loading = true;
    error = '';

    try {
      if (!window.ethereum) {
        throw new Error('Please install MetaMask!');
      }

      const web3Provider = new ethers.BrowserProvider(window.ethereum);
      await web3Provider.send('eth_requestAccounts', []);

      const web3Signer = await web3Provider.getSigner();
      const address = await web3Signer.getAddress();
      const bal = await web3Provider.getBalance(address);
      const network = await web3Provider.getNetwork();

      provider.set(web3Provider);
      signer.set(web3Signer);
      account.set(address);
      balance.set(ethers.formatEther(bal));
      chainId.set(Number(network.chainId));
    } catch (err: any) {
      error = err.message;
    } finally {
      loading = false;
    }
  }

  async function disconnectWallet() {
    provider.set(null);
    signer.set(null);
    account.set('');
    balance.set('0');
    chainId.set(0);
  }

  async function handleAccountsChanged(accounts: string[]) {
    if (accounts.length === 0) {
      disconnectWallet();
    } else {
      connectWallet();
    }
  }

  async function sendTransaction() {
    if (!$signer || !recipient || !amount) return;

    loading = true;
    error = '';

    try {
      const tx = await $signer.sendTransaction({
        to: recipient,
        value: ethers.parseEther(amount),
      });

      await tx.wait();
      alert('Transaction successful!');

      // Refresh balance
      const address = await $signer.getAddress();
      const bal = await $provider!.getBalance(address);
      balance.set(ethers.formatEther(bal));

      recipient = '';
      amount = '';
    } catch (err: any) {
      error = err.message;
    } finally {
      loading = false;
    }
  }

  function formatAddress(addr: string): string {
    return `${addr.substring(0, 6)}...${addr.substring(38)}`;
  }

  function getChainName(id: number): string {
    const chains: Record<number, string> = {
      1: 'Ethereum Mainnet',
      5: 'Goerli Testnet',
      137: 'Polygon',
      80001: 'Mumbai Testnet',
    };
    return chains[id] || `Chain ${id}`;
  }
</script>

<main class="container">
  <h1>🦊 Svelte Web3 Wallet</h1>

  {#if !$isConnected}
    <div class="card">
      <h2>Connect Your Wallet</h2>
      <p>Connect MetaMask to interact with Ethereum</p>
      <button on:click={connectWallet} disabled={loading}>
        {loading ? 'Connecting...' : 'Connect MetaMask'}
      </button>
    </div>
  {:else}
    <div class="card">
      <h2>✅ Connected</h2>

      <div class="info">
        <div class="info-row">
          <span class="label">Address:</span>
          <span class="value">{formatAddress($account)}</span>
        </div>
        <div class="info-row">
          <span class="label">Balance:</span>
          <span class="value">{Number($balance).toFixed(4)} ETH</span>
        </div>
        <div class="info-row">
          <span class="label">Network:</span>
          <span class="value">{getChainName($chainId)}</span>
        </div>
      </div>

      <button on:click={disconnectWallet} class="btn-secondary">
        Disconnect
      </button>
    </div>

    <div class="card">
      <h2>💸 Send Transaction</h2>

      <div class="form">
        <input
          type="text"
          placeholder="Recipient address (0x...)"
          bind:value={recipient}
        />
        <input
          type="number"
          placeholder="Amount (ETH)"
          bind:value={amount}
          step="0.001"
        />
        <button on:click={sendTransaction} disabled={loading || !recipient || !amount}>
          {loading ? 'Sending...' : 'Send ETH'}
        </button>
      </div>
    </div>
  {/if}

  {#if error}
    <div class="error">
      ⚠️ {error}
    </div>
  {/if}
</main>

<style>
  :global(body) {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
  }

  .container {
    max-width: 600px;
    margin: 0 auto;
    padding: 2rem;
  }

  h1 {
    text-align: center;
    color: white;
    font-size: 2.5rem;
    margin-bottom: 2rem;
  }

  .card {
    background: white;
    border-radius: 1rem;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  }

  h2 {
    margin-top: 0;
    color: #333;
  }

  .info {
    margin: 1.5rem 0;
  }

  .info-row {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid #eee;
  }

  .label {
    font-weight: 600;
    color: #666;
  }

  .value {
    color: #333;
    font-family: 'Courier New', monospace;
  }

  button {
    width: 100%;
    padding: 1rem;
    font-size: 1rem;
    font-weight: 600;
    color: white;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border: none;
    border-radius: 0.5rem;
    cursor: pointer;
    transition: transform 0.2s;
  }

  button:hover:not(:disabled) {
    transform: translateY(-2px);
  }

  button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .btn-secondary {
    background: #6c757d;
  }

  .form input {
    width: 100%;
    padding: 0.75rem;
    margin-bottom: 1rem;
    border: 2px solid #eee;
    border-radius: 0.5rem;
    font-size: 1rem;
    box-sizing: border-box;
  }

  .form input:focus {
    outline: none;
    border-color: #667eea;
  }

  .error {
    background: #fee;
    color: #c33;
    padding: 1rem;
    border-radius: 0.5rem;
    margin-top: 1rem;
  }
</style>
