"""Network configurations for different blockchains."""

NETWORKS = {
    "ethereum": {
        "name": "Ethereum",
        "rpc": "https://eth.llamarpc.com",
        "chain_id": 1,
        "coingecko_id": "ethereum",
        "explorer": "https://etherscan.io",
    },
    "polygon": {
        "name": "Polygon",
        "rpc": "https://polygon-rpc.com",
        "chain_id": 137,
        "coingecko_id": "matic-network",
        "explorer": "https://polygonscan.com",
    },
    "arbitrum": {
        "name": "Arbitrum One",
        "rpc": "https://arb1.arbitrum.io/rpc",
        "chain_id": 42161,
        "coingecko_id": "ethereum",  # ARB использует ETH для газа
        "explorer": "https://arbiscan.io",
    },
    "optimism": {
        "name": "Optimism",
        "rpc": "https://mainnet.optimism.io",
        "chain_id": 10,
        "coingecko_id": "ethereum",  # OP использует ETH для газа
        "explorer": "https://optimistic.etherscan.io",
    },
    "bsc": {
        "name": "BNB Smart Chain",
        "rpc": "https://bsc-dataseed.binance.org",
        "chain_id": 56,
        "coingecko_id": "binancecoin",
        "explorer": "https://bscscan.com",
    },
    "base": {
        "name": "Base",
        "rpc": "https://mainnet.base.org",
        "chain_id": 8453,
        "coingecko_id": "ethereum",  # Base использует ETH для газа
        "explorer": "https://basescan.org",
    },
    "zksync": {
        "name": "zkSync Era",
        "rpc": "https://mainnet.era.zksync.io",
        "chain_id": 324,
        "coingecko_id": "ethereum",  # zkSync использует ETH для газа
        "explorer": "https://explorer.zksync.io",
    },
    "avalanche": {
        "name": "Avalanche C-Chain",
        "rpc": "https://api.avax.network/ext/bc/C/rpc",
        "chain_id": 43114,
        "coingecko_id": "avalanche-2",
        "explorer": "https://snowtrace.io",
    },
}

# Gas costs for different transaction types (in gas units)
TX_TYPES = {
    "simple": {"gas": 21000, "name": "Simple Transfer"},
    "erc20": {"gas": 65000, "name": "ERC-20 Transfer"},
    "swap": {"gas": 150000, "name": "DEX Swap"},
    "nft_mint": {"gas": 100000, "name": "NFT Mint"},
    "nft_transfer": {"gas": 85000, "name": "NFT Transfer"},
}
