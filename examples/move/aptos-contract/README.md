# 💎 Move Simple Coin (Aptos)

A professional **fungible token** implementation in **Move** for the **Aptos blockchain**.

## What is Move?

Move is a smart contract language developed by Meta (Facebook) for the Diem project, now used by:
- **Aptos**: High-performance Layer 1 blockchain
- **Sui**: Parallel execution blockchain
- **0L Network**: Community-driven blockchain

### Move Advantages
- ✅ **Resource-oriented**: Assets are first-class citizens
- ✅ **Safe by design**: No reentrancy, no integer overflow
- ✅ **Formal verification**: Mathematical proofs of correctness
- ✅ **Linear types**: Resources can't be copied or dropped

## Features

- 🪙 **Fungible Token**: Standard coin implementation
- 👑 **Owner Control**: Mint and burn capabilities
- 💸 **Transfers**: Send tokens between accounts
- 📊 **Supply Tracking**: Monitor total supply
- 🔒 **Security**: Move's built-in safety features
- ✅ **Testing**: Comprehensive Move test suite

## Contract Structure

```
simple_coin/
├── sources/
│   └── simple_coin.move     # Main coin module
├── tests/
│   └── coin_tests.move      # Test suite
└── Move.toml                # Package configuration
```

## Public Functions

### Entry Functions (Transactions)

```move
/// Initialize the coin
public entry fun initialize(
    owner: &signer,
    name: vector<u8>,
    symbol: vector<u8>,
    decimals: u8,
)

/// Mint new coins (owner only)
public entry fun mint(
    owner: &signer,
    recipient: address,
    amount: u64,
)

/// Burn coins from sender's account
public entry fun burn(
    owner: &signer,
    amount: u64,
)

/// Transfer coins
public entry fun transfer(
    sender: &signer,
    recipient: address,
    amount: u64,
)

/// Register to receive coins
public entry fun register(account: &signer)
```

### View Functions (Read-only)

```move
#[view]
public fun balance_of(account: address): u64

#[view]
public fun total_supply(): u128

#[view]
public fun is_registered(account: address): bool
```

## Prerequisites

### Install Aptos CLI

```bash
curl -fsSL "https://aptos.dev/scripts/install_cli.py" | python3
```

### Create Aptos Account

```bash
aptos init
```

## Build & Test

### Compile the Module

```bash
aptos move compile
```

### Run Tests

```bash
# Run all tests
aptos move test

# Run with coverage
aptos move test --coverage

# Run specific test
aptos move test --filter test_mint_and_balance
```

### Publish to Devnet

```bash
# Publish module
aptos move publish --named-addresses simple_coin=default

# Or specify account
aptos move publish --named-addresses simple_coin=0xYourAddress
```

## Usage Examples

### Initialize Coin

```bash
aptos move run \
  --function-id 'default::coin::initialize' \
  --args string:"Simple Coin" string:"SMPL" u8:8
```

### Mint Tokens

```bash
aptos move run \
  --function-id 'default::coin::mint' \
  --args address:0x123 u64:1000000
```

### Transfer Tokens

```bash
aptos move run \
  --function-id 'default::coin::transfer' \
  --args address:0x456 u64:500
```

### Check Balance

```bash
aptos move view \
  --function-id 'default::coin::balance_of' \
  --args address:0x123
```

## TypeScript Integration

```typescript
import { AptosClient, AptosAccount, FaucetClient } from "aptos";

const NODE_URL = "https://fullnode.devnet.aptoslabs.com";
const client = new AptosClient(NODE_URL);

// Initialize coin
async function initializeCoin(owner: AptosAccount) {
  const payload = {
    type: "entry_function_payload",
    function: `${owner.address()}::coin::initialize`,
    type_arguments: [],
    arguments: ["Simple Coin", "SMPL", 8],
  };

  const txn = await client.generateTransaction(owner.address(), payload);
  const signedTxn = await client.signTransaction(owner, txn);
  const result = await client.submitTransaction(signedTxn);
  await client.waitForTransaction(result.hash);
}

// Mint coins
async function mint(owner: AptosAccount, recipient: string, amount: number) {
  const payload = {
    type: "entry_function_payload",
    function: `${owner.address()}::coin::mint`,
    type_arguments: [],
    arguments: [recipient, amount],
  };

  const txn = await client.generateTransaction(owner.address(), payload);
  const signedTxn = await client.signTransaction(owner, txn);
  const result = await client.submitTransaction(signedTxn);
  await client.waitForTransaction(result.hash);
}

// Get balance
async function getBalance(owner: string, account: string): Promise<number> {
  const payload = {
    function: `${owner}::coin::balance_of`,
    type_arguments: [],
    arguments: [account],
  };

  const balance = await client.view(payload);
  return balance[0] as number;
}
```

## Security Features

### Move's Built-in Safety

1. **Resource Safety**
   - Resources (like coins) can't be copied
   - Must be explicitly moved or destroyed
   - Prevents double-spending at language level

2. **No Reentrancy**
   - Move doesn't support callbacks
   - No reentrancy vulnerabilities by design

3. **Overflow Protection**
   - All arithmetic is checked
   - Automatic overflow/underflow prevention

4. **Type Safety**
   - Strong static typing
   - Generic type parameters with constraints

### Access Control

```move
assert!(caps.owner == owner_addr, E_NOT_OWNER);
```

## Gas Costs (Devnet/Mainnet)

| Operation | Approximate Gas |
|-----------|----------------|
| Initialize | ~2,000 gas units |
| Mint | ~500 gas units |
| Transfer | ~300 gas units |
| Burn | ~400 gas units |
| Register | ~150 gas units |

*Note: 1 APT = 100,000,000 Octas (8 decimals)*

## Testing Output

```bash
Running Move unit tests
[ PASS    ] 0xcafe::coin_tests::test_burn
[ PASS    ] 0xcafe::coin_tests::test_initialize
[ PASS    ] 0xcafe::coin_tests::test_mint_and_balance
[ PASS    ] 0xcafe::coin_tests::test_total_supply
[ PASS    ] 0xcafe::coin_tests::test_transfer
Test result: OK. Total tests: 5; passed: 5; failed: 0
```

## Move vs Solidity

| Feature | Move | Solidity |
|---------|------|----------|
| **Safety** | Resources prevent copying | Manual checks needed |
| **Reentrancy** | Impossible by design | Requires guards |
| **Overflow** | Built-in protection | Need SafeMath (pre-0.8.0) |
| **Gas Model** | More predictable | Can be complex |
| **Learning Curve** | Moderate | Moderate-High |
| **Ecosystem** | Growing (Aptos, Sui) | Mature (Ethereum) |

## Common Commands

```bash
# Initialize Aptos account
aptos init

# Get account info
aptos account list

# Fund account (devnet)
aptos account fund-with-faucet --account default

# Compile
aptos move compile

# Test
aptos move test

# Publish
aptos move publish

# Run function
aptos move run --function-id ADDRESS::MODULE::FUNCTION

# View function
aptos move view --function-id ADDRESS::MODULE::FUNCTION
```

## Resources

- [Aptos Documentation](https://aptos.dev/)
- [Move Language Book](https://move-language.github.io/move/)
- [Move Tutorial](https://github.com/aptos-labs/aptos-core/tree/main/aptos-move/move-examples)
- [Aptos TypeScript SDK](https://aptos.dev/sdks/ts-sdk/)

## License

MIT License - See LICENSE file for details

## Contributing

Educational example for Web3 multi-language playground. Contributions welcome!
