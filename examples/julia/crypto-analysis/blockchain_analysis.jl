"""
    BlockchainAnalysis

Julia module for high-performance blockchain data analysis.
Leverages Julia's speed for crypto analytics and quantitative research.
"""
module BlockchainAnalysis

using HTTP
using JSON3
using Statistics
using DataFrames
using Plots

export Web3Client, analyze_gas_prices, plot_block_times

"""
    Web3Client

Ethereum RPC client for blockchain data retrieval.
"""
struct Web3Client
    rpc_url::String
    request_id::Ref{Int}

    function Web3Client(rpc_url="https://eth.llamarpc.com")
        new(rpc_url, Ref(0))
    end
end

"""
    rpc_call(client, method, params)

Make JSON-RPC call to Ethereum node.
"""
function rpc_call(client::Web3Client, method::String, params::Vector=[])
    client.request_id[] += 1

    payload = Dict(
        "jsonrpc" => "2.0",
        "method" => method,
        "params" => params,
        "id" => client.request_id[]
    )

    response = HTTP.post(
        client.rpc_url,
        ["Content-Type" => "application/json"],
        JSON3.write(payload)
    )

    result = JSON3.read(String(response.body))
    return result.result
end

"""
    get_block_number(client)

Get latest block number.
"""
function get_block_number(client::Web3Client)
    result = rpc_call(client, "eth_blockNumber")
    return parse(Int, result, base=16)
end

"""
    get_balance(client, address)

Get balance of address in ETH.
"""
function get_balance(client::Web3Client, address::String)
    result = rpc_call(client, "eth_getBalance", [address, "latest"])
    wei = parse(BigInt, result, base=16)
    return wei / 1e18
end

"""
    get_gas_price(client)

Get current gas price in Gwei.
"""
function get_gas_price(client::Web3Client)
    result = rpc_call(client, "eth_gasPrice")
    wei = parse(Int, result, base=16)
    return wei / 1e9
end

"""
    get_block(client, number)

Get block by number.
"""
function get_block(client::Web3Client, number::Int)
    block_hex = string("0x", string(number, base=16))
    return rpc_call(client, "eth_getBlockByNumber", [block_hex, true])
end

"""
    analyze_gas_prices(client, num_blocks)

Analyze gas prices over recent blocks.
Returns statistical summary.
"""
function analyze_gas_prices(client::Web3Client, num_blocks::Int=100)
    latest = get_block_number(client)
    gas_prices = Float64[]

    println("📊 Analyzing gas prices over $num_blocks blocks...")

    for i in (latest-num_blocks+1):latest
        try
            block = get_block(client, i)
            if haskey(block, :gasUsed) && haskey(block, :baseFeePerGas)
                base_fee = parse(Int, block.baseFeePerGas, base=16) / 1e9
                push!(gas_prices, base_fee)
            end
        catch e
            @warn "Failed to fetch block $i: $e"
        end
    end

    return Dict(
        "mean" => mean(gas_prices),
        "median" => median(gas_prices),
        "std" => std(gas_prices),
        "min" => minimum(gas_prices),
        "max" => maximum(gas_prices),
        "samples" => length(gas_prices)
    )
end

"""
    plot_block_times(client, num_blocks)

Plot block production times.
"""
function plot_block_times(client::Web3Client, num_blocks::Int=50)
    latest = get_block_number(client)
    timestamps = Int[]
    block_numbers = Int[]

    println("📈 Fetching block times...")

    for i in (latest-num_blocks+1):latest
        block = get_block(client, i)
        timestamp = parse(Int, block.timestamp, base=16)
        push!(timestamps, timestamp)
        push!(block_numbers, i)
    end

    # Calculate block times
    block_times = diff(timestamps)

    # Create plot
    p = plot(block_numbers[2:end], block_times,
        xlabel="Block Number",
        ylabel="Block Time (seconds)",
        title="Ethereum Block Times",
        legend=false,
        linewidth=2)

    return p
end

end # module

# Example usage
if abspath(PROGRAM_FILE) == @__FILE__
    using .BlockchainAnalysis

    println("🔬 Julia Blockchain Analysis")
    println("="^50)

    client = Web3Client()

    # Basic queries
    block = get_block_number(client)
    println("📦 Block Number: $(block)")

    gas = get_gas_price(client)
    println("⛽ Gas Price: $(round(gas, digits=2)) Gwei")

    # Statistical analysis
    stats = analyze_gas_prices(client, 20)
    println("\n📊 Gas Price Statistics:")
    println("  Mean: $(round(stats["mean"], digits=2)) Gwei")
    println("  Median: $(round(stats["median"], digits=2)) Gwei")
    println("  Std Dev: $(round(stats["std"], digits=2)) Gwei")
    println("  Range: $(round(stats["min"], digits=2)) - $(round(stats["max"], digits=2)) Gwei")
end
