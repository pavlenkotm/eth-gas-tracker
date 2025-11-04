# ⛽ ETH Gas Tracker v2.0

Advanced Python CLI & Web UI for monitoring Ethereum and EVM-compatible blockchain gas prices using `eth_feeHistory` (no API keys required).

## ✨ Features

### Core Features
- **Multi-Network Support**: Ethereum, Polygon, Arbitrum, Optimism, BSC, Base, zkSync Era, Avalanche
- **Real-Time Monitoring**: Watch mode with auto-refresh
- **Smart Alerts**: Multiple notification channels (CLI, Desktop, Webhooks)
- **Historical Tracking**: Save and analyze price history
- **Transaction Cost Calculator**: Estimates for different tx types (transfers, ERC-20, swaps, NFT)
- **Statistics & Analytics**: Min/max/average with recommendations
- **ASCII Graphs**: Visual price trends in terminal
- **JSON Output**: For scripting and automation
- **REST API Server**: Built-in HTTP API for integrations
- **No API Keys**: Uses public RPC endpoints

### 🆕 New in v2.0
- **Network Comparison**: Compare gas prices across all networks simultaneously
- **Data Export**: Export history to CSV, Excel, or JSON formats
- **Price Prediction**: AI-powered gas price forecasting with multiple algorithms
- **Desktop Notifications**: Native OS notifications (Windows, macOS, Linux)
- **Webhook Integration**: Send alerts to Slack, Discord, Microsoft Teams, or custom webhooks
- **Advanced Statistics**: Percentiles, volatility analysis, standard deviation, coefficient of variation
- **Web UI**: Beautiful web-based dashboard with real-time updates
- **New Networks**: Support for Base, zkSync Era, and Avalanche C-Chain

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

## 🆕 New Features in v2.0

### Network Comparison

Compare gas prices across all supported networks:

```bash
# Compare all networks (table format)
python -m ethgas.main --compare

# Compare with specific transaction type
python -m ethgas.main --compare --compare-tx-type erc20

# Compare in JSON format
python -m ethgas.main --compare --json
```

Output example:
```
====================================================================================================
GAS PRICE COMPARISON - Simple Transfer (21,000 gas)
====================================================================================================
Network              Base Fee        Priority        Max Fee         Cost (Native)   Cost (USD)
----------------------------------------------------------------------------------------------------
🏆 Polygon            25.34 gwei      1.50 gwei       26.84 gwei      0.000564 MATIC  $0.0005
2. Base               12.50 gwei      1.00 gwei       13.50 gwei      0.000284 ETH    $0.6950
3. Arbitrum One       0.15 gwei       0.01 gwei       0.16 gwei       0.000003 ETH    $0.0075
```

### Data Export

Export historical data for analysis:

```bash
# Export to CSV
python -m ethgas.main --export csv

# Export to Excel with custom path
python -m ethgas.main --export excel --export-path gas_data.xlsx

# Export to JSON (last 1000 records)
python -m ethgas.main --export json --export-limit 1000

# Export specific network data
python -m ethgas.main --network polygon --export csv
```

### Price Prediction

Predict future gas prices based on historical data:

```bash
# Predict using moving average (default)
python -m ethgas.main --predict

# Predict using exponential weighted moving average
python -m ethgas.main --predict --predict-method exponential

# Predict using linear regression
python -m ethgas.main --predict --predict-method linear

# Predict for specific network
python -m ethgas.main --network polygon --predict
```

Output example:
```
============================================================
GAS PRICE PREDICTION (Moving Average)
============================================================
Predicted Base Fee:          24.50 gwei
Predicted Priority Tip:       1.50 gwei
Predicted Max Fee:           26.00 gwei
------------------------------------------------------------
Confidence:                   85.5%
Trend:                        DECREASING
============================================================
```

### Desktop Notifications

Get native OS notifications when gas drops below threshold:

```bash
# Enable desktop notifications
python -m ethgas.main --watch 10 --alert 30 --desktop-notify

# Watch with notifications (no beep)
python -m ethgas.main --watch 15 --alert 25 --desktop-notify
```

Notifications work on:
- Windows (Windows 10+)
- macOS (all versions)
- Linux (with notification daemon)

### Webhook Integration

Send alerts to Slack, Discord, Teams, or custom webhooks:

