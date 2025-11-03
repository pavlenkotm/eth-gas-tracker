# ⛽ ETH Gas Tracker

Advanced Python CLI for monitoring Ethereum and EVM-compatible blockchain gas prices using `eth_feeHistory` (no API keys required).

## ✨ Features

- **Multi-Network Support**: Ethereum, Polygon, Arbitrum, Optimism, BSC
- **Real-Time Monitoring**: Watch mode with auto-refresh
- **Smart Alerts**: Notifications when gas drops below threshold
- **Historical Tracking**: Save and analyze price history
- **Transaction Cost Calculator**: Estimates for different tx types (transfers, ERC-20, swaps, NFT)
- **Statistics & Analytics**: Min/max/average with recommendations
- **ASCII Graphs**: Visual price trends in terminal
- **JSON Output**: For scripting and automation
- **REST API Server**: Built-in HTTP API for integrations
- **No API Keys**: Uses public RPC endpoints

## 🚀 Quick Start

```bash
git clone https://github.com/pavlenkotm/eth-gas-tracker
cd eth-gas-tracker
python -m pip install -r requirements.txt

# Basic usage
python -m ethgas.main

# Watch mode with detailed info
python -m ethgas.main --watch 10 --detailed --graph --show-costs
```

## 📖 Usage Examples

### Basic Commands

```bash
# Simple gas check
python -m ethgas.main

# Show USD cost for simple transfer
python -m ethgas.main --show-usd

# Detailed view with recommendations
python -m ethgas.main --detailed --show-costs

# Monitor different networks
python -m ethgas.main --network polygon
python -m ethgas.main --network arbitrum
python -m ethgas.main --network optimism
python -m ethgas.main --network bsc
```

### Watch Mode (Real-Time Monitoring)

```bash
# Update every 10 seconds
python -m ethgas.main --watch 10

# Watch with detailed view and graph
python -m ethgas.main --watch 15 --detailed --graph

# Watch multiple networks (run in separate terminals)
python -m ethgas.main --network ethereum --watch 10
python -m ethgas.main --network polygon --watch 10
```

### Alerts & Notifications

```bash
# Alert when gas drops below 30 gwei
python -m ethgas.main --watch 10 --alert 30

# Alert with sound notification
python -m ethgas.main --watch 10 --alert 25 --beep

# Alert on Polygon when below 50 gwei
python -m ethgas.main --network polygon --watch 15 --alert 50 --beep
```

### History & Statistics

```bash
# Track history and show stats
python -m ethgas.main --detailed --history

# Watch and save history
python -m ethgas.main --watch 30 --history --detailed --graph

# Show stats for last 12 hours
python -m ethgas.main --detailed --history --stats-hours 12
```

### JSON Output (for scripting)

```bash
# JSON output
python -m ethgas.main --json

# JSON with all transaction costs
python -m ethgas.main --json --show-costs

# Use in scripts
GAS_DATA=$(python -m ethgas.main --json)
echo $GAS_DATA | jq '.base_fee'
```

### REST API Server

```bash
# Start API server on port 8080
python -m ethgas.main --api

# Custom host and port
python -m ethgas.main --api --host 127.0.0.1 --port 3000
```

#### API Endpoints

```bash
# Get API documentation
curl http://localhost:8080/

# Get current gas for Ethereum
curl http://localhost:8080/gas/ethereum

# Get Polygon gas prices
curl http://localhost:8080/gas/polygon

# List available networks
curl http://localhost:8080/networks

# Get historical data (last 50 records)
curl http://localhost:8080/history/ethereum?limit=50

# Get statistics for last 24 hours
curl http://localhost:8080/stats/ethereum?hours=24

# Health check
curl http://localhost:8080/health
```

### Custom RPC

```bash
# Use custom RPC endpoint
python -m ethgas.main --rpc https://rpc.ankr.com/eth

# Custom RPC with watch mode
python -m ethgas.main --rpc https://your-rpc-url.com --watch 10
```

## 🎨 Output Formats

### Simple Output
```
[Ethereum] Base: 25.3 gwei | Priority: 1.5 | Max: 26.8 | Tx ≈ $0.56
```

