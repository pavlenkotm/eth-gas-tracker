package com.web3;

import org.web3j.crypto.Credentials;
import org.web3j.crypto.ECKeyPair;
import org.web3j.crypto.Keys;
import org.web3j.protocol.Web3j;
import org.web3j.protocol.core.DefaultBlockParameterName;
import org.web3j.protocol.core.methods.response.*;
import org.web3j.protocol.http.HttpService;
import org.web3j.utils.Convert;

import java.io.IOException;
import java.math.BigDecimal;
import java.math.BigInteger;
import java.security.InvalidAlgorithmParameterException;
import java.security.NoSuchAlgorithmException;
import java.security.NoSuchProviderException;

/**
 * Web3 Service for Ethereum blockchain interaction using Web3j
 */
public class Web3Service {

    private final Web3j web3j;
    private static final String DEFAULT_RPC = "https://eth.llamarpc.com";

    public Web3Service() {
        this(DEFAULT_RPC);
    }

    public Web3Service(String rpcUrl) {
        this.web3j = Web3j.build(new HttpService(rpcUrl));
        System.out.println("✅ Connected to Ethereum node: " + rpcUrl);
    }

    /**
     * Get the latest block number
     */
    public BigInteger getBlockNumber() throws IOException {
        EthBlockNumber blockNumber = web3j.ethBlockNumber().send();
        return blockNumber.getBlockNumber();
    }

    /**
     * Get ETH balance for an address
     */
    public BigDecimal getBalance(String address) throws IOException {
        EthGetBalance balance = web3j.ethGetBalance(
            address,
            DefaultBlockParameterName.LATEST
        ).send();

        return Convert.fromWei(
            new BigDecimal(balance.getBalance()),
            Convert.Unit.ETHER
        );
    }

    /**
     * Get current gas price in Gwei
     */
    public BigDecimal getGasPrice() throws IOException {
        EthGasPrice gasPrice = web3j.ethGasPrice().send();
        return Convert.fromWei(
            new BigDecimal(gasPrice.getGasPrice()),
            Convert.Unit.GWEI
        );
    }

    /**
     * Get transaction by hash
     */
    public EthTransaction getTransaction(String txHash) throws IOException {
        return web3j.ethGetTransactionByHash(txHash).send();
    }

    /**
     * Get transaction receipt
     */
    public EthGetTransactionReceipt getTransactionReceipt(String txHash) throws IOException {
        return web3j.ethGetTransactionReceipt(txHash).send();
    }

    /**
     * Generate a new Ethereum key pair
     */
    public static Credentials generateKeyPair()
            throws InvalidAlgorithmParameterException,
                   NoSuchAlgorithmException,
                   NoSuchProviderException {
        ECKeyPair keyPair = Keys.createEcKeyPair();
        return Credentials.create(keyPair);
    }

    /**
     * Get client version
     */
    public String getClientVersion() throws IOException {
        Web3ClientVersion clientVersion = web3j.web3ClientVersion().send();
        return clientVersion.getWeb3ClientVersion();
    }

    /**
     * Check if address is valid
     */
    public static boolean isValidAddress(String address) {
        return address != null && address.matches("^0x[0-9a-fA-F]{40}$");
    }

    /**
     * Get syncing status
     */
    public EthSyncing getSyncingStatus() throws IOException {
        return web3j.ethSyncing().send();
    }

    /**
     * Get network ID
     */
    public BigInteger getNetworkId() throws IOException {
        EthChainId chainId = web3j.ethChainId().send();
        return chainId.getChainId();
    }

    /**
     * Close the Web3j connection
     */
    public void close() {
        web3j.shutdown();
        System.out.println("✅ Connection closed");
    }

    /**
     * Main method for demonstration
     */
    public static void main(String[] args) {
        Web3Service service = new Web3Service();

        try {
            System.out.println("\n🔗 Web3j Integration Demo");
            System.out.println("=".repeat(50));

            // Get latest block
            BigInteger blockNumber = service.getBlockNumber();
            System.out.println("\n📦 Latest Block: " + blockNumber);

            // Get gas price
            BigDecimal gasPrice = service.getGasPrice();
            System.out.println("⛽ Gas Price: " + gasPrice + " Gwei");

            // Get network ID
            BigInteger networkId = service.getNetworkId();
            System.out.println("🌐 Network ID: " + networkId);

            // Generate new key pair
            Credentials credentials = generateKeyPair();
            System.out.println("\n🔑 Generated New Wallet:");
            System.out.println("   Address: " + credentials.getAddress());
            System.out.println("   Private Key: " + credentials.getEcKeyPair().getPrivateKey().toString(16));

            // Check Vitalik's balance
            String vitalikAddress = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";
            BigDecimal balance = service.getBalance(vitalikAddress);
            System.out.println("\n💰 Vitalik's Balance:");
            System.out.println("   Address: " + vitalikAddress);
            System.out.println("   Balance: " + balance + " ETH");

            // Validate address
            System.out.println("\n✅ Address Validation:");
            System.out.println("   Valid: " + isValidAddress(vitalikAddress));
            System.out.println("   Invalid: " + isValidAddress("0xinvalid"));

        } catch (Exception e) {
            System.err.println("❌ Error: " + e.getMessage());
            e.printStackTrace();
        } finally {
            service.close();
        }
    }
}
