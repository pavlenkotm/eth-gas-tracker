%% Erlang Web3 Client - Distributed blockchain node communication
-module(web3_client).
-export([start/0, get_block_number/0, get_balance/1, get_gas_price/0]).

-define(RPC_URL, "https://eth.llamarpc.com").

start() ->
    application:ensure_all_started(inets),
    application:ensure_all_started(ssl),
    ok.

rpc_call(Method, Params) ->
    Payload = jsx:encode(#{
        <<"jsonrpc">> => <<"2.0">>,
        <<"method">> => list_to_binary(Method),
        <<"params">> => Params,
        <<"id">> => 1
    }),

    {ok, {{_, 200, _}, _, Body}} = httpc:request(
        post,
        {?RPC_URL, [], "application/json", Payload},
        [],
        []
    ),

    Result = jsx:decode(list_to_binary(Body)),
    maps:get(<<"result">>, Result).

hex_to_int(<<"0x", Hex/binary>>) ->
    binary_to_integer(Hex, 16).

wei_to_ether(Wei) ->
    Wei / 1.0e18.

wei_to_gwei(Wei) ->
    Wei / 1.0e9.

get_block_number() ->
    Result = rpc_call("eth_blockNumber", []),
    hex_to_int(Result).

get_balance(Address) ->
    Result = rpc_call("eth_getBalance", [list_to_binary(Address), <<"latest">>]),
    Wei = hex_to_int(Result),
    wei_to_ether(Wei).

get_gas_price() ->
    Result = rpc_call("eth_gasPrice", []),
    Wei = hex_to_int(Result),
    wei_to_gwei(Wei).