### Detailed Output
```
============================================================
🌐 Network: Ethereum
============================================================
⛽ Base Fee:      25.34 gwei
⚡ Priority Tip:  1.50 gwei
💎 Max Fee:       26.84 gwei
💰 Token Price:   $2,450.00

------------------------------------------------------------
📈 Statistics (Recent History):
   Min: 18.50 gwei | Avg: 28.75 gwei | Max: 45.20 gwei

------------------------------------------------------------
🎯 Recommendation: ✅ GOOD - Below average, good time to transact
============================================================

💸 Transaction Cost Estimates:
------------------------------------------------------------
  Simple Transfer      ( 21000 gas):      $1.39
  ERC-20 Transfer      ( 65000 gas):      $4.30
  DEX Swap             (150000 gas):      $9.92
  NFT Mint             (100000 gas):      $6.61
  NFT Transfer         ( 85000 gas):      $5.62
------------------------------------------------------------
```

### ASCII Graph
```
📊 Gas Price History (Base Fee in Gwei)
=================================================================================
2025-11-03 10:00 │ ████████████████████████████ 28.5
2025-11-03 10:30 │ ███████████████████████████████ 32.1
2025-11-03 11:00 │ ████████████████████ 22.4
2025-11-03 11:30 │ ██████████████████ 20.8
2025-11-03 12:00 │ ████████████████████████ 25.3
=================================================================================
```

## 🔧 Command-Line Options

```
Network Options:
  --network {ethereum,polygon,arbitrum,optimism,bsc}
                        Network to monitor (default: ethereum)
  --rpc URL            Custom RPC URL (overrides network default)

Gas Parameters:
  --priority GWEI      Priority tip in gwei (default: 1.5)

Display Options:
  --show-usd           Show simple transfer cost in USD
  --show-costs         Show costs for different transaction types
  --detailed           Show detailed view with stats and recommendations
  --graph              Show ASCII graph (requires --detailed)
  --json               Output in JSON format

Watch Mode:
  --watch SECONDS      Watch mode: update every N seconds

Alerts:
  --alert GWEI         Alert when base fee drops below threshold
  --beep               Make beep sound on alert

History & Statistics:
  --history            Save gas prices to history
  --stats-hours HOURS  Hours of history for statistics (default: 24)

API Server:
  --api                Start REST API server
  --host HOST          API server host (default: 0.0.0.0)
  --port PORT          API server port (default: 8080)
```

## 📦 Supported Networks

| Network | Chain ID | Native Token | RPC |
|---------|----------|--------------|-----|
| Ethereum | 1 | ETH | eth.llamarpc.com |
| Polygon | 137 | MATIC | polygon-rpc.com |
| Arbitrum One | 42161 | ETH | arb1.arbitrum.io/rpc |
| Optimism | 10 | ETH | mainnet.optimism.io |
| BNB Smart Chain | 56 | BNB | bsc-dataseed.binance.org |

## 💡 Transaction Types

| Type | Gas Units | Description |
|------|-----------|-------------|
| Simple Transfer | 21,000 | Basic ETH/native token transfer |
| ERC-20 Transfer | 65,000 | ERC-20 token transfer |
| DEX Swap | 150,000 | Typical DEX swap transaction |
| NFT Mint | 100,000 | NFT minting |
| NFT Transfer | 85,000 | NFT transfer between wallets |

## 📁 Data Storage

Historical data is stored in `~/.ethgas/history.jsonl` in JSON Lines format. Each record contains:
- Timestamp
- Network name
- Base fee
- Priority tip
- Max fee
- Token price in USD

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Add support for more networks

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Links

- GitHub: https://github.com/pavlenkotm/eth-gas-tracker
- Issues: https://github.com/pavlenkotm/eth-gas-tracker/issues

## 💻 Requirements

- Python 3.7+
- aiohttp
- python-dateutil

## 🎯 Use Cases

- **DApp Developers**: Monitor gas prices before deploying contracts
- **Traders**: Wait for optimal gas prices before executing transactions
- **Bots & Automation**: Integrate via JSON output or REST API
- **Multi-Chain Users**: Monitor gas across different EVM networks
- **Cost Optimization**: Plan transactions during low-gas periods
- **Analytics**: Track and analyze historical gas price trends

## ⚠️ Notes

- Gas estimates are approximations and may vary based on actual transaction complexity
- Historical data requires `--history` flag to persist across runs
- API server runs in foreground; use process manager for production
- Token prices fetched from CoinGecko API (no key required)
- RPC endpoints are public and may have rate limits

---

Made with ❤️ for the Ethereum community
