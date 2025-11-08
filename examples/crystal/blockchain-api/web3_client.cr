# Crystal Web3 Client
# Ruby-inspired syntax with C-level performance for blockchain APIs

require "http/client"
require "json"

class Web3Client
  property rpc_url : String
  property request_id : Int32

  def initialize(@rpc_url : String = "https://eth.llamarpc.com")
    @request_id = 0
  end

  private def rpc_call(method : String, params : Array = [] of JSON::Any) : JSON::Any
    @request_id += 1

    payload = {
      jsonrpc: "2.0",
      method: method,
      params: params,
      id: @request_id
    }

    response = HTTP::Client.post(
      @rpc_url,
      headers: HTTP::Headers{"Content-Type" => "application/json"},
      body: payload.to_json
    )

    raise "HTTP error: #{response.status_code}" unless response.status_code == 200

    result = JSON.parse(response.body)
    raise "RPC error: #{result["error"]}" if result["error"]?

    result["result"]
  end

  private def hex_to_int(hex : String | JSON::Any) : Int64
    hex_str = hex.is_a?(JSON::Any) ? hex.as_s : hex
    hex_str.lchop("0x").to_i64(16)
  end

  private def wei_to_ether(wei : Int64) : Float64
    wei.to_f / 1e18
  end

  private def wei_to_gwei(wei : Int64) : Float64
    wei.to_f / 1e9
  end

  def get_block_number : Int64
    result = rpc_call("eth_blockNumber")
    hex_to_int(result)
  end

  def get_balance(address : String) : Float64
    result = rpc_call("eth_getBalance", [JSON::Any.new(address), JSON::Any.new("latest")])
    wei = hex_to_int(result)
    wei_to_ether(wei)
  end

  def get_gas_price : Float64
    result = rpc_call("eth_gasPrice")
    wei = hex_to_int(result)
    wei_to_gwei(wei)
  end

  def get_transaction(tx_hash : String) : JSON::Any
    rpc_call("eth_getTransactionByHash", [JSON::Any.new(tx_hash)])
  end

  def get_block(block_number : Int64) : JSON::Any
    block_hex = "0x#{block_number.to_s(16)}"
    rpc_call("eth_getBlockByNumber", [JSON::Any.new(block_hex), JSON::Any.new(true)])
  end
end

# Example usage
if PROGRAM_NAME == __FILE__
  puts "💎 Crystal Web3 Client"
  puts "-" * 40

  client = Web3Client.new

  begin
    block = client.get_block_number
    puts "📦 Block Number: #{block}"

    gas = client.get_gas_price
    puts "⛽ Gas Price: #{"%.2f" % gas} Gwei"

    address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    balance = client.get_balance(address)
    puts "💰 Balance: #{"%.4f" % balance} ETH"

  rescue ex
    puts "❌ Error: #{ex.message}"
  end
end
