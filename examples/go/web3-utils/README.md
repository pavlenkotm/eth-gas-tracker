# 🐹 Go Web3 Utilities

Production-ready **Web3 utilities** written in **Go** using `go-ethereum` (Geth) client library.

## Features

- 🔗 **RPC Client**: Connect to Ethereum nodes
- 💰 **Balance Queries**: Check ETH balances
- ⛽ **Gas Price**: Get current gas prices
- 🔑 **Key Management**: Generate and manage private keys
- ✍️ **Message Signing**: Sign and verify messages
- 📦 **Block Data**: Query block information
- 📝 **Transactions**: Get transaction details and receipts
- 🔄 **Unit Conversion**: Wei ↔ ETH conversion

## Prerequisites

```bash
# Install Go 1.21+
# Download from https://go.dev/dl/

# Verify installation
go version
```

## Installation

```bash
# Clone or navigate to directory
cd examples/go/web3-utils

# Download dependencies
go mod download

# Build the application
go build -o web3-utils

# Run
./web3-utils
```

## Usage

### Basic Example

```go
package main

import (
    "fmt"
    "log"
)

func main() {
    // Create Web3Utils instance
    utils, err := NewWeb3Utils("https://eth.llamarpc.com")
    if err != nil {
        log.Fatal(err)
    }
    defer utils.Close()

    // Get latest block
    blockNum, err := utils.GetBlockNumber()
    if err != nil {
        log.Fatal(err)
    }
    fmt.Printf("Latest block: %d\n", blockNum)
}
```

### Get Account Balance

```go
balance, err := utils.GetBalance("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
if err != nil {
    log.Fatal(err)
}

ethBalance := WeiToEth(balance)
fmt.Printf("Balance: %.4f ETH\n", ethBalance)
```

### Generate New Wallet

```go
privateKey, err := GeneratePrivateKey()
if err != nil {
    log.Fatal(err)
}

address := PrivateKeyToAddress(privateKey)
fmt.Printf("Address: %s\n", address.Hex())
```

### Sign Message

```go
message := []byte("Hello, Ethereum!")
signature, err := SignMessage(message, privateKey)
if err != nil {
    log.Fatal(err)
}

fmt.Printf("Signature: %x\n", signature)
```

### Verify Signature

```go
isValid := VerifySignature(message, signature, address)
fmt.Printf("Valid: %v\n", isValid)
```

### Get Gas Price

```go
gasPrice, err := utils.GetGasPrice()
if err != nil {
    log.Fatal(err)
}

gasPriceGwei := new(big.Float).Quo(
    new(big.Float).SetInt(gasPrice),
    big.NewFloat(1e9),
)
fmt.Printf("Gas Price: %.2f Gwei\n", gasPriceGwei)
```

### Get Transaction Details

```go
txHash := "0x..."
tx, isPending, err := utils.GetTransactionByHash(txHash)
if err != nil {
    log.Fatal(err)
}

fmt.Printf("From: %s\n", tx.From().Hex())
fmt.Printf("To: %s\n", tx.To().Hex())
fmt.Printf("Value: %s\n", tx.Value().String())
fmt.Printf("Pending: %v\n", isPending)
```

### Get Transaction Receipt

```go
receipt, err := utils.GetTransactionReceipt(txHash)
if err != nil {
    log.Fatal(err)
}

fmt.Printf("Status: %d\n", receipt.Status)
fmt.Printf("Gas Used: %d\n", receipt.GasUsed)
fmt.Printf("Block Number: %d\n", receipt.BlockNumber)
```

## API Reference

### Web3Utils Methods

```go
// NewWeb3Utils creates a new Web3Utils instance
func NewWeb3Utils(rpcURL string) (*Web3Utils, error)

// GetBalance retrieves the balance of an address
func (w *Web3Utils) GetBalance(address string) (*big.Int, error)

// GetBlockNumber gets the latest block number
func (w *Web3Utils) GetBlockNumber() (uint64, error)

// GetGasPrice retrieves the current gas price
func (w *Web3Utils) GetGasPrice() (*big.Int, error)

// GetTransactionByHash retrieves transaction details
func (w *Web3Utils) GetTransactionByHash(txHash string) (*types.Transaction, bool, error)

// GetTransactionReceipt retrieves the receipt of a transaction
func (w *Web3Utils) GetTransactionReceipt(txHash string) (*types.Receipt, error)

// Close closes the Ethereum client connection
func (w *Web3Utils) Close()
```