```bash
# Single webhook URL
python -m ethgas.main --watch 10 --alert 30 --webhook https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Multiple webhooks
python -m ethgas.main --watch 10 --alert 30 \
  --webhook https://hooks.slack.com/... \
  --webhook https://discord.com/api/webhooks/...

# Load webhooks from file
python -m ethgas.main --watch 10 --alert 30 --webhook-file webhooks.txt
```

#### Webhook File Format (`webhooks.txt`):
```
# Slack webhook
https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Discord webhook
https://discord.com/api/webhooks/YOUR/WEBHOOK/ID/TOKEN

# Microsoft Teams webhook
https://outlook.office.com/webhook/YOUR/WEBHOOK/URL
```

Supported platforms:
- Slack (auto-formatted)
- Discord (auto-formatted)
- Microsoft Teams (auto-formatted)
- Custom HTTP endpoints (JSON payload)

### Advanced Statistics

View detailed statistical analysis with percentiles, volatility, and more:

```bash
# Show advanced statistics
python -m ethgas.main --advanced-stats

# Advanced stats for specific timeframe
python -m ethgas.main --advanced-stats --stats-hours 12

# Advanced stats for specific network
python -m ethgas.main --network polygon --advanced-stats
```

Output example:
```
================================================================================
ADVANCED GAS PRICE STATISTICS
================================================================================
Sample Size: 245 records

BASE FEE STATISTICS (gwei):
--------------------------------------------------------------------------------
  Minimum:                   18.50
  25th Percentile:           22.30
  Median (50th):             25.40
  Average (Mean):            26.75
  75th Percentile:           31.20
  90th Percentile:           38.50
  95th Percentile:           42.80
  Maximum:                   45.20

  Range:                     26.70
  Standard Deviation:         6.42
  Variance:                  41.22
  Coefficient of Var:        24.01%
  Volatility:                Moderate
================================================================================
```

### Web UI Dashboard

Launch a beautiful web-based dashboard:

```bash
# Start Web UI (default: http://0.0.0.0:8080)
python -m ethgas.main --web-ui

# Custom host and port
python -m ethgas.main --web-ui --host 127.0.0.1 --port 3000
```

Features:
- Real-time gas prices for all networks
- Auto-refresh with configurable intervals
- Network comparison table
- Beautiful responsive design
- Works on desktop and mobile

Access at: `http://localhost:8080`

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
  --network {ethereum,polygon,arbitrum,optimism,bsc,base,zksync,avalanche}
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

🆕 New Features:
Comparison:
  --compare            Compare gas prices across all networks
  --compare-tx-type    Transaction type for comparison (default: simple)

Export:
  --export {csv,excel,json}  Export historical data to file
  --export-path PATH   Custom path for export file
  --export-limit N     Limit number of records to export

Prediction:
  --predict            Predict future gas prices
  --predict-method {moving_average,exponential,linear}
                       Prediction algorithm (default: moving_average)

Notifications:
  --desktop-notify     Enable desktop notifications for alerts
  --webhook URL        Webhook URL for alerts (can be used multiple times)
  --webhook-file PATH  File containing webhook URLs (one per line)

Advanced Analytics:
  --advanced-stats     Show advanced statistics (percentiles, volatility, etc.)

Web UI:
  --web-ui             Start web-based user interface
```

## 📦 Supported Networks

| Network | Chain ID | Native Token | RPC |
|---------|----------|--------------|-----|
| Ethereum | 1 | ETH | eth.llamarpc.com |
| Polygon | 137 | MATIC | polygon-rpc.com |
| Arbitrum One | 42161 | ETH | arb1.arbitrum.io/rpc |
| Optimism | 10 | ETH | mainnet.optimism.io |
| BNB Smart Chain | 56 | BNB | bsc-dataseed.binance.org |
| 🆕 Base | 8453 | ETH | mainnet.base.org |
| 🆕 zkSync Era | 324 | ETH | mainnet.era.zksync.io |
| 🆕 Avalanche C-Chain | 43114 | AVAX | api.avax.network/ext/bc/C/rpc |

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

### Core Requirements
- Python 3.7+
- aiohttp >= 3.9
- python-dateutil >= 2.8.0

### Optional Requirements
- openpyxl >= 3.1.0 (for Excel export)
- plyer >= 2.1.0 (for desktop notifications)

Install all dependencies:
```bash
pip install -r requirements.txt
```

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
