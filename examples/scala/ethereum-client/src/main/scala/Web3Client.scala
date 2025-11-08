package com.web3.client

import scala.concurrent.{Future, ExecutionContext}
import scala.util.{Try, Success, Failure}
import java.net.URI
import java.net.http.{HttpClient, HttpRequest, HttpResponse}
import java.net.http.HttpRequest.BodyPublishers
import java.net.http.HttpResponse.BodyHandlers
import spray.json._
import DefaultJsonProtocol._

/**
 * Functional Web3 client for Ethereum using Scala
 * Demonstrates type-safe blockchain interactions with functional programming
 */
object Web3Client {

  case class RpcRequest(
    jsonrpc: String = "2.0",
    method: String,
    params: List[Any],
    id: Int
  )

  case class RpcResponse[T](
    jsonrpc: String,
    result: Option[T],
    error: Option[JsValue],
    id: Int
  )

  class EthereumClient(rpcUrl: String = "https://eth.llamarpc.com") {
    private var requestId = 0
    private val client = HttpClient.newHttpClient()

    implicit val rpcRequestFormat = jsonFormat4(RpcRequest)

    /**
     * Make RPC call to Ethereum node
     */
    private def rpcCall[T: JsonReader](method: String, params: List[Any] = List.empty): Try[T] = Try {
      requestId += 1

      val request = RpcRequest(
        method = method,
        params = params,
        id = requestId
      )

      val httpRequest = HttpRequest.newBuilder()
        .uri(URI.create(rpcUrl))
        .header("Content-Type", "application/json")
        .POST(BodyPublishers.ofString(request.toJson.toString))
        .build()

      val response = client.send(httpRequest, BodyHandlers.ofString())

      if (response.statusCode() != 200) {
        throw new Exception(s"HTTP error: ${response.statusCode()}")
      }

      val json = response.body().parseJson.asJsObject
      json.fields.get("result") match {
        case Some(result) => result.convertTo[T]
        case None =>
          val error = json.fields.get("error")
          throw new Exception(s"RPC error: $error")
      }
    }

    /**
     * Get latest block number
     */
    def getBlockNumber: Try[Long] = {
      rpcCall[String]("eth_blockNumber")
        .map(hex => java.lang.Long.parseLong(hex.stripPrefix("0x"), 16))
    }

    /**
     * Get balance of address in ETH
     */
    def getBalance(address: String): Try[BigDecimal] = {
      rpcCall[String]("eth_getBalance", List(address, "latest"))
        .map { hex =>
          val wei = BigInt(hex.stripPrefix("0x"), 16)
          BigDecimal(wei) / BigDecimal("1000000000000000000")
        }
    }

    /**
     * Get current gas price in Gwei
     */
    def getGasPrice: Try[BigDecimal] = {
      rpcCall[String]("eth_gasPrice")
        .map { hex =>
          val wei = BigInt(hex.stripPrefix("0x"), 16)
          BigDecimal(wei) / BigDecimal("1000000000")
        }
    }

    /**
     * Get transaction by hash
     */
    def getTransaction(txHash: String): Try[JsValue] = {
      rpcCall[JsValue]("eth_getTransactionByHash", List(txHash))
    }

    /**
     * Get block by number
     */
    def getBlock(blockNumber: Long): Try[JsValue] = {
      val blockHex = s"0x${blockNumber.toHexString}"
      rpcCall[JsValue]("eth_getBlockByNumber", List(blockHex, true))
    }

    /**
     * Call contract method (read-only)
     */
    def call(to: String, data: String, from: Option[String] = None): Try[String] = {
      val params = Map(
        "to" -> to.toJson,
        "data" -> data.toJson
      ) ++ from.map(f => "from" -> f.toJson)

      rpcCall[String]("eth_call", List(params.toJson, "latest"))
    }
  }

  def main(args: Array[String]): Unit = {
    println("⚙️  Scala Web3 Client")
    println("-" * 40)

    val client = new EthereumClient()

    // Get block number
    client.getBlockNumber match {
      case Success(block) => println(s"📦 Block Number: ${block}")
      case Failure(e) => println(s"❌ Error: ${e.getMessage}")
    }

    // Get gas price
    client.getGasPrice match {
      case Success(gas) => println(f"⛽ Gas Price: ${gas}%.2f Gwei")
      case Failure(e) => println(s"❌ Error: ${e.getMessage}")
    }

    // Get balance (Vitalik's address)
    val address = "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    client.getBalance(address) match {
      case Success(balance) => println(f"💰 Balance: ${balance}%.4f ETH")
      case Failure(e) => println(s"❌ Error: ${e.getMessage}")
    }
  }
}
