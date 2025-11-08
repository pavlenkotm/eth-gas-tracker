<?php

/**
 * PHP Web3 Client for Ethereum
 * Server-side blockchain interactions for Web3 backends
 */
class Web3Client
{
    private string $rpcUrl;
    private int $requestId = 0;

    public function __construct(string $rpcUrl = 'https://eth.llamarpc.com')
    {
        $this->rpcUrl = $rpcUrl;
    }

    /**
     * Make JSON-RPC call to Ethereum node
     */
    private function rpcCall(string $method, array $params = []): mixed
    {
        $this->requestId++;

        $payload = json_encode([
            'jsonrpc' => '2.0',
            'method' => $method,
            'params' => $params,
            'id' => $this->requestId
        ]);

        $ch = curl_init($this->rpcUrl);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);

        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);

        if ($httpCode !== 200) {
            throw new Exception("HTTP error: $httpCode");
        }

        $result = json_decode($response, true);

        if (isset($result['error'])) {
            throw new Exception("RPC error: " . $result['error']['message']);
        }

        return $result['result'];
    }

    private function hexToInt(string $hex): int|string
    {
        return gmp_strval(gmp_init($hex, 16), 10);
    }

    private function weiToEther(string $wei): float
    {
        return (float)bcdiv($wei, '1000000000000000000', 18);
    }

    private function weiToGwei(string $wei): float
    {
        return (float)bcdiv($wei, '1000000000', 9);
    }

    public function getBlockNumber(): int
    {
        $result = $this->rpcCall('eth_blockNumber');
        return (int)$this->hexToInt($result);
    }

    public function getBalance(string $address): float
    {
        $result = $this->rpcCall('eth_getBalance', [$address, 'latest']);
        $wei = $this->hexToInt($result);
        return $this->weiToEther($wei);
    }

    public function getGasPrice(): float
    {
        $result = $this->rpcCall('eth_gasPrice');
        $wei = $this->hexToInt($result);
        return $this->weiToGwei($wei);
    }

    public function getTransaction(string $txHash): array
    {
        return $this->rpcCall('eth_getTransactionByHash', [$txHash]);
    }

    public function getBlock(int $blockNumber): array
    {
        $blockHex = '0x' . dechex($blockNumber);
        return $this->rpcCall('eth_getBlockByNumber', [$blockHex, true]);
    }

    public function call(string $to, string $data, ?string $from = null): string
    {
        $params = [
            'to' => $to,
            'data' => $data
        ];

        if ($from !== null) {
            $params['from'] = $from;
        }

        return $this->rpcCall('eth_call', [$params, 'latest']);
    }
}

// Example usage
if (php_sapi_name() === 'cli') {
    echo "🐘 PHP Web3 Client\n";
    echo str_repeat('-', 40) . "\n";

    $client = new Web3Client();

    try {
        $block = $client->getBlockNumber();
        echo "📦 Block Number: " . number_format($block) . "\n";

        $gas = $client->getGasPrice();
        echo "⛽ Gas Price: " . round($gas, 2) . " Gwei\n";

        $address = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045';
        $balance = $client->getBalance($address);
        echo "💰 Balance: " . number_format($balance, 4) . " ETH\n";

    } catch (Exception $e) {
        echo "❌ Error: " . $e->getMessage() . "\n";
    }
}
