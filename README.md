# ⚡ Web3 Multi-Language Playground

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/pavlenkotm/eth-gas-tracker?style=social)
![GitHub forks](https://img.shields.io/github/forks/pavlenkotm/eth-gas-tracker?style=social)
![GitHub issues](https://img.shields.io/github/issues/pavlenkotm/eth-gas-tracker)
![GitHub license](https://img.shields.io/github/license/pavlenkotm/eth-gas-tracker)
![Commits](https://img.shields.io/github/commit-activity/m/pavlenkotm/eth-gas-tracker)

**Master blockchain development across 15+ programming languages**

[Explore Examples](#-examples-by-language) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🌟 Overview

This repository is a comprehensive **Web3 development playground** showcasing blockchain development across **15+ programming languages and frameworks**. Whether you're building on Ethereum, Solana, Aptos, Cardano, or other chains, you'll find production-ready examples with complete documentation.

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
        <li>Ethereum & EVM chains</li>
        <li>Solana</li>
        <li>Aptos</li>
        <li>Cardano</li>
      </ul>
    </td>
    <td width="50%">
      <h3>💻 15+ Languages</h3>
      <ul>
        <li>Solidity, Vyper, Rust</li>
        <li>Move, TypeScript, Go</li>
        <li>Java, C++, Swift, Haskell</li>
        <li>Python, Bash, HTML/CSS, Zig, Kotlin</li>
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

### Additional Languages

<details>
<summary><b>🔽 Click to expand</b></summary>

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
| **Rust** | Programs | Anchor | Solana | ✅ Complete |
| **Move** | Smart Contracts | Aptos CLI | Aptos | ✅ Complete |
| **TypeScript** | Frontend | Wagmi/React | Multi-chain | ✅ Complete |
| **Go** | Backend/CLI | go-ethereum | Ethereum | ✅ Complete |
| **Java** | Backend | Web3j | Ethereum | ✅ Complete |
| **Python** | CLI/Backend | Web3.py | Multi-chain | ✅ Complete |
| **Bash** | DevOps | Shell | - | ✅ Complete |
| **HTML/CSS** | Frontend | Vanilla | - | ✅ Complete |
| **C++** | Crypto | Custom | - | 🚧 Basic |
| **Swift** | Mobile | Web3.swift | Ethereum | 🚧 Basic |
| **Haskell** | Smart Contracts | Plutus | Cardano | 🚧 Basic |
| **Zig** | WASM | Custom | - | 🚧 Basic |
| **Kotlin** | Mobile | Web3j-Android | Ethereum | 🚧 Basic |

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
