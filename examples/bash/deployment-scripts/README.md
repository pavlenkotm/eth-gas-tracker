# 🔧 Bash Deployment Scripts

Professional **deployment automation** scripts for Ethereum smart contracts and node management.

## Scripts

### 1. `deploy-hardhat.sh`

Comprehensive Hardhat deployment script with:
- ✅ Dependency checking
- 🔨 Automated compilation
- ✅ Test execution
- 🚀 Multi-network deployment
- ⛽ Gas price monitoring
- 📝 Deployment reports
- ✅ Contract verification

### 2. `manage-node.sh`

Local Ethereum node management:
- 🟢 Start/stop Hardhat node
- 🟢 Start/stop Ganache
- 📊 Status checking
- 🔄 Restart functionality

## Usage

### Make Scripts Executable

```bash
chmod +x deploy-hardhat.sh manage-node.sh
```

### Deploy Contracts

```bash
# Deploy to localhost
./deploy-hardhat.sh localhost

# Deploy to Sepolia testnet
./deploy-hardhat.sh sepolia

# Deploy to mainnet (with confirmation)
./deploy-hardhat.sh mainnet

# Skip tests
./deploy-hardhat.sh sepolia --skip-tests
```

### Manage Local Node

```bash
# Start Hardhat node
./manage-node.sh start

# Start Ganache
./manage-node.sh start-ganache

# Stop node
./manage-node.sh stop

# Restart node
./manage-node.sh restart

# Check status
./manage-node.sh status
```

## Features

### deploy-hardhat.sh

#### 🎨 Colored Output
- Success messages in green
- Errors in red
- Warnings in yellow
- Info in blue

#### 🔍 Pre-deployment Checks
- Node.js installation
- npm availability
- Hardhat installation
- .env file presence

#### ⚠️ Safety Features
- Mainnet deployment confirmation
- Test execution before deployment
- Gas price monitoring
- Error handling with exit codes

#### 📝 Deployment Reports
Automatically generates reports in `deployments/` with:
- Timestamp
- Network information
- Contract addresses
- Transaction hashes
- Gas usage

### manage-node.sh

#### Node Management
- Start local Ethereum nodes
- Stop running nodes
- Check node status
- Restart functionality

#### PID Tracking
- Stores process IDs
- Clean shutdown
- Prevents duplicate instances

## Configuration

### .env File

Create `.env` in your project root:

```env
# Sepolia Testnet
SEPOLIA_RPC_URL=https://rpc.sepolia.org
SEPOLIA_PRIVATE_KEY=your_private_key_here

# Ethereum Mainnet
MAINNET_RPC_URL=https://eth.llamarpc.com
MAINNET_PRIVATE_KEY=your_private_key_here

# Polygon
POLYGON_RPC_URL=https://polygon-rpc.com
POLYGON_PRIVATE_KEY=your_private_key_here

# API Keys for Verification
ETHERSCAN_API_KEY=your_etherscan_api_key
POLYGONSCAN_API_KEY=your_polygonscan_api_key
```

### Hardhat Config

Ensure `hardhat.config.js` has network configurations:

```javascript
require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL,
      accounts: [process.env.SEPOLIA_PRIVATE_KEY]
    },
    mainnet: {
      url: process.env.MAINNET_RPC_URL,
      accounts: [process.env.MAINNET_PRIVATE_KEY]
    }
  }
};
```

## Best Practices

### 1. Always Test Before Deploy

```bash
# Run tests first
npx hardhat test

# Then deploy
./deploy-hardhat.sh sepolia
```

### 2. Use Testnet First

```bash
# Deploy to testnet
./deploy-hardhat.sh sepolia

# Verify everything works

# Then deploy to mainnet
./deploy-hardhat.sh mainnet
```

### 3. Check Gas Prices

Monitor gas prices before mainnet deployment:
```bash
# Check current gas prices
curl -s https://api.etherscan.io/api\?module=gastracker\&action=gasoracle
```

### 4. Verify Contracts

After deployment, verify on block explorer:
```bash
npx hardhat verify --network sepolia CONTRACT_ADDRESS "Constructor Arg"
```

## Troubleshooting

### Port Already in Use

```bash
# Find process using port
lsof -i :8545

# Kill process
kill -9 <PID>

# Or use the stop script
./manage-node.sh stop
```

### Compilation Errors

```bash
# Clean build artifacts
npx hardhat clean

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Deployment Fails

Check:
- [ ] Private key is correct
- [ ] Account has sufficient balance
- [ ] RPC URL is accessible
- [ ] Network name matches hardhat.config.js

## Advanced Usage

### Custom Deployment Script

```bash
#!/bin/bash
# my-deploy.sh

source deploy-hardhat.sh

# Add custom logic
MY_CONTRACT_ADDRESS="0x..."
echo "Deployed at: $MY_CONTRACT_ADDRESS"
```

### Continuous Deployment

```bash
# Watch for changes and redeploy
while inotifywait -e modify contracts/; do
    ./deploy-hardhat.sh localhost
done
```

## Security Notes

- ⚠️ **Never commit private keys** to version control
- ⚠️ Use `.gitignore` for `.env` files
- ⚠️ Test on testnet before mainnet
- ⚠️ Verify contracts after deployment

## Resources

- [Hardhat Documentation](https://hardhat.org/docs)
- [Bash Scripting Guide](https://www.gnu.org/software/bash/manual/)
- [Ethereum Best Practices](https://consensys.github.io/smart-contract-best-practices/)

## License

MIT License - See LICENSE file for details
