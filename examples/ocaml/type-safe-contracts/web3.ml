(* OCaml Web3 - Type-safe blockchain interactions *)

open Lwt.Infix

module Web3 = struct
  type t = { rpc_url: string; mutable request_id: int }

  let create ?(rpc_url = "https://eth.llamarpc.com") () =
    { rpc_url; request_id = 0 }

  let rpc_call client method_name params =
    client.request_id <- client.request_id + 1;

    let payload = `Assoc [
      ("jsonrpc", `String "2.0");
      ("method", `String method_name);
      ("params", `List params);
      ("id", `Int client.request_id)
    ] in

    let body = Yojson.Basic.to_string payload in

    Cohttp_lwt_unix.Client.post
      ~body:(Cohttp_lwt.Body.of_string body)
      ~headers:(Cohttp.Header.init_with "Content-Type" "application/json")
      (Uri.of_string client.rpc_url)
    >>= fun (resp, body) ->

    Cohttp_lwt.Body.to_string body
    >>= fun body_string ->

    let json = Yojson.Basic.from_string body_string in
    match json with
    | `Assoc assoc ->
        (match List.assoc_opt "result" assoc with
         | Some result -> Lwt.return result
         | None -> Lwt.fail_with "RPC error")
    | _ -> Lwt.fail_with "Invalid response"

  let hex_to_int = function
    | `String hex ->
        let hex = if String.sub hex 0 2 = "0x" then String.sub hex 2 (String.length hex - 2) else hex in
        int_of_string ("0x" ^ hex)
    | _ -> 0

  let wei_to_ether wei =
    float_of_int wei /. 1e18

  let wei_to_gwei wei =
    float_of_int wei /. 1e9

  let get_block_number client =
    rpc_call client "eth_blockNumber" []
    >|= hex_to_int

  let get_balance client address =
    rpc_call client "eth_getBalance" [`String address; `String "latest"]
    >|= hex_to_int
    >|= wei_to_ether

  let get_gas_price client =
    rpc_call client "eth_gasPrice" []
    >|= hex_to_int
    >|= wei_to_gwei
end

(* Example usage *)
let () =
  Lwt_main.run begin
    let client = Web3.create () in
    Printf.printf "🐫 OCaml Web3 Client\n%!";
    Printf.printf "%s\n%!" (String.make 40 '-');

    Web3.get_block_number client
    >>= fun block ->
    Printf.printf "📦 Block Number: %d\n%!" block;

    Web3.get_gas_price client
    >>= fun gas ->
    Printf.printf "⛽ Gas Price: %.2f Gwei\n%!" gas;

    let address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045" in
    Web3.get_balance client address
    >|= fun balance ->
    Printf.printf "💰 Balance: %.4f ETH\n%!" balance
  end
