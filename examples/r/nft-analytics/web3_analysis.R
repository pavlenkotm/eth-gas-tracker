# R Web3 Analytics
# Statistical analysis and visualization for blockchain data

library(httr)
library(jsonlite)
library(ggplot2)
library(dplyr)

Web3Client <- setRefClass(
  "Web3Client",
  fields = list(
    rpc_url = "character",
    request_id = "numeric"
  ),
  methods = list(
    initialize = function(rpc_url = "https://eth.llamarpc.com") {
      .self$rpc_url <- rpc_url
      .self$request_id <- 0
    },

    rpc_call = function(method, params = list()) {
      .self$request_id <- .self$request_id + 1

      payload <- list(
        jsonrpc = "2.0",
        method = method,
        params = params,
        id = .self$request_id
      )

      response <- POST(
        .self$rpc_url,
        body = toJSON(payload, auto_unbox = TRUE),
        add_headers("Content-Type" = "application/json")
      )

      if (status_code(response) != 200) {
        stop(paste("HTTP error:", status_code(response)))
      }

      result <- fromJSON(content(response, "text"))

      if (!is.null(result$error)) {
        stop(paste("RPC error:", result$error$message))
      }

      return(result$result)
    },

    hex_to_int = function(hex) {
      return(strtoi(hex, 16))
    },

    wei_to_ether = function(wei) {
      return(as.numeric(wei) / 1e18)
    },

    wei_to_gwei = function(wei) {
      return(as.numeric(wei) / 1e9)
    },

    get_block_number = function() {
      result <- .self$rpc_call("eth_blockNumber")
      return(.self$hex_to_int(result))
    },

    get_balance = function(address) {
      result <- .self$rpc_call("eth_getBalance", list(address, "latest"))
      wei <- .self$hex_to_int(result)
      return(.self$wei_to_ether(wei))
    },

    get_gas_price = function() {
      result <- .self$rpc_call("eth_gasPrice")
      wei <- .self$hex_to_int(result)
      return(.self$wei_to_gwei(wei))
    },

    get_block = function(block_number) {
      block_hex <- sprintf("0x%x", block_number)
      return(.self$rpc_call("eth_getBlockByNumber", list(block_hex, TRUE)))
    }
  )
)

# Analyze gas prices over time
analyze_gas_prices <- function(client, num_blocks = 100) {
  latest <- client$get_block_number()
  gas_prices <- numeric(num_blocks)
  block_numbers <- numeric(num_blocks)

  cat("📊 Analyzing gas prices over", num_blocks, "blocks...\n")

  for (i in 1:num_blocks) {
    block_num <- latest - num_blocks + i
    block <- tryCatch(
      client$get_block(block_num),
      error = function(e) NULL
    )

    if (!is.null(block) && !is.null(block$baseFeePerGas)) {
      gas_prices[i] <- client$hex_to_int(block$baseFeePerGas) / 1e9
      block_numbers[i] <- block_num
    }
  }

  df <- data.frame(
    block = block_numbers[block_numbers > 0],
    gas = gas_prices[gas_prices > 0]
  )

  # Statistical summary
  cat("\n📈 Gas Price Statistics:\n")
  cat(sprintf("  Mean: %.2f Gwei\n", mean(df$gas)))
  cat(sprintf("  Median: %.2f Gwei\n", median(df$gas)))
  cat(sprintf("  Std Dev: %.2f Gwei\n", sd(df$gas)))
  cat(sprintf("  Range: %.2f - %.2f Gwei\n", min(df$gas), max(df$gas)))

  # Plot
  p <- ggplot(df, aes(x = block, y = gas)) +
    geom_line(color = "blue", size = 1) +
    geom_smooth(method = "loess", color = "red", linetype = "dashed") +
    labs(
      title = "Ethereum Gas Prices Over Time",
      x = "Block Number",
      y = "Gas Price (Gwei)"
    ) +
    theme_minimal()

  print(p)
  return(df)
}

# Example usage
if (!interactive()) {
  cat("📊 R Web3 Analytics\n")
  cat(strrep("-", 40), "\n")

  client <- Web3Client$new()

  tryCatch({
    block <- client$get_block_number()
    cat(sprintf("📦 Block Number: %d\n", block))

    gas <- client$get_gas_price()
    cat(sprintf("⛽ Gas Price: %.2f Gwei\n", gas))

    address <- "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"
    balance <- client$get_balance(address)
    cat(sprintf("💰 Balance: %.4f ETH\n", balance))

    # Analyze gas prices
    # analyze_gas_prices(client, 50)

  }, error = function(e) {
    cat(sprintf("❌ Error: %s\n", e$message))
  })
}
