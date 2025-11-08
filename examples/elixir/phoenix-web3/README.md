# 💧 Elixir Web3 Client

Functional, concurrent Web3 client built with **Elixir** and **OTP**, demonstrating the power of the BEAM VM for blockchain applications.

## 🌟 Features

- 🔄 **GenServer-based**: Concurrent request handling
- ⚡ **Fault Tolerant**: OTP supervision trees
- 🧮 **Type Safe**: Decimal precision for ETH values
- 📊 **Real-time Updates**: Phoenix PubSub integration
- 🎯 **Pattern Matching**: Elegant error handling

## 🚀 Quick Start

```bash
cd examples/elixir/phoenix-web3

# Install dependencies
mix deps.get

# Run interactive shell
iex -S mix

# Usage
iex> Web3Client.get_block_number()
{:ok, 18500000}

iex> Web3Client.get_balance("0x...")
{:ok, #Decimal<1.5>}
```

## 📖 Usage Examples

### Get Block Number

```elixir
{:ok, block_number} = Web3Client.get_block_number()
IO.puts("Current block: #{block_number}")
```

### Check Balance

```elixir
address = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb"
{:ok, balance} = Web3Client.get_balance(address)
IO.puts("Balance: #{balance} ETH")
```

### Monitor Gas Price

```elixir
{:ok, gas_price} = Web3Client.get_gas_price()
IO.puts("Gas price: #{gas_price} Gwei")
```

## 📄 License

MIT License
