#!/usr/bin/env dub
/+ dub.sdl:
    name "web3_client"
    dependency "vibe-d" version="~>0.9.0"
+/

/// D Web3 Client - High-performance blockchain interactions
module web3_client;

import vibe.d;
import std.stdio;
import std.conv;
import std.json;
import std.algorithm;
import std.string;

class Web3Client
{
    private string rpcUrl;
    private int requestId;

    this(string rpcUrl = "https://eth.llamarpc.com")
    {
        this.rpcUrl = rpcUrl;
        this.requestId = 0;
    }

    private JSONValue rpcCall(string method, JSONValue[] params = [])
    {
        this.requestId++;

        auto payload = JSONValue([
            "jsonrpc": JSONValue("2.0"),
            "method": JSONValue(method),
            "params": JSONValue(params),
            "id": JSONValue(this.requestId)
        ]);

        auto response = requestHTTP(this.rpcUrl,
            (scope req) {
                req.method = HTTPMethod.POST;
                req.contentType = "application/json";
                req.writeJsonBody(payload);
            },
            (scope res) {
                return res.readJson();
            }
        );

        if ("error" in response)
            throw new Exception("RPC error: " ~ response["error"].toString());

        return response["result"];
    }

    private long hexToInt(string hex)
    {
        if (hex.startsWith("0x"))
            hex = hex[2..$];
        return hex.to!long(16);
    }

    private double weiToEther(long wei)
    {
        return wei / 1e18;
    }

    private double weiToGwei(long wei)
    {
        return wei / 1e9;
    }

    long getBlockNumber()
    {
        auto result = rpcCall("eth_blockNumber");
        return hexToInt(result.str);
    }

    double getBalance(string address)
    {
        auto result = rpcCall("eth_getBalance", [JSONValue(address), JSONValue("latest")]);
        auto wei = hexToInt(result.str);
        return weiToEther(wei);
    }

    double getGasPrice()
    {
        auto result = rpcCall("eth_gasPrice");
        auto wei = hexToInt(result.str);
        return weiToGwei(wei);
    }

    JSONValue getTransaction(string txHash)
    {
        return rpcCall("eth_getTransactionByHash", [JSONValue(txHash)]);
    }
}

void main()
{
    writeln("🔷 D Web3 Client");
    writeln("-".repeat(40));

    auto client = new Web3Client();

    try
    {
        auto blockNum = client.getBlockNumber();
        writefln("📦 Block Number: %d", blockNum);

        auto gas = client.getGasPrice();
        writefln("⛽ Gas Price: %.2f Gwei", gas);

        auto address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045";
        auto balance = client.getBalance(address);
        writefln("💰 Balance: %.4f ETH", balance);
    }
    catch (Exception e)
    {
        writefln("❌ Error: %s", e.msg);
    }
}
