# 🪙 Cairo ERC-20 Token on StarkNet

A production-ready ERC-20 token implementation in **Cairo 1.0** for StarkNet, showcasing the power of Cairo's native integration with zero-knowledge proofs.

## 🌟 Features

- ✅ Standard ERC-20 functionality (transfer, approve, transferFrom)
- 🔒 Built-in safety with Cairo's type system
- ⚡ Gas-efficient StarkNet deployment
- 🧪 Comprehensive test coverage
- 📊 Event emissions for all state changes

## 🛠️ Prerequisites

```bash
# Install Scarb (Cairo package manager)
curl --proto '=https' --tlsv1.2 -sSf https://docs.swmansion.com/scarb/install.sh | sh

# Install Starkli (CLI tool)
curl https://get.starkli.sh | sh
starkliup

# Verify installation
scarb --version
starkli --version
```

## 🚀 Quick Start

### 1. Build the Contract

```bash
cd examples/cairo/starknet-token
scarb build
```

### 2. Test the Contract

```bash
scarb test
```

### 3. Deploy to Testnet

```bash
# Declare the contract
starkli declare target/dev/token_ERC20Token.sierra.json \
  --network goerli-1

# Deploy the contract
starkli deploy \
  <CLASS_HASH> \
  <NAME> <SYMBOL> <INITIAL_SUPPLY_LOW> <INITIAL_SUPPLY_HIGH> <RECIPIENT> \
  --network goerli-1
```

## 📖 Contract Interface

### Constructor

```cairo
fn constructor(
    name: felt252,
    symbol: felt252,
    initial_supply: u256,
    recipient: ContractAddress
)
```

### Read Functions

```cairo
fn balance_of(account: ContractAddress) -> u256
fn allowance(owner: ContractAddress, spender: ContractAddress) -> u256
fn total_supply() -> u256
```

### Write Functions

```cairo
fn transfer(to: ContractAddress, amount: u256) -> bool
fn approve(spender: ContractAddress, amount: u256) -> bool
fn transfer_from(from: ContractAddress, to: ContractAddress, amount: u256) -> bool
```

## 🧪 Testing

```bash
# Run all tests
scarb test

# Run specific test
scarb test test_transfer

# Test with verbose output
scarb test -v
```

## 📊 Example Usage

### Deploy Token

```bash
# Deploy with 1,000,000 tokens
starkli deploy \
  <CLASS_HASH> \
  0x544f4b454e  # "TOKEN" \
  0x544b4e      # "TKN" \
  1000000000000000000000000 0 \  # 1M * 10^18 (as u256)
  <YOUR_ADDRESS>
```

### Interact with Token

```bash
# Check balance
starkli call \
  <CONTRACT_ADDRESS> \
  balance_of \
  <ACCOUNT_ADDRESS> \
  --network goerli-1

# Transfer tokens
starkli invoke \
  <CONTRACT_ADDRESS> \
  transfer \
  <TO_ADDRESS> \
  1000000000000000000 0 \  # 1 token (as u256)
  --network goerli-1
```

## 🔒 Security Features

1. **Overflow Protection**: Cairo's native u256 type prevents overflows
2. **Reentrancy Safe**: StarkNet's execution model prevents reentrancy
3. **Type Safety**: Strong typing prevents common vulnerabilities
4. **Zero Balance Check**: Automatic validation of sufficient balances

## 📚 Cairo 1.0 Features

- ✨ **Native Type System**: Strong typing with u256, felt252, etc.
- 🧩 **Storage Optimizations**: Efficient LegacyMap usage
- 🎯 **Event System**: Structured events for indexing
- 🔐 **Safety First**: Compile-time checks prevent vulnerabilities

## 🌐 StarkNet Advantages

- **Scalability**: L2 scaling with validity proofs
- **Low Fees**: Significantly cheaper than Ethereum L1
- **Security**: Inherits Ethereum security
- **Cairo**: Purpose-built smart contract language

## 📖 Additional Resources

- [Cairo Book](https://book.cairo-lang.org/)
- [StarkNet Documentation](https://docs.starknet.io/)
- [Cairo by Example](https://cairo-by-example.com/)
- [StarkWare Blog](https://medium.com/starkware)

## 📄 License

MIT License - see LICENSE file for details

---

**Built with ❤️ using Cairo on StarkNet**
