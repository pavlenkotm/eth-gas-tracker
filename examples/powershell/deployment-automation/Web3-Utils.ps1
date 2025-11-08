# PowerShell Web3 Utilities
# Enterprise-grade blockchain automation and deployment

class Web3Client {
    [string]$RpcUrl
    [int]$RequestId

    Web3Client([string]$rpcUrl = "https://eth.llamarpc.com") {
        $this.RpcUrl = $rpcUrl
        $this.RequestId = 0
    }

    [object] RpcCall([string]$method, [array]$params) {
        $this.RequestId++

        $payload = @{
            jsonrpc = "2.0"
            method = $method
            params = $params
            id = $this.RequestId
        } | ConvertTo-Json -Depth 10

        try {
            $response = Invoke-RestMethod `
                -Uri $this.RpcUrl `
                -Method Post `
                -Body $payload `
                -ContentType "application/json"

            if ($response.error) {
                throw "RPC Error: $($response.error.message)"
            }

            return $response.result
        }
        catch {
            Write-Error "Request failed: $_"
            throw
        }
    }

    [long] HexToInt([string]$hex) {
        return [Convert]::ToInt64($hex, 16)
    }

    [double] WeiToEther([long]$wei) {
        return $wei / 1e18
    }

    [double] WeiToGwei([long]$wei) {
        return $wei / 1e9
    }

    [long] GetBlockNumber() {
        $result = $this.RpcCall("eth_blockNumber", @())
        return $this.HexToInt($result)
    }

    [double] GetBalance([string]$address) {
        $result = $this.RpcCall("eth_getBalance", @($address, "latest"))
        $wei = $this.HexToInt($result)
        return $this.WeiToEther($wei)
    }

    [double] GetGasPrice() {
        $result = $this.RpcCall("eth_gasPrice", @())
        $wei = $this.HexToInt($result)
        return $this.WeiToGwei($wei)
    }

    [object] GetTransaction([string]$txHash) {
        return $this.RpcCall("eth_getTransactionByHash", @($txHash))
    }

    [object] GetBlock([long]$blockNumber) {
        $blockHex = "0x{0:X}" -f $blockNumber
        return $this.RpcCall("eth_getBlockByNumber", @($blockHex, $true))
    }
}

function Get-EthBlockNumber {
    <#
    .SYNOPSIS
    Get latest Ethereum block number
    #>
    $client = [Web3Client]::new()
    return $client.GetBlockNumber()
}

function Get-EthBalance {
    <#
    .SYNOPSIS
    Get ETH balance of address
    #>
    param(
        [Parameter(Mandatory=$true)]
        [string]$Address
    )

    $client = [Web3Client]::new()
    return $client.GetBalance($Address)
}

function Get-EthGasPrice {
    <#
    .SYNOPSIS
    Get current gas price in Gwei
    #>
    $client = [Web3Client]::new()
    return $client.GetGasPrice()
}

# Example usage
if ($MyInvocation.InvocationName -ne '.') {
    Write-Host "⚡ PowerShell Web3 Utils" -ForegroundColor Cyan
    Write-Host ("-" * 40)

    try {
        $client = [Web3Client]::new()

        $block = $client.GetBlockNumber()
        Write-Host "📦 Block Number: $($block.ToString('N0'))" -ForegroundColor Green

        $gas = $client.GetGasPrice()
        Write-Host "⛽ Gas Price: $([math]::Round($gas, 2)) Gwei" -ForegroundColor Yellow

        $address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
        $balance = $client.GetBalance($address)
        Write-Host "💰 Balance: $([math]::Round($balance, 4)) ETH" -ForegroundColor Magenta
    }
    catch {
        Write-Host "❌ Error: $_" -ForegroundColor Red
    }
}

Export-ModuleMember -Function Get-EthBlockNumber, Get-EthBalance, Get-EthGasPrice
