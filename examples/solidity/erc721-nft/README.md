# 🎨 ERC-721 NFT Collection

Professional ERC-721 NFT smart contract with minting, metadata, royalties, and advanced features using OpenZeppelin.

## Features

- ✅ **ERC-721 Standard Compliant**: Full NFT implementation
- 🎨 **Metadata Support**: On-chain and IPFS metadata via token URI
- 💰 **Public Minting**: Enable/disable public minting with configurable price
- 👑 **Owner Minting**: Free minting for contract owner
- 📦 **Batch Minting**: Mint multiple NFTs in one transaction
- 🔥 **Burnable**: NFT owners can burn their tokens
- 💎 **Royalties**: EIP-2981 compatible royalty support
- 🎯 **Max Supply**: Optional maximum supply cap
- 💸 **Withdrawable**: Owner can withdraw mint proceeds

## Smart Contract Details

### Constructor Parameters

```solidity
constructor(
    string memory name_,       // Collection name (e.g., "My NFT Collection")
    string memory symbol_,     // Collection symbol (e.g., "MNFT")
    string memory baseURI_,    // Base URI for metadata
    uint256 maxSupply_,        // Maximum supply (0 for unlimited)
    uint256 mintPrice_         // Mint price in wei
)
```

### Key Functions

#### Owner Functions
- `safeMint(address to, string memory uri)` - Mint single NFT (owner)
- `batchMint(address to, string[] memory uris)` - Mint multiple NFTs (owner)
- `setPublicMintEnabled(bool enabled)` - Toggle public minting
- `setMintPrice(uint256 newPrice)` - Update mint price
- `setBaseURI(string memory newBaseURI)` - Update base URI
- `setRoyaltyInfo(address receiver, uint96 feeNumerator)` - Set royalty info
- `withdraw()` - Withdraw contract balance

#### Public Functions
- `publicMint(string memory uri)` - Mint NFT (public, requires payment)
- `burn(uint256 tokenId)` - Burn NFT (owner only)
- `royaltyInfo(uint256 tokenId, uint256 salePrice)` - Get royalty info
- `totalSupply()` - Get total minted count
- `tokenURI(uint256 tokenId)` - Get token metadata URI

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

## Deployment

### Local Network

```bash
# Terminal 1: Start local node
npx hardhat node

# Terminal 2: Deploy
npm run deploy:local
```

### Testnet Deployment

Create `.env` file:
```env
ALCHEMY_API_KEY=your_alchemy_key
PRIVATE_KEY=your_deployer_private_key
```

Deploy to Sepolia:
```bash
npm run deploy:sepolia
```

## Usage Examples

### Deploy NFT Collection

```javascript
const SimpleNFT = await ethers.getContractFactory("SimpleNFT");
const nft = await SimpleNFT.deploy(
  "My NFT Collection",
  "MNFT",
  "ipfs://QmYourBaseURI/",
  10000,  // max supply
  ethers.parseEther("0.05")  // 0.05 ETH mint price
);
```

### Mint NFT (Owner)

```javascript
await nft.safeMint(
  userAddress,
  "ipfs://QmYourTokenURI/1.json"
);
```

### Enable Public Minting

```javascript
await nft.setPublicMintEnabled(true);
```

### Public Mint

```javascript
await nft.publicMint(
  "ipfs://QmYourTokenURI/2.json",
  { value: ethers.parseEther("0.05") }
);
```

### Batch Mint

```javascript
const uris = [
  "ipfs://QmURI/1.json",
  "ipfs://QmURI/2.json",
  "ipfs://QmURI/3.json"
];
await nft.batchMint(recipientAddress, uris);
```

### Set Royalties

```javascript
// Set 5% royalty
await nft.setRoyaltyInfo(
  artistAddress,
  500  // 500 basis points = 5%
);
```

### Withdraw Funds

```javascript
await nft.withdraw();
```

## Metadata Format

Token metadata should follow the ERC-721 metadata standard:

```json
{
  "name": "My NFT #1",
  "description": "This is my awesome NFT",
  "image": "ipfs://QmImageHash",
  "attributes": [
    {
      "trait_type": "Background",
      "value": "Blue"
    },
    {
      "trait_type": "Rarity",
      "value": "Legendary"
    }
  ]
}
```

## Security Features

- ✅ Uses OpenZeppelin v5.0.0 contracts
- ✅ Reentrancy protection
- ✅ Access control via `Ownable`
- ✅ Safe minting with `_safeMint`
- ✅ Overflow protection
- ✅ Refunds excess payment

## Gas Optimization

- Compiler optimization enabled
- Efficient counter library
- Batch operations for bulk minting
- Minimal storage usage

## Testing

Comprehensive test coverage including:
- ✅ Deployment and initialization
- ✅ Owner minting
- ✅ Public minting
- ✅ Batch minting
- ✅ Price validation
- ✅ Max supply enforcement
- ✅ Metadata retrieval
- ✅ Burning
- ✅ Royalty calculations
- ✅ Withdrawals

## Royalty Standard (EIP-2981)

The contract implements EIP-2981 for marketplace royalty support:

```javascript
// Get royalty info for a sale
const [receiver, amount] = await nft.royaltyInfo(
  tokenId,
  ethers.parseEther("1.0")  // sale price
);
```

## Common Use Cases

- 🖼️ **Art Collections**: Digital art NFT marketplaces
- 🎮 **Gaming Assets**: In-game items and characters
- 🎫 **Event Tickets**: Tokenized event access
- 🏆 **Membership Tokens**: Exclusive community access
- 📚 **Collectibles**: Trading cards and collectibles

## License

MIT License - See LICENSE file for details

## Resources

- [OpenZeppelin ERC-721 Documentation](https://docs.openzeppelin.com/contracts/5.x/erc721)
- [EIP-721 Specification](https://eips.ethereum.org/EIPS/eip-721)
- [EIP-2981 Royalty Standard](https://eips.ethereum.org/EIPS/eip-2981)
- [NFT Metadata Standards](https://docs.opensea.io/docs/metadata-standards)
