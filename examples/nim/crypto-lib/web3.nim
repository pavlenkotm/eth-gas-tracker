# Nim Web3 Client
# Systems programming for blockchain with expressive syntax

import httpclient, json, strutils, math

type
  Web3Client* = object
    rpcUrl*: string
    requestId*: int

proc newWeb3Client*(rpcUrl = "https://eth.llamarpc.com"): Web3Client =
  Web3Client(rpcUrl: rpcUrl, requestId: 0)

proc rpcCall(client: var Web3Client, `method`: string, params: JsonNode = newJArray()): JsonNode =
  client.requestId.inc

  let payload = %* {
    "jsonrpc": "2.0",
    "method": `method`,
    "params": params,
    "id": client.requestId
  }

  var httpClient = newHttpClient()
  httpClient.headers = newHttpHeaders({"Content-Type": "application/json"})

  let response = httpClient.postContent(client.rpcUrl, $payload)
  let jsonResponse = parseJson(response)

  if jsonResponse.hasKey("error"):
    raise newException(IOError, "RPC error: " & $jsonResponse["error"])

  return jsonResponse["result"]

proc hexToInt(hex: string): int64 =
  return parseBiggestInt(hex, 16)

proc weiToEther(wei: int64): float =
  return float(wei) / 1e18

proc weiToGwei(wei: int64): float =
  return float(wei) / 1e9

proc getBlockNumber*(client: var Web3Client): int64 =
  let result = client.rpcCall("eth_blockNumber")
  return hexToInt(result.getStr)

proc getBalance*(client: var Web3Client, address: string): float =
  let result = client.rpcCall("eth_getBalance", %* [address, "latest"])
  let wei = hexToInt(result.getStr)
  return weiToEther(wei)

proc getGasPrice*(client: var Web3Client): float =
  let result = client.rpcCall("eth_gasPrice")
  let wei = hexToInt(result.getStr)
  return weiToGwei(wei)

proc getTransaction*(client: var Web3Client, txHash: string): JsonNode =
  return client.rpcCall("eth_getTransactionByHash", %* [txHash])

when isMainModule:
  echo "👑 Nim Web3 Client"
  echo repeat('-', 40)

  var client = newWeb3Client()

  try:
    let blockNum = client.getBlockNumber()
    echo "📦 Block Number: ", blockNum

    let gas = client.getGasPrice()
    echo "⛽ Gas Price: ", formatFloat(gas, ffDecimal, 2), " Gwei"

    let address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    let balance = client.getBalance(address)
    echo "💰 Balance: ", formatFloat(balance, ffDecimal, 4), " ETH"

  except IOError as e:
    echo "❌ Error: ", e.msg
