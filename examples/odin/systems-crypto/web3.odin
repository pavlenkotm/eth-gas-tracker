package web3

import "core:fmt"
import "core:net"
import "core:encoding/json"
import "core:strings"
import "core:strconv"

// Odin Web3 Client - Systems programming for blockchain
Web3_Client :: struct {
    rpc_url: string,
    request_id: int,
}

make_web3_client :: proc(rpc_url := "https://eth.llamarpc.com") -> Web3_Client {
    return Web3_Client{rpc_url = rpc_url, request_id = 0}
}

rpc_call :: proc(client: ^Web3_Client, method: string, params: []json.Value = nil) -> (json.Value, bool) {
    client.request_id += 1

    payload := json.Object{
        "jsonrpc" = json.String("2.0"),
        "method" = json.String(method),
        "params" = json.Array(params),
        "id" = json.Integer(client.request_id),
    }

    // Note: Simplified - actual HTTP implementation would go here
    fmt.println("RPC Call:", method)

    // Return dummy result for compilation
    return json.Null{}, true
}

hex_to_int :: proc(hex: string) -> (i64, bool) {
    hex_stripped := strings.trim_prefix(hex, "0x")
    return strconv.parse_i64(hex_stripped, 16)
}

wei_to_ether :: proc(wei: i64) -> f64 {
    return f64(wei) / 1e18
}

wei_to_gwei :: proc(wei: i64) -> f64 {
    return f64(wei) / 1e9
}

get_block_number :: proc(client: ^Web3_Client) -> (i64, bool) {
    result, ok := rpc_call(client, "eth_blockNumber")
    if !ok do return 0, false

    hex_str, str_ok := result.(json.String)
    if !str_ok do return 0, false

    return hex_to_int(string(hex_str))
}

get_balance :: proc(client: ^Web3_Client, address: string) -> (f64, bool) {
    params := []json.Value{json.String(address), json.String("latest")}
    result, ok := rpc_call(client, "eth_getBalance", params)
    if !ok do return 0, false

    hex_str, str_ok := result.(json.String)
    if !str_ok do return 0, false

    wei, int_ok := hex_to_int(string(hex_str))
    if !int_ok do return 0, false

    return wei_to_ether(wei), true
}

main :: proc() {
    fmt.println("⚙️  Odin Web3 Client")
    fmt.println(strings.repeat("-", 40))

    client := make_web3_client()

    block, block_ok := get_block_number(&client)
    if block_ok {
        fmt.printf("📦 Block Number: %d\n", block)
    }

    address := "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    balance, bal_ok := get_balance(&client, address)
    if bal_ok {
        fmt.printf("💰 Balance: %.4f ETH\n", balance)
    }
}
