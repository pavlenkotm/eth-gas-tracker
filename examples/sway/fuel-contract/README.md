# ⛽ Sway Token Contract on Fuel

A high-performance token contract written in **Sway** for the **Fuel Network**, demonstrating the power of Rust-inspired smart contract development with native optimistic rollup features.

## 🌟 Features

- 🚀 **Ultra-Fast Execution**: Fuel's UTXO model for parallel execution
- 💎 **Token Operations**: Mint, burn, transfer with owner controls
- 🔒 **Access Control**: Owner-only minting functionality
- ⚡ **Gas Efficient**: Optimized storage and execution
- 📊 **Event Logging**: Comprehensive event emissions
- 🧪 **Type Safe**: Sway's strong type system

## 🛠️ Prerequisites

```bash
# Install fuelup (Fuel toolchain manager)
curl https://install.fuel.network | sh

# Install Fuel toolchain
fuelup toolchain install latest
fuelup default latest

# Verify installation
forc --version
fuel-core --version
```

## 🚀 Quick Start

### 1. Build the Contract

```bash
cd examples/sway/fuel-contract
forc build
```

### 2. Run Tests

```bash
forc test
```

### 3. Deploy to Testnet

```bash
# Start local Fuel node
fuel-core run --db-type in-memory

# Deploy contract
forc deploy --testnet
```

## 📖 Contract Interface

### Initialize

```sway
fn initialize(initial_supply: u64, owner: Identity)
```

Creates the token with initial supply and sets the owner.

### Token Operations

```sway
// Transfer tokens
fn transfer_tokens(amount: u64, recipient: Identity)

// Mint new tokens (owner only)
fn mint_tokens(amount: u64, recipient: Identity)

// Burn tokens
fn burn_tokens(amount: u64)
```

### Query Functions

```sway
fn get_balance(target: Identity) -> u64
fn get_total_supply() -> u64
```

## 🧪 Testing

Create a test file `tests/harness.rs`:

```rust
use fuels::{prelude::*, types::Identity};

#[tokio::test]
async fn test_transfer() {
    let wallet = launch_provider_and_get_wallet().await;
    let id = Contract::deploy(
        "./out/debug/fuel-token-contract.bin",
        &wallet,
        TxParameters::default(),
        StorageConfiguration::default(),
    )
    .await
    .unwrap();

    let instance = TokenContract::new(id, wallet);

    // Initialize
    let owner = Identity::Address(wallet.address().into());
    instance
        .methods()
        .initialize(1000000, owner)
        .call()
        .await
        .unwrap();

    // Test transfer
    let recipient = Identity::Address(Address::zeroed());
    instance
        .methods()
        .transfer_tokens(100, recipient)
        .call()
        .await
        .unwrap();

    let balance = instance
        .methods()
        .get_balance(recipient)
        .call()
        .await
        .unwrap();

    assert_eq!(balance.value, 100);
}
```

Run tests:

```bash
cargo test
```

## 📊 Example Usage

### Using Fuel SDK (TypeScript)

```typescript
import { Provider, Wallet } from 'fuels';
import { TokenContract } from './types/TokenContract';

// Connect to Fuel testnet
const provider = await Provider.create('https://testnet.fuel.network/graphql');
const wallet = Wallet.fromPrivateKey('your-private-key', provider);

// Load contract
const contractId = 'your-contract-id';
const contract = new TokenContract(contractId, wallet);

// Initialize token
await contract.functions
  .initialize(1000000, { Address: { value: wallet.address.toB256() } })
  .call();

// Transfer tokens
await contract.functions
  .transfer_tokens(100, {
    Address: { value: recipientAddress },
  })
  .call();

// Check balance
const { value } = await contract.functions
  .get_balance({ Address: { value: wallet.address.toB256() } })
  .get();

console.log('Balance:', value);
```

### Using Rust SDK

```rust
use fuels::prelude::*;

#[tokio::main]
async fn main() -> Result<()> {
    let wallet = WalletUnlocked::new_random(None);
    let provider = Provider::connect("testnet.fuel.network").await?;

    let contract_id = Bech32ContractId::from_str("fuel1...")?;
    let contract = TokenContract::new(contract_id, wallet);

    // Initialize
    let owner = Identity::Address(wallet.address().into());
    contract
        .methods()
        .initialize(1_000_000, owner)
        .call()
        .await?;

    // Transfer
    let recipient = Identity::Address(Address::zeroed());
    contract
        .methods()
        .transfer_tokens(100, recipient)
        .call()
        .await?;

    Ok(())
}
```

## 🔒 Security Features

1. **Initialization Check**: Prevents re-initialization
2. **Balance Verification**: Ensures sufficient funds before transfer
3. **Owner Authorization**: Minting restricted to owner
4. **Overflow Protection**: u64 with safe arithmetic
5. **Identity System**: Type-safe address handling

## ⚡ Fuel Network Advantages

- **Parallel Execution**: UTXO model enables concurrent transactions
- **Low Fees**: Optimistic rollup with fraud proofs
- **High Throughput**: Orders of magnitude faster than Ethereum
- **Developer Experience**: Rust-like syntax with Sway
- **Fraud Proofs**: Security inherited from Ethereum

## 🎯 Sway Language Features

- 🦀 **Rust-Inspired**: Familiar syntax for Rust developers
- 🔐 **Memory Safe**: No null pointers or buffer overflows
- ⚡ **Performance**: Compiled to optimized FuelVM bytecode
- 📦 **Module System**: Clean code organization
- 🧩 **Type System**: Strong typing prevents errors

## 📚 Additional Resources

- [Sway Book](https://fuellabs.github.io/sway/)
- [Fuel Documentation](https://docs.fuel.network/)
- [Fuel Forum](https://forum.fuel.network/)
- [Fuel GitHub](https://github.com/FuelLabs)

## 🛣️ Roadmap

- [ ] Add allowance mechanism
- [ ] Implement ERC-20 compatibility
- [ ] Add pausable functionality
- [ ] Create governance features
- [ ] Build SDK examples

## 📄 License

MIT License - see LICENSE file for details

---

**Built with ⛽ using Sway on Fuel Network**
