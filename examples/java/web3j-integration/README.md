# ☕ Web3j Integration - Java Ethereum Client

Professional **Ethereum integration** using **Web3j**, the most popular Java library for blockchain interaction.

## Features

- 🔗 **Ethereum RPC Client**: Connect to any Ethereum node
- 💰 **Balance Queries**: Check ETH balances
- ⛽ **Gas Price**: Get current network gas prices
- 🔑 **Wallet Generation**: Create new Ethereum wallets
- 📦 **Block Data**: Query blockchain information
- 📝 **Transactions**: Monitor and query transactions
- ✅ **Address Validation**: Validate Ethereum addresses

## Prerequisites

- Java 17 or higher
- Maven 3.6+

## Installation & Build

```bash
# Navigate to project directory
cd examples/java/web3j-integration

# Install dependencies and build
mvn clean install

# Run the application
mvn exec:java -Dexec.mainClass="com.web3.Web3Service"

# Or run the JAR
java -jar target/web3j-integration-1.0.0.jar
```

## Usage Examples

### Initialize Web3Service

```java
// Connect to default RPC
Web3Service service = new Web3Service();

// Connect to custom RPC
Web3Service service = new Web3Service("https://your-rpc-url.com");
```

### Get Latest Block Number

```java
BigInteger blockNumber = service.getBlockNumber();
System.out.println("Latest block: " + blockNumber);
```

### Check Account Balance

```java
String address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";
BigDecimal balance = service.getBalance(address);
System.out.println("Balance: " + balance + " ETH");
```

### Get Gas Price

```java
BigDecimal gasPrice = service.getGasPrice();
System.out.println("Gas price: " + gasPrice + " Gwei");
```

### Generate New Wallet

```java
Credentials credentials = Web3Service.generateKeyPair();
String address = credentials.getAddress();
String privateKey = credentials.getEcKeyPair().getPrivateKey().toString(16);

System.out.println("Address: " + address);
System.out.println("Private Key: " + privateKey);
```

### Get Transaction Details

```java
String txHash = "0x...";
EthTransaction transaction = service.getTransaction(txHash);

if (transaction.getTransaction().isPresent()) {
    Transaction tx = transaction.getTransaction().get();
    System.out.println("From: " + tx.getFrom());
    System.out.println("To: " + tx.getTo());
    System.out.println("Value: " + tx.getValue());
}
```

### Get Transaction Receipt

```java
EthGetTransactionReceipt receipt = service.getTransactionReceipt(txHash);

if (receipt.getTransactionReceipt().isPresent()) {
    TransactionReceipt txReceipt = receipt.getTransactionReceipt().get();
    System.out.println("Status: " + txReceipt.getStatus());
    System.out.println("Gas Used: " + txReceipt.getGasUsed());
}
```

### Validate Address

```java
boolean isValid = Web3Service.isValidAddress("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045");
System.out.println("Valid address: " + isValid);
```

## API Reference

### Web3Service Methods

| Method | Return Type | Description |
|--------|-------------|-------------|
| `getBlockNumber()` | `BigInteger` | Get latest block number |
| `getBalance(String)` | `BigDecimal` | Get ETH balance in ETH |
| `getGasPrice()` | `BigDecimal` | Get gas price in Gwei |
| `getTransaction(String)` | `EthTransaction` | Get transaction by hash |
| `getTransactionReceipt(String)` | `EthGetTransactionReceipt` | Get transaction receipt |
| `generateKeyPair()` | `Credentials` | Generate new wallet |
| `getClientVersion()` | `String` | Get node client version |
| `getSyncingStatus()` | `EthSyncing` | Get sync status |
| `getNetworkId()` | `BigInteger` | Get network/chain ID |
| `isValidAddress(String)` | `boolean` | Validate Ethereum address |
| `close()` | `void` | Close connection |

## Unit Conversion

Web3j provides built-in conversion utilities:

```java
import org.web3j.utils.Convert;

// Wei to ETH
BigDecimal eth = Convert.fromWei("1000000000000000000", Convert.Unit.ETHER);

// ETH to Wei
BigDecimal wei = Convert.toWei("1.5", Convert.Unit.ETHER);

// Wei to Gwei
BigDecimal gwei = Convert.fromWei("1000000000", Convert.Unit.GWEI);
```

## Error Handling

```java
try {
    BigInteger blockNumber = service.getBlockNumber();
    System.out.println("Block: " + blockNumber);
} catch (IOException e) {
    System.err.println("RPC Error: " + e.getMessage());
} catch (Exception e) {
    System.err.println("Unexpected error: " + e.getMessage());
}
```

## Maven Dependencies

```xml
<dependency>
    <groupId>org.web3j</groupId>
    <artifactId>core</artifactId>
    <version>4.10.3</version>
</dependency>
```

## Smart Contract Interaction

### Generate Contract Wrappers

```bash
# Install Web3j CLI
curl -L get.web3j.io | sh

# Generate Java wrapper from ABI
web3j generate solidity \
    -a path/to/contract.abi \
    -b path/to/contract.bin \
    -o src/main/java \
    -p com.web3.contracts
```

### Load and Call Contract

```java
// Load contract
YourContract contract = YourContract.load(
    contractAddress,
    web3j,
    credentials,
    new DefaultGasProvider()
);

// Read function
BigInteger value = contract.getValue().send();

// Write function
TransactionReceipt receipt = contract.setValue(BigInteger.valueOf(42)).send();
```

## Testing

```bash
# Run tests
mvn test

# Run with coverage
mvn clean test jacoco:report
```

## Building for Production

```bash
# Create executable JAR
mvn clean package

# Run the JAR
java -jar target/web3j-integration-1.0.0.jar
```

## Android Integration

Web3j works on Android! Add to `build.gradle`:

```gradle
dependencies {
    implementation 'org.web3j:core:4.10.3:android'
}
```

## Performance Tips

- ✅ Reuse `Web3j` instances
- ✅ Use connection pooling for multiple requests
- ✅ Cache frequently accessed data
- ✅ Use batch requests when possible

## Common Use Cases

### 1. Wallet Application

```java
// Create wallet
Credentials wallet = Web3Service.generateKeyPair();

// Check balance
BigDecimal balance = service.getBalance(wallet.getAddress());

// Send transaction
// (Requires gas and nonce management)
```

### 2. Payment Gateway

```java
// Monitor incoming transactions
// Check transaction confirmations
TransactionReceipt receipt = service.getTransactionReceipt(txHash)
    .getTransactionReceipt().orElseThrow();

if (receipt.getStatus().equals("0x1")) {
    // Payment successful
}
```

### 3. DApp Backend

```java
// Query smart contract state
// Process events
// Execute transactions
```

## Resources

- [Web3j Documentation](https://docs.web3j.io/)
- [Web3j GitHub](https://github.com/web3j/web3j)
- [Ethereum JSON-RPC](https://ethereum.org/en/developers/docs/apis/json-rpc/)
- [Maven Central](https://search.maven.org/artifact/org.web3j/core)

## License

MIT License - See LICENSE file for details
