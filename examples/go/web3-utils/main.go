package main

import (
	"context"
	"crypto/ecdsa"
	"fmt"
	"log"
	"math/big"

	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/common/hexutil"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/crypto"
	"github.com/ethereum/go-ethereum/ethclient"
)

const (
	// Ethereum Mainnet RPC URL
	EthereumRPC = "https://eth.llamarpc.com"
)

// Web3Utils provides utility functions for Ethereum interaction
type Web3Utils struct {
	client *ethclient.Client
}

// NewWeb3Utils creates a new Web3Utils instance
func NewWeb3Utils(rpcURL string) (*Web3Utils, error) {
	client, err := ethclient.Dial(rpcURL)
	if err != nil {
		return nil, fmt.Errorf("failed to connect to Ethereum client: %v", err)
	}

	return &Web3Utils{client: client}, nil
}

// GetBalance retrieves the balance of an address
func (w *Web3Utils) GetBalance(address string) (*big.Int, error) {
	account := common.HexToAddress(address)
	balance, err := w.client.BalanceAt(context.Background(), account, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to get balance: %v", err)
	}
	return balance, nil
}

// GetBlockNumber gets the latest block number
func (w *Web3Utils) GetBlockNumber() (uint64, error) {
	blockNumber, err := w.client.BlockNumber(context.Background())
	if err != nil {
		return 0, fmt.Errorf("failed to get block number: %v", err)
	}
	return blockNumber, nil
}

// GetGasPrice retrieves the current gas price
func (w *Web3Utils) GetGasPrice() (*big.Int, error) {
	gasPrice, err := w.client.SuggestGasPrice(context.Background())
	if err != nil {
		return nil, fmt.Errorf("failed to get gas price: %v", err)
	}
	return gasPrice, nil
}

// GeneratePrivateKey generates a new ECDSA private key
func GeneratePrivateKey() (*ecdsa.PrivateKey, error) {
	privateKey, err := crypto.GenerateKey()
	if err != nil {
		return nil, fmt.Errorf("failed to generate private key: %v", err)
	}
	return privateKey, nil
}

// PrivateKeyToAddress converts a private key to an Ethereum address
func PrivateKeyToAddress(privateKey *ecdsa.PrivateKey) common.Address {
	publicKey := privateKey.Public()
	publicKeyECDSA, ok := publicKey.(*ecdsa.PublicKey)
	if !ok {
		log.Fatal("error casting public key to ECDSA")
	}
	return crypto.PubkeyToAddress(*publicKeyECDSA)
}

// SignMessage signs a message with a private key
func SignMessage(message []byte, privateKey *ecdsa.PrivateKey) ([]byte, error) {
	hash := crypto.Keccak256Hash(message)
	signature, err := crypto.Sign(hash.Bytes(), privateKey)
	if err != nil {
		return nil, fmt.Errorf("failed to sign message: %v", err)
	}
	return signature, nil
}

// VerifySignature verifies a signature against a message and address
func VerifySignature(message []byte, signature []byte, address common.Address) bool {
	hash := crypto.Keccak256Hash(message)

	// Remove the recovery ID from signature
	if len(signature) == 65 {
		signature = signature[:64]
	}

	pubKey, err := crypto.SigToPub(hash.Bytes(), signature)
	if err != nil {
		return false
	}

	recoveredAddr := crypto.PubkeyToAddress(*pubKey)
	return recoveredAddr == address
}

// Wei converts ETH to Wei
func WeiToEth(wei *big.Int) *big.Float {
	return new(big.Float).Quo(new(big.Float).SetInt(wei), big.NewFloat(1e18))
}

// EthToWei converts Wei to ETH
func EthToWei(eth *big.Float) *big.Int {
	wei := new(big.Float).Mul(eth, big.NewFloat(1e18))
	result := new(big.Int)
	wei.Int(result)
	return result
}

// GetTransactionByHash retrieves transaction details
func (w *Web3Utils) GetTransactionByHash(txHash string) (*types.Transaction, bool, error) {
	hash := common.HexToHash(txHash)
	tx, isPending, err := w.client.TransactionByHash(context.Background(), hash)
	if err != nil {
		return nil, false, fmt.Errorf("failed to get transaction: %v", err)
	}
	return tx, isPending, nil
}

// GetTransactionReceipt retrieves the receipt of a transaction
func (w *Web3Utils) GetTransactionReceipt(txHash string) (*types.Receipt, error) {
	hash := common.HexToHash(txHash)
	receipt, err := w.client.TransactionReceipt(context.Background(), hash)
	if err != nil {
		return nil, fmt.Errorf("failed to get receipt: %v", err)
	}
	return receipt, nil
}

// Close closes the Ethereum client connection
func (w *Web3Utils) Close() {
	w.client.Close()
}

func main() {
	// Create Web3Utils instance
	utils, err := NewWeb3Utils(EthereumRPC)
	if err != nil {
		log.Fatalf("Error creating Web3Utils: %v", err)
	}
	defer utils.Close()

	fmt.Println("🔗 Web3 Go Utilities Demo")
	fmt.Println("=" + string(make([]byte, 50)))

	// Get latest block number
	blockNum, err := utils.GetBlockNumber()
	if err != nil {
		log.Printf("Error getting block number: %v", err)
	} else {
		fmt.Printf("\n📦 Latest Block: %d\n", blockNum)
	}

	// Get gas price
	gasPrice, err := utils.GetGasPrice()
	if err != nil {
		log.Printf("Error getting gas price: %v", err)
	} else {
		gasPriceGwei := new(big.Float).Quo(
			new(big.Float).SetInt(gasPrice),
			big.NewFloat(1e9),
		)
		fmt.Printf("⛽ Gas Price: %.2f Gwei\n", gasPriceGwei)
	}

	// Generate new key pair
	privateKey, err := GeneratePrivateKey()
	if err != nil {
		log.Fatalf("Error generating private key: %v", err)
	}

	address := PrivateKeyToAddress(privateKey)
	privateKeyBytes := crypto.FromECDSA(privateKey)
	privateKeyHex := hexutil.Encode(privateKeyBytes)

	fmt.Printf("\n🔑 Generated New Key Pair:\n")
	fmt.Printf("   Address: %s\n", address.Hex())
	fmt.Printf("   Private Key: %s\n", privateKeyHex)

	// Sign and verify message
	message := []byte("Hello, Web3!")
	signature, err := SignMessage(message, privateKey)
	if err != nil {
		log.Fatalf("Error signing message: %v", err)
	}

	fmt.Printf("\n✍️  Message Signature:\n")
	fmt.Printf("   Message: %s\n", string(message))
	fmt.Printf("   Signature: %s\n", hexutil.Encode(signature))

	// Verify signature
	isValid := VerifySignature(message, signature, address)
	fmt.Printf("   Valid: %v\n", isValid)

	// Example: Check Vitalik's balance
	vitalikAddress := "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
	balance, err := utils.GetBalance(vitalikAddress)
	if err != nil {
		log.Printf("Error getting balance: %v", err)
	} else {
		ethBalance := WeiToEth(balance)
		fmt.Printf("\n💰 Vitalik's Balance:\n")
		fmt.Printf("   Address: %s\n", vitalikAddress)
		fmt.Printf("   Balance: %.4f ETH\n", ethBalance)
	}
}
