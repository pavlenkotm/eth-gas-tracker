require("@nomicfoundation/hardhat-toolbox");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      chainId: 31337,
    },
    localhost: {
      url: "http://127.0.0.1:8545",
    },
    // Uncomment and add your keys for testnet deployment
    // sepolia: {
    //   url: `https://eth-sepolia.g.alchemy.com/v2/${ALCHEMY_API_KEY}`,
    //   accounts: [PRIVATE_KEY],
    // },
  },
  paths: {
    sources: "./",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts",
  },
};
