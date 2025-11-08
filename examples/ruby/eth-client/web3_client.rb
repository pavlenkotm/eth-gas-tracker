#!/usr/bin/env ruby
# frozen_string_literal: true

require 'net/http'
require 'json'
require 'uri'

##
# Ruby Web3 Client for Ethereum
# Elegant blockchain interactions with Ruby's expressive syntax
class Web3Client
  attr_reader :rpc_url, :request_id

  def initialize(rpc_url = 'https://eth.llamarpc.com')
    @rpc_url = URI.parse(rpc_url)
    @request_id = 0
  end

  # Get latest block number
  def block_number
    hex_to_int(rpc_call('eth_blockNumber'))
  end

  # Get balance of address in ETH
  def balance(address)
    wei = hex_to_int(rpc_call('eth_getBalance', [address, 'latest']))
    wei_to_ether(wei)
  end

  # Get current gas price in Gwei
  def gas_price
    wei = hex_to_int(rpc_call('eth_gasPrice'))
    wei_to_gwei(wei)
  end

  # Get transaction by hash
  def transaction(tx_hash)
    rpc_call('eth_getTransactionByHash', [tx_hash])
  end

  # Get block by number
  def block(number = 'latest')
    block_param = number.is_a?(Integer) ? format('0x%x', number) : number
    rpc_call('eth_getBlockByNumber', [block_param, true])
  end

  # Call contract method (read-only)
  def call(to:, data:, from: nil)
    params = [{
      from: from,
      to: to,
      data: data
    }.compact, 'latest']

    rpc_call('eth_call', params)
  end

  private

  def rpc_call(method, params = [])
    @request_id += 1

    request = Net::HTTP::Post.new(@rpc_url.request_uri)
    request['Content-Type'] = 'application/json'
    request.body = {
      jsonrpc: '2.0',
      method: method,
      params: params,
      id: @request_id
    }.to_json

    response = Net::HTTP.start(@rpc_url.host, @rpc_url.port, use_ssl: @rpc_url.scheme == 'https') do |http|
      http.request(request)
    end

    raise "HTTP Error: #{response.code}" unless response.code.to_i == 200

    result = JSON.parse(response.body)
    raise "RPC Error: #{result['error']}" if result['error']

    result['result']
  end

  def hex_to_int(hex)
    hex.to_i(16)
  end

  def wei_to_ether(wei)
    wei.to_f / 1e18
  end

  def wei_to_gwei(wei)
    wei.to_f / 1e9
  end
end

# Example usage
if __FILE__ == $PROGRAM_NAME
  client = Web3Client.new

  puts '💎 Ruby Web3 Client'
  puts '-' * 40

  # Block number
  block = client.block_number
  puts "📦 Block Number: #{block.to_s.reverse.gsub(/(\d{3})(?=\d)/, '\\1,').reverse}"

  # Gas price
  gas = client.gas_price
  puts "⛽ Gas Price: #{gas.round(2)} Gwei"

  # Balance (Vitalik's address)
  address = '0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045'
  balance = client.balance(address)
  puts "💰 Balance: #{balance.round(4)} ETH"
end
