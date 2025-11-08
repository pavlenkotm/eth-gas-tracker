// F# Web3 Client - Functional blockchain analytics
module Web3Client

open System
open System.Net.Http
open System.Text
open System.Text.Json
open System.Numerics

type RpcRequest = {
    jsonrpc: string
    method: string
    params: obj[]
    id: int
}

type RpcResponse<'T> = {
    jsonrpc: string
    result: 'T option
    error: JsonElement option
    id: int
}

type Web3Client(rpcUrl: string) =
    let mutable requestId = 0
    let httpClient = new HttpClient()

    member private _.RpcCall<'T>(method: string, [<ParamArray>] params: obj[]) : Async<'T> =
        async {
            requestId <- requestId + 1

            let payload = {
                jsonrpc = "2.0"
                method = method
                params = params
                id = requestId
            }

            let json = JsonSerializer.Serialize(payload)
            let content = new StringContent(json, Encoding.UTF8, "application/json")

            let! response = httpClient.PostAsync(rpcUrl, content) |> Async.AwaitTask
            let! body = response.Content.ReadAsStringAsync() |> Async.AwaitTask

            if not response.IsSuccessStatusCode then
                failwithf "HTTP error: %d" (int response.StatusCode)

            let result = JsonSerializer.Deserialize<RpcResponse<'T>>(body)

            match result.result with
            | Some r -> return r
            | None -> return failwith "RPC error"
        }

    member private _.HexToInt(hex: string) : bigint =
        BigInteger.Parse(hex.Replace("0x", ""), Globalization.NumberStyles.HexNumber)

    member private _.WeiToEther(wei: bigint) : decimal =
        decimal wei / 1_000_000_000_000_000_000m

    member private _.WeiToGwei(wei: bigint) : decimal =
        decimal wei / 1_000_000_000m

    member this.GetBlockNumberAsync() : Async<bigint> =
        async {
            let! result = this.RpcCall<string>("eth_blockNumber")
            return this.HexToInt(result)
        }

    member this.GetBalanceAsync(address: string) : Async<decimal> =
        async {
            let! result = this.RpcCall<string>("eth_getBalance", address, "latest")
            let wei = this.HexToInt(result)
            return this.WeiToEther(wei)
        }

    member this.GetGasPriceAsync() : Async<decimal> =
        async {
            let! result = this.RpcCall<string>("eth_gasPrice")
            let wei = this.HexToInt(result)
            return this.WeiToGwei(wei)
        }

    member this.GetTransactionAsync(txHash: string) : Async<JsonElement> =
        this.RpcCall<JsonElement>("eth_getTransactionByHash", txHash)

[<EntryPoint>]
let main argv =
    printfn "🔷 F# Web3 Client"
    printfn "%s" (String.replicate 40 "-")

    let client = Web3Client("https://eth.llamarpc.com")

    try
        // Get block number
        let block = client.GetBlockNumberAsync() |> Async.RunSynchronously
        printfn "📦 Block Number: %A" block

        // Get gas price
        let gas = client.GetGasPriceAsync() |> Async.RunSynchronously
        printfn "⛽ Gas Price: %.2f Gwei" gas

        // Get balance
        let address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
        let balance = client.GetBalanceAsync(address) |> Async.RunSynchronously
        printfn "💰 Balance: %.4f ETH" balance

        0
    with
    | ex ->
        printfn "❌ Error: %s" ex.Message
        1
