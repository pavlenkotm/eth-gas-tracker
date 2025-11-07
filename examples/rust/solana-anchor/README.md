# ⚓ Solana Counter Program (Anchor)

A production-ready **Solana smart contract** (program) built with the **Anchor framework** in Rust.

## What is Anchor?

Anchor is the most popular framework for Solana development, providing:
- **High-level abstractions** for Solana programs
- **Security best practices** built-in
- **Automatic IDL generation** for client integration
- **Testing framework** with TypeScript support
- **CLI tools** for building and deploying

## Features

- ✅ **Counter Operations**: Initialize, increment, decrement, set, reset
- 🔒 **Access Control**: Authority-based permissions
- 🛡️ **Overflow Protection**: Safe arithmetic with checked operations
- 📝 **Events**: Program logs for all operations
- 🔄 **Authority Transfer**: Transfer control to new owners
- ⚡ **Gas Efficient**: Optimized for Solana's low-cost transactions
- ✅ **Comprehensive Tests**: Full test coverage with TypeScript

## Program Structure

```
counter/
├── programs/counter/src/
│   └── lib.rs              # Main program logic
├── tests/
│   └── counter.ts          # TypeScript tests
├── Anchor.toml             # Anchor configuration
└── Cargo.toml              # Rust dependencies
```

## Instructions

### `initialize`
Initialize a new counter account
- Sets count to 0
- Sets caller as authority

### `increment`
Increment counter by 1 (authority only)

### `decrement`
Decrement counter by 1 (authority only)

### `set`
Set counter to specific value (authority only)

### `reset`
Reset counter to 0 (authority only)

### `transfer_authority`
Transfer authority to new owner (authority only)

## Prerequisites

### Install Solana CLI

```bash
sh -c "$(curl -sSfL https://release.solana.com/stable/install)"
```

### Install Anchor CLI

```bash
cargo install --git https://github.com/coral-xyz/anchor avm --locked --force
avm install latest
avm use latest
```

### Install Node Dependencies

```bash
yarn install
# or
npm install
```

## Setup Local Validator

```bash
# Create Solana config
solana-keygen new

# Start local validator
solana-test-validator
```

## Build & Test

### Build the Program

```bash
# Build with Anchor
anchor build

# Or use cargo directly
cd programs/counter
cargo build-bpf
```

### Run Tests

```bash
# Run all tests
anchor test

# Run tests with logs
anchor test -- --nocapture

# Run on devnet
anchor test --provider.cluster devnet
```

### Deploy

```bash
# Deploy to local validator
anchor deploy

# Deploy to devnet
anchor deploy --provider.cluster devnet

# Deploy to mainnet
anchor deploy --provider.cluster mainnet
```

## Usage Examples

### Initialize Counter

```typescript
import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { Counter } from "./target/types/counter";

const program = anchor.workspace.Counter as Program<Counter>;
const counterAccount = anchor.web3.Keypair.generate();

await program.methods
  .initialize()
  .accounts({
    counter: counterAccount.publicKey,
    user: provider.wallet.publicKey,
    systemProgram: anchor.web3.SystemProgram.programId,
  })
  .signers([counterAccount])
  .rpc();
```

### Increment Counter

```typescript
await program.methods
  .increment()
  .accounts({
    counter: counterAccount.publicKey,
    authority: provider.wallet.publicKey,
  })
  .rpc();
```

### Set Counter Value

```typescript
await program.methods
  .set(new anchor.BN(42))
  .accounts({
    counter: counterAccount.publicKey,
    authority: provider.wallet.publicKey,
  })
  .rpc();
```

### Fetch Counter State

```typescript
const account = await program.account.counter.fetch(
  counterAccount.publicKey
);
console.log("Count:", account.count.toNumber());
console.log("Authority:", account.authority.toString());
```

## Account Structure

```rust
pub struct Counter {
    pub count: u64,        // 8 bytes
    pub authority: Pubkey, // 32 bytes
}
// Total: 40 bytes + 8 bytes discriminator = 48 bytes
```

## Security Features

### Built-in Protections
- ✅ **Overflow/Underflow**: Checked arithmetic operations
- ✅ **Authorization**: `has_one` constraint validates authority
- ✅ **Account Validation**: Automatic account type checking
- ✅ **Rent Exemption**: Accounts initialized with sufficient lamports

### Error Handling

```rust
#[error_code]
pub enum ErrorCode {
    #[msg("Arithmetic overflow occurred")]
    Overflow,
    #[msg("Arithmetic underflow occurred")]
    Underflow,
    #[msg("Unauthorized: Only the authority can perform this action")]
    Unauthorized,
}
```

## Cost Analysis

### Transaction Costs (Devnet/Mainnet)
- **Initialize**: ~0.001 SOL (account creation + rent)
- **Increment/Decrement**: ~0.000005 SOL
- **Set/Reset**: ~0.000005 SOL
- **Transfer Authority**: ~0.000005 SOL

*Note: Costs may vary based on network congestion*

## Client Integration

### Generate TypeScript Client

```bash
anchor build
# IDL is automatically generated in target/idl/counter.json
```

### Use in Frontend

```typescript
import { Program, AnchorProvider } from "@coral-xyz/anchor";
import { Connection, PublicKey } from "@solana/web3.js";
import idl from "./target/idl/counter.json";

const connection = new Connection("https://api.devnet.solana.com");
const provider = new AnchorProvider(connection, wallet, {});
const program = new Program(idl, programId, provider);

// Use program methods as shown above
```

## Debugging

### View Program Logs

```bash
# Follow logs in real-time
solana logs | grep "<PROGRAM_ID>"
```

### Inspect Accounts

```bash
solana account <ACCOUNT_ADDRESS>
```

### Common Issues

**Issue**: "Program failed to complete"
```bash
# Increase compute units
.remainingAccounts([/* additional accounts */])
.preInstructions([
  ComputeBudgetProgram.setComputeUnitLimit({ units: 400000 })
])
```

**Issue**: Account not rent-exempt
```bash
# Check rent status
solana rent <ACCOUNT_SIZE>
```

## Comparison: Solana vs Ethereum

| Feature | Solana | Ethereum |
|---------|--------|----------|
| Language | Rust/C | Solidity/Vyper |
| TPS | ~65,000 | ~15-30 |
| Block Time | ~400ms | ~12s |
| Transaction Cost | $0.00025 | $1-100+ |
| Account Model | Account-based | Contract-based |
| State Storage | Rent-based | Gas-based |

## Resources

- [Anchor Documentation](https://www.anchor-lang.com/)
- [Solana Cookbook](https://solanacookbook.com/)
- [Solana Program Library](https://spl.solana.com/)
- [Anchor Examples](https://github.com/coral-xyz/anchor/tree/master/tests)

## License

MIT License - See LICENSE file for details

## Contributing

Educational example for Web3 multi-language playground. Contributions welcome!