### Cryptography Functions

```go
// GeneratePrivateKey generates a new ECDSA private key
func GeneratePrivateKey() (*ecdsa.PrivateKey, error)

// PrivateKeyToAddress converts a private key to an Ethereum address
func PrivateKeyToAddress(privateKey *ecdsa.PrivateKey) common.Address

// SignMessage signs a message with a private key
func SignMessage(message []byte, privateKey *ecdsa.PrivateKey) ([]byte, error)

// VerifySignature verifies a signature against a message and address
func VerifySignature(message []byte, signature []byte, address common.Address) bool
```

### Utility Functions

```go
// WeiToEth converts Wei to ETH
func WeiToEth(wei *big.Int) *big.Float

// EthToWei converts ETH to Wei
func EthToWei(eth *big.Float) *big.Int
```

## Unit Conversion

### Wei to ETH

```go
wei := big.NewInt(1000000000000000000) // 1 ETH in Wei
eth := WeiToEth(wei)
fmt.Printf("%.18f ETH\n", eth) // 1.000000000000000000 ETH
```

### ETH to Wei

```go
eth := big.NewFloat(1.5) // 1.5 ETH
wei := EthToWei(eth)
fmt.Printf("%s Wei\n", wei.String()) // 1500000000000000000 Wei
```

## Building

```bash
# Build for current platform
go build -o web3-utils

# Build for Linux
GOOS=linux GOARCH=amd64 go build -o web3-utils-linux

# Build for Windows
GOOS=windows GOARCH=amd64 go build -o web3-utils.exe

# Build for macOS
GOOS=darwin GOARCH=amd64 go build -o web3-utils-macos
```

## Testing

```bash
# Run tests
go test -v

# Run with coverage
go test -v -cover

# Generate coverage report
go test -coverprofile=coverage.out
go tool cover -html=coverage.out
```

## Error Handling

```go
balance, err := utils.GetBalance("invalid_address")
if err != nil {
    // Handle error
    log.Printf("Error: %v", err)
    return
}
```

## Best Practices

### 1. Always Close Connections

```go
utils, err := NewWeb3Utils(rpcURL)
if err != nil {
    log.Fatal(err)
}
defer utils.Close() // Always close
```

### 2. Use Context for Timeouts

```go
ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
defer cancel()

balance, err := client.BalanceAt(ctx, address, nil)
```

### 3. Handle Big Numbers Carefully

```go
// Use big.Int for Wei amounts
wei := big.NewInt(1000000000000000000)

// Use big.Float for ETH amounts with decimals
eth := big.NewFloat(1.5)
```

### 4. Secure Private Key Storage

```go
// NEVER hardcode private keys
// Use environment variables or secure key management
privateKeyHex := os.Getenv("PRIVATE_KEY")
```

## Performance Tips

- ✅ Reuse `ethclient.Client` instances
- ✅ Use batch requests when possible
- ✅ Cache frequently accessed data
- ✅ Use websocket connections for real-time updates

## Common Use Cases

### 1. Wallet Service

```go
// Generate new wallets for users
privateKey, _ := GeneratePrivateKey()
address := PrivateKeyToAddress(privateKey)
```

### 2. Balance Checker

```go
// Check balances for multiple addresses
for _, addr := range addresses {
    balance, _ := utils.GetBalance(addr)
    fmt.Printf("%s: %s ETH\n", addr, WeiToEth(balance))
}
```

### 3. Transaction Monitor

```go
// Monitor transaction status
receipt, _ := utils.GetTransactionReceipt(txHash)
if receipt.Status == 1 {
    fmt.Println("✅ Transaction successful")
} else {
    fmt.Println("❌ Transaction failed")
}
```

## Dependencies

- **go-ethereum**: Official Go implementation of Ethereum
- **btcd**: Bitcoin crypto primitives

## Resources

- [go-ethereum Documentation](https://geth.ethereum.org/docs/developers/dapp-developer/native)
- [Ethereum JSON-RPC API](https://ethereum.org/en/developers/docs/apis/json-rpc/)
- [Go Documentation](https://go.dev/doc/)

## License

MIT License - See LICENSE file for details
