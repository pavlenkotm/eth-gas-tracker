# 🌙 Lua Blockchain Script

Lightweight Web3 scripting with **Lua** - perfect for automation, game development, and embedded blockchain interactions.

## 🌟 Features

- 🪶 **Lightweight**: Minimal dependencies
- ⚡ **Fast Execution**: Compiled to bytecode
- 🎮 **Game Integration**: Perfect for Web3 games
- 🔧 **Scriptable**: Easy automation
- 📦 **Portable**: Cross-platform

## 🚀 Quick Start

```bash
cd examples/lua/blockchain-script

# Install Lua and dependencies
sudo apt-get install lua5.4 luarocks
luarocks install luasocket
luarocks install json-lua

# Run script
lua web3.lua
```

## 📖 Usage

```lua
local Web3 = require("web3")

-- Create client
local client = Web3:new("https://eth.llamarpc.com")

-- Get block number
local block = client:get_block_number()
print("Block:", block)

-- Check balance
local balance = client:get_balance("0x...")
print("Balance:", balance, "ETH")

-- Get gas price
local gas = client:get_gas_price()
print("Gas:", gas, "Gwei")
```

## 🎮 Use Cases

- Web3 game scripting
- Blockchain automation
- IoT devices
- Embedded systems
- Configuration scripts

## 📄 License

MIT License
