(ns web3.core
  "Clojure Web3 client - Functional blockchain interactions"
  (:require [clj-http.client :as http]
            [cheshire.core :as json]))

(def ^:dynamic *rpc-url* "https://eth.llamarpc.com")
(def request-id (atom 0))

(defn rpc-call
  "Make JSON-RPC call to Ethereum node"
  [method & params]
  (let [id (swap! request-id inc)
        payload {:jsonrpc "2.0"
                 :method method
                 :params (vec params)
                 :id id}
        response (http/post *rpc-url*
                           {:body (json/generate-string payload)
                            :content-type :json
                            :as :json})]
    (get-in response [:body :result])))

(defn hex->int
  "Convert hex string to integer"
  [hex]
  (when hex
    (BigInteger. (.substring hex 2) 16)))

(defn wei->ether
  "Convert wei to ether"
  [wei]
  (/ (bigdec wei) 1e18))

(defn wei->gwei
  "Convert wei to gwei"
  [wei]
  (/ (bigdec wei) 1e9))

(defn block-number
  "Get latest block number"
  []
  (-> (rpc-call "eth_blockNumber")
      hex->int))

(defn balance
  "Get balance of address in ETH"
  [address]
  (-> (rpc-call "eth_getBalance" address "latest")
      hex->int
      wei->ether))

(defn gas-price
  "Get current gas price in Gwei"
  []
  (-> (rpc-call "eth_gasPrice")
      hex->int
      wei->gwei))

(defn transaction
  "Get transaction by hash"
  [tx-hash]
  (rpc-call "eth_getTransactionByHash" tx-hash))

(defn block
  "Get block by number"
  [number]
  (let [block-hex (format "0x%x" number)]
    (rpc-call "eth_getBlockByNumber" block-hex true)))

(defn -main
  "Example usage"
  [& args]
  (println "🔧 Clojure Web3 Client")
  (println (apply str (repeat 40 "-")))

  (let [block-num (block-number)
        gas (gas-price)
        addr "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
        bal (balance addr)]

    (println "📦 Block Number:" block-num)
    (println "⛽ Gas Price:" (format "%.2f" gas) "Gwei")
    (println "💰 Balance:" (format "%.4f" bal) "ETH")))
