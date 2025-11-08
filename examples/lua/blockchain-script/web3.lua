-- Lua Web3 Script
-- Lightweight blockchain interaction scripting

local http = require("socket.http")
local json = require("json")
local ltn12 = require("ltn12")

local Web3 = {}
Web3.__index = Web3

-- Constructor
function Web3:new(rpc_url)
    local instance = {
        rpc_url = rpc_url or "https://eth.llamarpc.com",
        request_id = 0
    }
    setmetatable(instance, self)
    return instance
end

-- RPC call helper
function Web3:rpc_call(method, params)
    self.request_id = self.request_id + 1

    local payload = json.encode({
        jsonrpc = "2.0",
        method = method,
        params = params or {},
        id = self.request_id
    })

    local response_body = {}

    local res, code, headers, status = http.request{
        url = self.rpc_url,
        method = "POST",
        headers = {
            ["Content-Type"] = "application/json",
            ["Content-Length"] = tostring(#payload)
        },
        source = ltn12.source.string(payload),
        sink = ltn12.sink.table(response_body)
    }

    if code ~= 200 then
        error("HTTP request failed: " .. tostring(status))
    end

    local response = json.decode(table.concat(response_body))
    return response.result
end

-- Get latest block number
function Web3:get_block_number()
    local result = self:rpc_call("eth_blockNumber")
    return tonumber(result, 16)
end

-- Get balance
function Web3:get_balance(address)
    local result = self:rpc_call("eth_getBalance", {address, "latest"})
    local wei = tonumber(result, 16)
    return wei / 1e18 -- Convert to ETH
end

-- Get gas price
function Web3:get_gas_price()
    local result = self:rpc_call("eth_gasPrice")
    local wei = tonumber(result, 16)
    return wei / 1e9 -- Convert to Gwei
end

-- Get transaction
function Web3:get_transaction(tx_hash)
    return self:rpc_call("eth_getTransactionByHash", {tx_hash})
end

-- Get block
function Web3:get_block(block_number)
    local block_hex = string.format("0x%x", block_number)
    return self:rpc_call("eth_getBlockByNumber", {block_hex, true})
end

-- Example usage
if arg[0]:match("web3.lua$") then
    print("🌙 Lua Web3 Client")
    print(string.rep("-", 40))

    local client = Web3:new()

    -- Get block number
    local block_number = client:get_block_number()
    print(string.format("📦 Block Number: %d", block_number))

    -- Get gas price
    local gas_price = client:get_gas_price()
    print(string.format("⛽ Gas Price: %.2f Gwei", gas_price))

    -- Get balance (Vitalik's address)
    local address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    local balance = client:get_balance(address)
    print(string.format("💰 Balance: %.4f ETH", balance))
end

return Web3
