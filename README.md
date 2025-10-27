# ⛽ ETH Gas Tracker

Tiny Python CLI that reads Ethereum gas using `eth_feeHistory` (no API keys).  
Optionally estimates simple transfer cost in USD.

## 🚀 Quick start
```bash
git clone https://github.com/pavlenkotm/eth-gas-tracker
cd eth-gas-tracker
python -m pip install -r requirements.txt
python -m ethgas.main --show-usd
# или с кастомным RPC:
python -m ethgas.main --rpc https://rpc.ankr.com/eth
