# 🐍 Vyper Simple Vault

A secure ETH vault contract written in **Vyper**, demonstrating Pythonic smart contract development.

## What is Vyper?

Vyper is a contract-oriented, pythonic programming language for the Ethereum Virtual Machine (EVM). It emphasizes:
- **Security**: Designed to make it easier to write secure code
- **Simplicity**: Python-like syntax that's easy to audit
- **Auditability**: Readable code that's straightforward to verify

## Features

- 💰 **Deposit ETH**: Secure ETH deposits with min/max limits
- 💸 **Withdraw ETH**: Withdraw deposited funds anytime
- 🔒 **Access Control**: Owner-only administrative functions
- ⚡ **Gas Efficient**: Optimized for low gas consumption
- 🛡️ **Safety Checks**: Built-in overflow protection and assertions
- 📊 **Balance Tracking**: Individual balance tracking per account
- 🚨 **Emergency Functions**: Emergency withdrawal for critical situations

## Contract Details

### Key Functions

#### Public Functions
```python
@external
@payable
def deposit():
    """Deposit ETH into the vault"""

@external
def withdraw(amount: uint256):
    """Withdraw specific amount"""

@external
def withdrawAll():
    """Withdraw all deposited ETH"""
```

#### View Functions
```python
@view
@external
def getBalance(account: address) -> uint256:
    """Get balance of an account"""

@view
@external
def getContractBalance() -> uint256:
    """Get total contract balance"""
```

#### Owner Functions
```python
@external
def setWithdrawalEnabled(enabled: bool):
    """Enable/disable withdrawals"""

@external
def transferOwnership(newOwner: address):
    """Transfer contract ownership"""

@external
def emergencyWithdraw():
    """Emergency withdrawal (owner only)"""
```

## Setup & Installation

### Prerequisites
- Python 3.8+
- ApeWorX Framework

```bash
# Install ApeWorX
pip install eth-ape

# Install plugins
ape plugins install vyper
ape plugins install alchemy
ape plugins install hardhat

# Install project dependencies
ape plugins install .
```

## Compilation

```bash
# Compile the contract
ape compile

# View compiled artifacts
ls .build/
```

## Testing

```bash
# Run all tests
ape test

# Run with verbose output
ape test -v

# Run with gas profiling
ape test --gas

# Run specific test
ape test tests/test_vault.py::test_deposit -v
```

## Deployment

### Local Network

```bash
# Start local node
ape node

# Deploy (in another terminal)
ape run deploy --network ethereum:local:hardhat
```

### Testnet (Sepolia)

```bash
# Set up environment variables
export WEB3_ALCHEMY_PROJECT_ID=your_key
export ACCOUNT_PASSWORD=your_password

# Deploy to Sepolia
ape run deploy --network ethereum:sepolia:alchemy
```

## Usage Examples

### Interact with Deployed Contract

```python
from ape import accounts, project, networks

# Connect to network
with networks.parse_network_choice("ethereum:local:hardhat"):
    # Load account
    account = accounts.load("my_account")

    # Deploy vault
    vault = project.SimpleVault.deploy(sender=account)

    # Deposit ETH
    vault.deposit(value="1 ether", sender=account)

    # Check balance
    balance = vault.getBalance(account.address)
    print(f"Balance: {balance / 10**18} ETH")

    # Withdraw
    vault.withdraw("0.5 ether", sender=account)

    # Withdraw all
    vault.withdrawAll(sender=account)
```

### Script Example

```python
# scripts/deploy.py
from ape import accounts, project

def main():
    account = accounts.load("deployer")
    vault = project.SimpleVault.deploy(sender=account)
    print(f"Vault deployed at: {vault.address}")
    return vault
```

Run with: `ape run deploy --network ethereum:sepolia:alchemy`

## Security Features

### Built-in Safety
- ✅ **Integer Overflow Protection**: Automatic checks
- ✅ **Reentrancy Protection**: Safe external calls
- ✅ **Access Control**: Owner-only functions
- ✅ **Input Validation**: Min/max deposit limits
- ✅ **Zero Address Checks**: Prevents common errors

### Audit Checklist
- [x] No floating pragmas
- [x] Uses safe math operations
- [x] Proper access control
- [x] Event logging for state changes
- [x] Input validation on all functions

## Vyper vs Solidity

| Feature | Vyper | Solidity |
|---------|-------|----------|
| Syntax | Python-like | JavaScript-like |
| Inheritance | ❌ Not supported | ✅ Supported |
| Modifiers | ❌ Not supported | ✅ Supported |
| Operator Overloading | ❌ No | ✅ Yes |
| Infinite Loops | ❌ Not possible | ✅ Possible |
| Readability | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Security Focus | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## Gas Costs (Estimated)

| Operation | Gas Cost |
|-----------|----------|
| Deployment | ~350,000 |
| First Deposit | ~70,000 |
| Subsequent Deposits | ~50,000 |
| Withdraw | ~45,000 |
| Withdraw All | ~47,000 |

## Testing Coverage

```bash
# Generate coverage report
ape test --coverage

# View detailed coverage
coverage report
coverage html
```

## Common Issues & Solutions

### Issue: "vyper not installed"
```bash
pip install vyper
```

### Issue: "No provider for ethereum:local"
```bash
ape plugins install hardhat
```

### Issue: Gas estimation failed
```bash
# Add gas limit manually
vault.deposit(value="1 ether", sender=account, gas_limit=100000)
```

## Why Use Vyper?

1. **Security First**: Designed to minimize attack vectors
2. **Python Syntax**: Familiar for Python developers
3. **Less Complexity**: No inheritance or modifiers reduces bugs
4. **Audit-Friendly**: Easy to read and verify
5. **Growing Ecosystem**: Used by major projects like Curve Finance

## Resources

- [Vyper Documentation](https://docs.vyperlang.org/)
- [ApeWorX Framework](https://docs.apeworx.io/)
- [Vyper by Example](https://vyper.readthedocs.io/en/stable/vyper-by-example.html)
- [Curve Finance (Vyper User)](https://curve.fi/)

## License

MIT License - See LICENSE file for details

## Contributing

Contributions welcome! This is an educational example showcasing Vyper capabilities.
