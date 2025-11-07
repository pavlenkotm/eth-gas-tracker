# 🪙 ERC-20 Token Implementation

Professional ERC-20 token smart contract using OpenZeppelin libraries with minting, burning, and ownership features.

## Features

- ✅ **ERC-20 Standard Compliant**: Full implementation of the ERC-20 token standard
- 🔒 **Ownership Control**: Only owner can mint new tokens
- 🔥 **Burning**: Users can burn their own tokens
- 📊 **Max Supply**: Optional maximum supply cap
- 🛡️ **Security**: Built on OpenZeppelin's battle-tested contracts
- ✨ **Events**: Comprehensive event logging for all operations

## Smart Contract Details

### Constructor Parameters

```solidity
constructor(
    string memory name_,        // Token name (e.g., "Simple Token")
    string memory symbol_,      // Token symbol (e.g., "SMPL")
    uint8 decimals_,           // Decimals (typically 18)
    uint256 initialSupply,     // Initial supply to mint
    uint256 maxSupply_         // Maximum supply (0 for unlimited)
)
```

### Key Functions

- `mint(address to, uint256 amount)` - Mint new tokens (owner only)
- `burn(uint256 amount)` - Burn tokens from your balance
- `burnFrom(address from, uint256 amount)` - Burn tokens from another account (with allowance)
- `updateMaxSupply(uint256 newMaxSupply)` - Update maximum supply cap (owner only)

## Setup & Installation

```bash
# Install dependencies
npm install

# Compile contracts
npx hardhat compile

# Run tests
npx hardhat test

# Run test coverage
npx hardhat coverage
```

## Testing

Comprehensive test suite covering:
- ✅ Deployment and initialization
- ✅ Token minting
- ✅ Token burning
- ✅ Transfers and approvals
- ✅ Max supply enforcement
- ✅ Access control

```bash
npm test
```

## Deployment

### Local Network

```bash
# Terminal 1: Start local node
npx hardhat node

# Terminal 2: Deploy
npm run deploy:local
```

### Testnet (Sepolia)

1. Configure your `.env` file:
```env
ALCHEMY_API_KEY=your_alchemy_key
PRIVATE_KEY=your_deployer_private_key
```

2. Deploy:
```bash
npm run deploy:sepolia
```

## Usage Example

```javascript
// Deploy token
const SimpleToken = await ethers.getContractFactory("SimpleToken");
const token = await SimpleToken.deploy(
  "My Token",
  "MTK",
  18,           // decimals
  1000000,      // 1M initial supply
  10000000      // 10M max supply
);

// Mint tokens
await token.mint(userAddress, ethers.parseUnits("1000", 18));

// Transfer tokens
await token.transfer(recipientAddress, ethers.parseUnits("100", 18));

// Burn tokens
await token.burn(ethers.parseUnits("50", 18));
```

## Security Considerations

- Uses OpenZeppelin v5.0.0 contracts
- Includes access control via `Ownable`
- Prevents minting to zero address
- Enforces max supply cap
- Comprehensive event logging
- Thoroughly tested

## Gas Optimization

- Compiler optimization enabled (200 runs)
- Efficient storage usage
- Minimal external calls

## Dependencies

- **Hardhat**: Development environment
- **OpenZeppelin Contracts**: Secure smart contract library
- **Ethers.js**: Ethereum library for interaction
- **Chai**: Testing framework

## License

MIT License - See LICENSE file for details

## Resources

- [OpenZeppelin ERC-20 Documentation](https://docs.openzeppelin.com/contracts/5.x/erc20)
- [Hardhat Documentation](https://hardhat.org/docs)
- [Ethereum ERC-20 Standard](https://eips.ethereum.org/EIPS/eip-20)
