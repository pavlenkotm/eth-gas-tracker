<template>
  <div id="app" class="container">
    <h1>🌐 Vue Web3 Dashboard</h1>

    <div v-if="!connected" class="card">
      <h2>Connect Wallet</h2>
      <button @click="connectWallet" :disabled="loading">
        {{ loading ? 'Connecting...' : 'Connect MetaMask' }}
      </button>
    </div>

    <div v-else>
      <div class="card">
        <h2>✅ Connected</h2>
        <div class="info">
          <div><strong>Address:</strong> {{ formatAddress(account) }}</div>
          <div><strong>Balance:</strong> {{ balance }} ETH</div>
          <div><strong>Network:</strong> {{ networkName }}</div>
        </div>
        <button @click="disconnect" class="btn-secondary">Disconnect</button>
      </div>

      <div class="card">
        <h2>💸 Send ETH</h2>
        <input v-model="recipient" placeholder="Recipient address" />
        <input v-model="amount" type="number" step="0.001" placeholder="Amount" />
        <button @click="sendTransaction" :disabled="loading || !recipient || !amount">
          {{ loading ? 'Sending...' : 'Send' }}
        </button>
      </div>
    </div>

    <div v-if="error" class="error">⚠️ {{ error }}</div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import { ethers } from 'ethers';

export default {
  name: 'App',
  setup() {
    const provider = ref(null);
    const signer = ref(null);
    const account = ref('');
    const balance = ref('0');
    const chainId = ref(0);
    const recipient = ref('');
    const amount = ref('');
    const loading = ref(false);
    const error = ref('');

    const connected = computed(() => account.value !== '');
    const networkName = computed(() => {
      const names = {1: 'Mainnet', 5: 'Goerli', 137: 'Polygon'};
      return names[chainId.value] || `Chain ${chainId.value}`;
    });

    const connectWallet = async () => {
      loading.value = true;
      error.value = '';

      try {
        if (!window.ethereum) throw new Error('Install MetaMask!');

        const web3Provider = new ethers.BrowserProvider(window.ethereum);
        await web3Provider.send('eth_requestAccounts', []);

        const web3Signer = await web3Provider.getSigner();
        const address = await web3Signer.getAddress();
        const bal = await web3Provider.getBalance(address);
        const network = await web3Provider.getNetwork();

        provider.value = web3Provider;
        signer.value = web3Signer;
        account.value = address;
        balance.value = ethers.formatEther(bal);
        chainId.value = Number(network.chainId);
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    };

    const disconnect = () => {
      provider.value = null;
      signer.value = null;
      account.value = '';
      balance.value = '0';
    };

    const sendTransaction = async () => {
      loading.value = true;
      error.value = '';

      try {
        const tx = await signer.value.sendTransaction({
          to: recipient.value,
          value: ethers.parseEther(amount.value),
        });
        await tx.wait();
        alert('Transaction successful!');

        const bal = await provider.value.getBalance(account.value);
        balance.value = ethers.formatEther(bal);
        recipient.value = '';
        amount.value = '';
      } catch (err) {
        error.value = err.message;
      } finally {
        loading.value = false;
      }
    };

    const formatAddress = (addr) =>
      `${addr.substring(0, 6)}...${addr.substring(38)}`;

    return {
      connected,
      account,
      balance,
      networkName,
      recipient,
      amount,
      loading,
      error,
      connectWallet,
      disconnect,
      sendTransaction,
      formatAddress,
    };
  },
};
</script>

<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); min-height: 100vh; }
.container { max-width: 600px; margin: 0 auto; padding: 2rem; }
h1 { color: white; text-align: center; margin-bottom: 2rem; }
.card { background: white; border-radius: 1rem; padding: 2rem; margin-bottom: 1.5rem; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }
button { width: 100%; padding: 1rem; font-size: 1rem; font-weight: 600; color: white; background: linear-gradient(135deg, #667eea, #764ba2); border: none; border-radius: 0.5rem; cursor: pointer; }
button:hover:not(:disabled) { transform: translateY(-2px); }
button:disabled { opacity: 0.6; cursor: not-allowed; }
input { width: 100%; padding: 0.75rem; margin-bottom: 1rem; border: 2px solid #eee; border-radius: 0.5rem; }
.info div { padding: 0.5rem 0; border-bottom: 1px solid #eee; }
.error { background: #fee; color: #c33; padding: 1rem; border-radius: 0.5rem; margin-top: 1rem; }
</style>
