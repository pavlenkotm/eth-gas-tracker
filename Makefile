.PHONY: help install test lint clean

help:
	@echo "Web3 Multi-Language Playground - Make Commands"
	@echo ""
	@echo "Available commands:"
	@echo "  make install     - Install all dependencies"
	@echo "  make test        - Run all tests"
	@echo "  make lint        - Run all linters"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make python      - Run Python Gas Tracker"
	@echo "  make solidity    - Test Solidity contracts"
	@echo "  make rust        - Test Rust programs"
	@echo "  make typescript  - Build TypeScript DApp"
	@echo "  make go          - Build Go utilities"
	@echo "  make java        - Build Java integration"

install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt
	@echo "Installing Node.js dependencies..."
	cd examples/solidity/erc20-token && npm install || true
	cd examples/typescript/wagmi-dapp && npm install || true
	@echo "Done!"

test:
	@echo "Running Python tests..."
	pytest ethgas/tests/ -v || true
	@echo "Running Solidity tests..."
	cd examples/solidity/erc20-token && npx hardhat test || true
	@echo "Done!"

lint:
	@echo "Running Python linting..."
	flake8 ethgas || true
	@echo "Running JavaScript/TypeScript linting..."
	cd examples/typescript/wagmi-dapp && npm run lint || true
	@echo "Done!"

clean:
	@echo "Cleaning Python artifacts..."
	find . -type d -name __pycache__ -exec rm -rf {} + || true
	find . -type f -name "*.pyc" -delete || true
	@echo "Cleaning Node.js artifacts..."
	find . -type d -name node_modules -exec rm -rf {} + || true
	find . -type d -name .next -exec rm -rf {} + || true
	@echo "Cleaning build artifacts..."
	find . -type d -name target -exec rm -rf {} + || true
	find . -type d -name build -exec rm -rf {} + || true
	@echo "Done!"

python:
	@echo "Running Python Gas Tracker..."
	python -m ethgas.main --watch 10

solidity:
	@echo "Testing Solidity contracts..."
	cd examples/solidity/erc20-token && npx hardhat test

rust:
	@echo "Testing Rust programs..."
	cd examples/rust/solana-anchor && anchor test || cargo test

typescript:
	@echo "Building TypeScript DApp..."
	cd examples/typescript/wagmi-dapp && npm run build

go:
	@echo "Building Go utilities..."
	cd examples/go/web3-utils && go build

java:
	@echo "Building Java integration..."
	cd examples/java/web3j-integration && mvn clean package
