# ⚡ Web3 Multi-Language Playground

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/pavlenkotm/eth-gas-tracker?style=social)
![GitHub forks](https://img.shields.io/github/forks/pavlenkotm/eth-gas-tracker?style=social)
![GitHub issues](https://img.shields.io/github/issues/pavlenkotm/eth-gas-tracker)
![GitHub license](https://img.shields.io/github/license/pavlenkotm/eth-gas-tracker)
![Commits](https://img.shields.io/github/commit-activity/m/pavlenkotm/eth-gas-tracker)

**Master blockchain development across 50+ programming languages (including exotic ones!)**

[Explore Examples](#-examples-by-language) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🌟 Overview

This repository is a comprehensive **Web3 development playground** showcasing blockchain development across **50+ programming languages and frameworks** - from production-ready to mind-bendingly esoteric! Whether you're building on Ethereum, Solana, Aptos, StarkNet, Fuel, Polkadot, Cardano, Cosmos, or other chains, you'll find examples ranging from professional smart contracts to hilarious esoteric languages.

## 🚀 Installation

```bash
# Core CLI
pip install .

# Optional helpers
pip install .[excel]          # Enable Excel export support
pip install .[notifications]  # Enable desktop notifications
pip install .[all]            # Install every optional extra
```

> Requires Python 3.8+.

### 🎯 Perfect For

- 🚀 **Developers** learning Web3 development
- 🔄 **Polyglot programmers** exploring blockchain
- 🎓 **Students** studying distributed systems
- 👨‍💼 **Teams** evaluating Web3 tech stacks
- 📚 **Educators** teaching blockchain development

---

## ✨ Features

<table>
  <tr>
    <td width="50%">
      <h3>🌐 Multi-Chain Support</h3>
      <ul>
        <li>Ethereum & EVM chains (Solidity, Vyper, Yul, Huff)</li>
        <li>Solana (Rust/Anchor)</li>
        <li>NEAR (Rust)</li>
        <li>Aptos & Sui (Move)</li>
        <li>StarkNet (Cairo)</li>
        <li>Polkadot & Substrate (Ink!, Rust)</li>
        <li>Stacks / Bitcoin L2 (Clarity)</li>
        <li>DFINITY / ICP (Motoko)</li>
        <li>Cardano (Haskell/Plutus)</li>
        <li>Cosmos SDK (Go)</li>
        <li>Fuel Network (Sway)</li>
      </ul>
    </td>
    <td width="50%">
      <h3>💻 50+ Languages</h3>
      <ul>
        <li>Smart Contracts: Solidity, Vyper, Move, Rust, Cairo, Ink!, Clarity, Motoko, Haskell, Go, Yul, Huff, Sway</li>
        <li>Frontend: TypeScript, Svelte, Vue, Elm, Astro, HTML/CSS</li>
        <li>Backend: Go, Elixir, Scala, Ruby, Nim, Crystal, Erlang</li>
        <li>Scripting: Python, Lua, Perl, PHP, PowerShell, Bash</li>
        <li>Systems: Rust, C, Zig, D, Odin, C++</li>
        <li>Functional: Haskell, F#, OCaml, Clojure, Scheme</li>
        <li>Data Science: Julia, R, MATLAB</li>
        <li>🎨 <strong>Esoteric: Brainfuck, Whitespace, LOLCODE, Befunge, ArnoldC</strong></li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>📚 Production-Ready</h3>
      <ul>
        <li>Complete test suites</li>
        <li>Comprehensive documentation</li>
        <li>Security best practices</li>
        <li>Gas optimization</li>
      </ul>
    </td>
    <td width="50%">
      <h3>🔧 DevOps Included</h3>
      <ul>
        <li>CI/CD pipelines</li>
        <li>Deployment scripts</li>
        <li>Automated testing</li>
        <li>Dependabot integration</li>
      </ul>
    </td>
  </tr>
</table>

---

## 📂 Repository Structure

```
eth-gas-tracker/
├── ethgas/                    # 🐍 Python ETH Gas Tracker (Core Project)
│   ├── tracker.py
│   ├── web_ui.py
│   └── ...
├── examples/                  # 🎯 Multi-Language Examples
│   ├── solidity/             # 📜 Smart Contracts
│   │   ├── erc20-token/
│   │   └── erc721-nft/
│   ├── vyper/                # 🐍 Pythonic Smart Contracts
│   │   └── simple-token/
│   ├── rust/                 # 🦀 Solana Programs
│   │   └── solana-anchor/
│   ├── move/                 # 💎 Aptos Smart Contracts
│   │   └── aptos-contract/
│   ├── typescript/           # ⚡ DApp Frontends
│   │   └── wagmi-dapp/
│   ├── go/                   # 🐹 Web3 Utilities
│   │   └── web3-utils/
│   ├── java/                 # ☕ Web3j Integration
│   │   └── web3j-integration/
│   ├── cpp/                  # ⚙️ Crypto Primitives
│   │   └── crypto-primitives/
│   ├── swift/                # 🦅 iOS Wallet SDK
│   │   └── wallet-sdk/
│   ├── haskell/              # λ Plutus Contracts
│   │   └── plutus-contract/
│   ├── bash/                 # 🔧 Deployment Scripts
│   │   └── deployment-scripts/
│   ├── html-css/             # 🎨 Landing Pages
│   │   └── dapp-landing/
│   ├── zig/                  # ⚡ WASM Crypto
│   │   └── wasm-crypto/
│   └── kotlin/               # 🤖 Android Web3
│       └── android-web3/
├── .github/workflows/        # 🔄 CI/CD Pipelines
├── CONTRIBUTING.md          # 🤝 Contribution Guidelines
├── CODE_OF_CONDUCT.md       # 📜 Community Standards
└── README.md                # 📖 This File
```

---

## 🚀 Examples by Language

### Smart Contract Languages

#### 📜 [Solidity](./examples/solidity)
**Ethereum Smart Contracts**
- 🪙 ERC-20 Token with minting/burning
- 🎨 ERC-721 NFT with royalties (EIP-2981)
- 🔒 OpenZeppelin integration
- ✅ Hardhat test suite

```bash
cd examples/solidity/erc20-token
npm install && npx hardhat test
```

#### 🐍 [Vyper](./examples/vyper)
**Pythonic Smart Contracts**
- 💰 Simple ETH Vault
- 🔒 Built-in safety features
- 📊 ApeWorX framework
- ✅ Comprehensive tests

```bash
cd examples/vyper/simple-token
ape compile && ape test
```

#### 🦀 [Rust](./examples/rust)
**Solana Programs**
- 📊 Counter program with Anchor
- 🔑 Authority-based access control
- ⚡ High-performance execution
- ✅ TypeScript test suite

```bash
cd examples/rust/solana-anchor
anchor build && anchor test
```

#### 💎 [Move](./examples/move)
**Aptos Smart Contracts**
- 🪙 Fungible token (Coin standard)
- 🔒 Resource-oriented programming
- 🛡️ Built-in safety guarantees
- ✅ Move test framework

```bash
cd examples/move/aptos-contract
aptos move compile && aptos move test
```

---

### Frontend & Integration

#### ⚡ [TypeScript](./examples/typescript)
**Modern DApp Frontend**
- 👛 Wallet connection (Wagmi)
- 💸 Transaction sending
- 📜 Contract interaction
- 🎨 React + Vite

```bash
cd examples/typescript/wagmi-dapp
npm install && npm run dev
```

#### 🐹 [Go](./examples/go)
**Web3 Utilities**
- 🔗 Ethereum RPC client
- 🔑 Key management
- ✍️ Message signing
- 📦 Transaction monitoring

```bash
cd examples/go/web3-utils
go build && ./web3-utils
```

#### ☕ [Java](./examples/java)
**Web3j Integration**
- 🔗 Ethereum client wrapper
- 💰 Balance queries
- 📝 Transaction handling
- 🔑 Wallet generation

```bash
cd examples/java/web3j-integration
mvn clean install && java -jar target/web3j-integration-1.0.0.jar
```

---

### DevOps & Tooling

#### 🔧 [Bash](./examples/bash)
**Deployment Automation**
- 🚀 Multi-network deployment
- ⛽ Gas price monitoring
- ✅ Pre-deployment checks
- 📝 Deployment reports

```bash
cd examples/bash/deployment-scripts
./deploy-hardhat.sh sepolia
```

#### 🎨 [HTML/CSS](./examples/html-css)
**DApp Landing Page**
- 🌐 Professional landing page
- 📱 Fully responsive
- ⚡ No frameworks needed
- 🎯 SEO optimized

```bash
cd examples/html-css/dapp-landing
open index.html
```

---

### Next-Gen Smart Contract Languages

#### 🏺 [Cairo](./examples/cairo)
**StarkNet Smart Contracts**
- 🔐 Zero-knowledge native
- ⚡ L2 scaling solution
- 🛡️ Built-in safety features
- ✅ Scarb package manager

```bash
cd examples/cairo/starknet-token
scarb build && scarb test
```

#### ⛽ [Sway](./examples/sway)
**Fuel Network Contracts**
- 🦀 Rust-inspired syntax
- ⚡ UTXO-based execution
- 🔒 Memory safety guarantees
- 📊 Parallel transaction processing

```bash
cd examples/sway/fuel-contract
forc build && forc test
```

#### ⚡ [Yul](./examples/yul)
**Low-Level EVM Programming**
- 💰 Maximum gas efficiency
- 🔧 Direct opcode control
- ⚡ 10-15% gas savings
- 🎯 Performance-critical code

```bash
cd examples/yul/evm-optimized
solc --strict-assembly Storage.yul
```

#### 🔥 [Huff](./examples/huff)
**Ultra-Optimized EVM Bytecode**
- 🚀 30-40% gas reduction
- 🎯 Zero abstraction overhead
- ⚙️ Manual stack management
- 🏆 Used by Seaport, Uniswap V4

```bash
cd examples/huff/ultra-optimized
huffc SimpleStorage.huff --bytecode
```

---

### Frontend Frameworks

#### 🦊 [Svelte](./examples/svelte)
**Reactive Web3 Wallet**
- ⚡ Truly reactive (no virtual DOM)
- 📦 Tiny bundle size (~3KB)
- 👛 MetaMask integration
- 💸 Transaction sending

```bash
cd examples/svelte/web3-wallet
npm install && npm run dev
```

#### 🌐 [Vue](./examples/vue)
**Web3 DApp Dashboard**
- 🎯 Composition API
- 💎 Elegant reactivity
- 🔄 State management
- 📊 Real-time updates

```bash
cd examples/vue/dapp-dashboard
npm install && npm run dev
```

---

### Backend & Systems

#### 💧 [Elixir](./examples/elixir)
**Functional Web3 Client**
- 🔄 Concurrent request handling
- 🛡️ Fault-tolerant OTP
- ⚡ Phoenix framework
- 📊 Real-time PubSub

```bash
cd examples/elixir/phoenix-web3
mix deps.get && iex -S mix
```

#### 💎 [Ruby](./examples/ruby)
**Elegant Blockchain API**
- 🎨 Expressive syntax
- 🔧 Metaprogramming
- 📦 RubyGems ecosystem
- 🚀 Rails integration

```bash
cd examples/ruby/eth-client
ruby web3_client.rb
```

#### ⚙️ [Scala](./examples/scala)
**Type-Safe Functional Client**
- 🎯 Functional programming
- 🔒 Strong type system
- ⚡ JVM performance
- 🧩 Pattern matching

```bash
cd examples/scala/ethereum-client
sbt run
```

#### 🔧 [Clojure](./examples/clojure)
**Lisp-Powered Blockchain**
- 🎨 Functional paradigm
- 🔄 Immutable data structures
- 📊 REPL-driven development
- 🧩 Java interop

```bash
cd examples/clojure/smart-contract-tools
lein run
```

---

### Scripting & Automation

#### 🌙 [Lua](./examples/lua)
**Lightweight Blockchain Scripts**
- 🪶 Minimal footprint
- ⚡ Fast execution
- 🎮 Game integration
- 📱 Embedded systems

```bash
cd examples/lua/blockchain-script
lua web3.lua
```

#### 🔮 [Perl](./examples/perl)
**Text Processing & Web3**
- 📝 Regex powerhouse
- 🔧 System automation
- 📊 Data extraction
- 🕸️ Web scraping

```bash
cd examples/perl/web3-monitor
perl web3_client.pl
```

#### 🐘 [PHP](./examples/php)
**Server-Side Web3**
- 🌐 Web backend integration
- 💰 Payment processing
- 🔐 API endpoints
- 📊 Admin dashboards

```bash
cd examples/php/dapp-backend
php Web3Client.php
```

#### ⚡ [PowerShell](./examples/powershell)
**Enterprise Blockchain Automation**
- 🏢 Windows integration
- 🔧 DevOps workflows
- 📊 Monitoring scripts
- 🚀 CI/CD pipelines

```bash
cd examples/powershell/deployment-automation
pwsh Web3-Utils.ps1
```

---

### Systems Programming

#### 🔨 [C](./examples/c)
**High-Performance Crypto**
- ⚡ Bare metal speed
- 🔐 Keccak-256 hashing
- 🧮 Elliptic curves
- 📊 Zero overhead

```bash
cd examples/c/evm-crypto
gcc -o keccak keccak256.c -lcurl -ljson-c -lssl -lcrypto
./keccak
```

#### 👑 [Nim](./examples/nim)
**Expressive Systems Language**
- 🎨 Python-like syntax
- ⚡ C-level performance
- 🔧 Metaprogramming
- 📦 Package manager

```bash
cd examples/nim/crypto-lib
nim c -r web3.nim
```

#### 💎 [Crystal](./examples/crystal)
**Ruby Performance**
- 💎 Ruby-inspired syntax
- ⚡ Compiled to native code
- 🔒 Type safety
- 🚀 Fast execution

```bash
cd examples/crystal/blockchain-api
crystal run web3_client.cr
```

#### 🔷 [D](./examples/d)
**Modern Systems Language**
- ⚡ High performance
- 🔧 Metaprogramming
- 🧩 Template system
- 📊 Memory safety

```bash
cd examples/d/high-performance
dub run
```

#### ⚙️ [Odin](./examples/odin)
**Joy of Programming**
- 🎯 Simple & readable
- ⚡ Fast compilation
- 🔧 Low-level control
- 📦 Minimal runtime

```bash
cd examples/odin/systems-crypto
odin run web3.odin
```

---

### Functional Programming

#### 🔷 [F#](./examples/fsharp)
**Functional-First .NET**
- 🎯 Type inference
- 🔄 Async workflows
- 📊 Pattern matching
- 🧩 LINQ integration

```bash
cd examples/fsharp/defi-analytics
dotnet run
```

#### 🐫 [OCaml](./examples/ocaml)
**Type-Safe Contracts**
- 🔒 Strong type system
- ⚡ Fast compilation
- 🧩 Pattern matching
- 📚 Formal verification

```bash
cd examples/ocaml/type-safe-contracts
dune build && dune exec web3
```

#### 🎨 [Scheme](./examples/scheme)
**Lisp Blockchain**
- 🎨 Minimalist design
- 🔄 Macros & metaprogramming
- 📚 Academic foundations
- 🧩 Homoiconicity

```bash
cd examples/scheme/lisp-blockchain
guile web3.scm
```

#### 📡 [Erlang](./examples/erlang)
**Distributed Blockchain Nodes**
- 🔄 Massive concurrency
- 🛡️ Fault tolerance
- 📡 Distributed systems
- ⚡ Hot code reloading

```bash
cd examples/erlang/distributed-node
erl -compile web3_client
```

---

### Data Science & Analytics

#### 🔬 [Julia](./examples/julia)
**High-Performance Analytics**
- ⚡ Python syntax, C speed
- 📊 Statistical analysis
- 📈 Data visualization
- 🧮 Numerical computing

```bash
cd examples/julia/crypto-analysis
julia blockchain_analysis.jl
```

#### 📊 [R](./examples/r)
**Statistical Blockchain Analysis**
- 📈 ggplot2 visualization
- 📊 Statistical modeling
- 🔬 Research-grade analytics
- 📉 Time series analysis

```bash
cd examples/r/nft-analytics
Rscript web3_analysis.R
```

---

### Esoteric & Fun Languages 🎨

#### 🧠 [Brainfuck](./examples/brainfuck)
**The Minimalist's Nightmare**
- Only 8 commands (><+-.,\[\])
- Turing-complete language
- "Hello Blockchain" in pure minimalism
- Stack-based like EVM

```bash
cd examples/brainfuck/blockchain-hash
bf hello_blockchain.bf
```

#### 👻 [Whitespace](./examples/whitespace)
**The Invisible Language**
- Code using only spaces, tabs, and newlines
- All other characters are comments
- Steganographic programming
- Stack + Heap architecture

```bash
cd examples/whitespace/stealth-contract
wspace hello_eth.ws
```

#### 😹 [LOLCODE](./examples/lolcode)
**I CAN HAZ BLOCKCHAIN?**
- Based on lolcat memes
- `HAI` to start, `KTHXBYE` to end
- `I HAS A BALANCE ITZ 42`
- Most fun language ever

```bash
cd examples/lolcode/lolcat-wallet
lci wallet_balance.lol
```

#### 🎮 [Befunge](./examples/befunge)
**2D Programming Grid**
- Code flows in 2D space (↑↓←→)
- Stack-based execution
- Self-modifying code
- Perfect for Merkle tree visualization

```bash
cd examples/befunge/2d-blockchain
pyfunge hello_blockchain.bf
```

#### 💪 [ArnoldC](./examples/arnoldc)
**GET TO THE BLOCKCHAIN!**
- Every keyword is an Arnold Schwarzenegger quote
- `IT'S SHOWTIME` = start program
- `TALK TO THE HAND` = print
- `I'LL BE BACK` = return
- `HASTA LA VISTA, BABY` = end function

```bash
cd examples/arnoldc/terminator-chain
./arnoldc hello_blockchain.arnoldc
java hello_blockchain
```

---

### Additional Languages

<details>
<summary><b>🔽 Click to expand more</b></summary>

#### ⚙️ C++ - Crypto Primitives
- Hashing algorithms
- BLS signatures
- Elliptic curve operations

#### 🦅 Swift - iOS Wallet SDK
- Mobile wallet integration
- WalletConnect support
- Biometric authentication

#### λ Haskell - Plutus Contracts
- Cardano smart contracts
- Functional programming
- Formal verification

#### ⚡ Zig - WASM Crypto
- Low-level crypto operations
- WebAssembly compilation
- Performance optimization

#### 🤖 Kotlin - Android Web3
- Android app integration
- Web3j for Android
- Mobile-first design

#### 🐍 Python - Gas Tracker
- Multi-network gas monitoring
- Real-time alerts
- Web UI dashboard

</details>

---

## 🎓 Getting Started

### Prerequisites

```bash
# Node.js and npm
node --version  # v18+
npm --version

# Python
python --version  # 3.8+

# Rust
rustc --version

# Go
go version

# Java
java --version
```

### Quick Start

```bash
# Clone repository
git clone https://github.com/pavlenkotm/eth-gas-tracker.git
cd eth-gas-tracker

# Try Python Gas Tracker
python -m ethgas.main --watch 10

# Try Solidity Examples
cd examples/solidity/erc20-token
npm install && npx hardhat test

# Try Rust/Solana
cd examples/rust/solana-anchor
anchor build && anchor test

# Try TypeScript DApp
cd examples/typescript/wagmi-dapp
npm install && npm run dev
```

---

## 📊 Technology Matrix

| Language | Use Case | Framework | Chain | Status |
|----------|----------|-----------|-------|--------|
| **Solidity** | Smart Contracts | Hardhat | Ethereum | ✅ Complete |
| **Vyper** | Smart Contracts | ApeWorX | Ethereum | ✅ Complete |
| **Rust** | Programs | Anchor | Solana / NEAR | ✅ Complete |
| **Move** | Smart Contracts | Aptos CLI | Aptos / Sui | ✅ Complete |
| **Cairo** | Smart Contracts | Scarb | StarkNet | ✅ Complete |
| **Yul** | Low-level EVM | Solc | Ethereum | ✅ Complete |
| **Huff** | Ultra-optimized | Huffc | Ethereum | ✅ Complete |
| **Sway** | Smart Contracts | Forc | Fuel Network | ✅ Complete |
| **Ink!** | Smart Contracts | Cargo Contract | Polkadot / Substrate | 📝 Planned |
| **Clarity** | Smart Contracts | Clarinet | Stacks / Bitcoin L2 | 📝 Planned |
| **Motoko** | Smart Contracts | dfx | DFINITY / ICP | 📝 Planned |
| **Haskell** | Smart Contracts | Plutus | Cardano | 🚧 Basic |
| **Go** | SDK/Backend | Cosmos SDK | Cosmos / Ethereum | ✅ Complete |
| **TypeScript** | Frontend | Wagmi/React | Multi-chain | ✅ Complete |
| **Java** | Backend | Web3j | Ethereum | ✅ Complete |
| **Python** | CLI/Backend | Web3.py | Multi-chain | ✅ Complete |
| **Bash** | DevOps | Shell | - | ✅ Complete |
| **HTML/CSS** | Frontend | Vanilla | - | ✅ Complete |
| **C++** | Crypto | Custom | - | 🚧 Basic |
| **Swift** | Mobile | Web3.swift | Ethereum | 🚧 Basic |
| **Zig** | WASM | Custom | - | 🚧 Basic |
| **Kotlin** | Mobile | Web3j-Android | Ethereum | 🚧 Basic |
| **🧠 Brainfuck** | Esoteric/Educational | Interpreter | - | ✅ Complete |
| **👻 Whitespace** | Esoteric/Educational | Interpreter | - | ✅ Complete |
| **😹 LOLCODE** | Esoteric/Educational | lci | - | ✅ Complete |
| **🎮 Befunge** | Esoteric/Educational | pyfunge | - | ✅ Complete |
| **💪 ArnoldC** | Esoteric/Educational | Java bytecode | - | ✅ Complete |

---

## 🧪 Testing

Each example includes comprehensive tests:

```bash
# Solidity (Hardhat)
npx hardhat test

# Rust (Anchor)
anchor test

# Move (Aptos)
aptos move test

# Python
pytest

# Go
go test ./...

# Java
mvn test
```

---

## 🔄 CI/CD

Automated workflows for:
- ✅ Linting and formatting
- ✅ Unit testing
- ✅ Security scanning
- ✅ Dependency updates (Dependabot)

See [`.github/workflows/`](./.github/workflows/) for configuration.

---

## 📖 Documentation

Each example includes:
- 📄 Detailed README
- 💻 Code comments
- 🧪 Test examples
- 🚀 Deployment guide
- 🔒 Security considerations

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Ways to Contribute

- 🐛 Report bugs
- ✨ Suggest features
- 📝 Improve documentation
- 🔧 Submit pull requests
- ⭐ Star the repository

---

## 📜 Code of Conduct

Please read our [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) before contributing.

---

## 🎯 Roadmap

- [ ] Add more language examples
- [ ] Create video tutorials
- [ ] Build interactive playground
- [ ] Add more chain integrations
- [ ] Expand test coverage
- [ ] Create deployment templates

---

## 📊 Repository Stats

![GitHub Stats](https://img.shields.io/github/languages/count/pavlenkotm/eth-gas-tracker)
![Code Size](https://img.shields.io/github/languages/code-size/pavlenkotm/eth-gas-tracker)
![Contributors](https://img.shields.io/github/contributors/pavlenkotm/eth-gas-tracker)
![Last Commit](https://img.shields.io/github/last-commit/pavlenkotm/eth-gas-tracker)

---

## 🙏 Acknowledgments

- **Ethereum** - Smart contract platform
- **Solana** - High-performance blockchain
- **Aptos** - Move-based blockchain
- **OpenZeppelin** - Smart contract library
- **Hardhat** - Ethereum development environment
- **Anchor** - Solana framework
- **Web3.js** / **Ethers.js** - JavaScript libraries
- **go-ethereum** - Go Ethereum implementation
- **Web3j** - Java Ethereum library

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for details.

---

## 🔗 Links

- **GitHub**: [pavlenkotm/eth-gas-tracker](https://github.com/pavlenkotm/eth-gas-tracker)
- **Issues**: [Report a bug](https://github.com/pavlenkotm/eth-gas-tracker/issues)
- **Discussions**: [Join the conversation](https://github.com/pavlenkotm/eth-gas-tracker/discussions)

---

<div align="center">

**⭐ Star this repository if you find it helpful!**

Made with ❤️ for the Web3 community

![Footer Banner](https://img.shields.io/badge/Web3-Multi--Language-blueviolet?style=for-the-badge)

</div>
