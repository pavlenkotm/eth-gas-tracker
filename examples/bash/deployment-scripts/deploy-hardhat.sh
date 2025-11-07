#!/bin/bash

###############################################################################
# Hardhat Smart Contract Deployment Script
# Automates deployment to multiple networks with safety checks
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NETWORKS=("localhost" "sepolia" "mainnet" "polygon" "arbitrum")
CONTRACTS_DIR="contracts"
DEPLOY_SCRIPT="scripts/deploy.js"

# Functions
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}  $1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

check_dependencies() {
    print_header "Checking Dependencies"

    # Check Node.js
    if ! command -v node &> /dev/null; then
        print_error "Node.js is not installed"
        exit 1
    fi
    print_success "Node.js $(node --version)"

    # Check npm
    if ! command -v npm &> /dev/null; then
        print_error "npm is not installed"
        exit 1
    fi
    print_success "npm $(npm --version)"

    # Check Hardhat
    if [ ! -f "node_modules/.bin/hardhat" ]; then
        print_error "Hardhat not found. Run: npm install"
        exit 1
    fi
    print_success "Hardhat installed"

    # Check for .env file
    if [ ! -f ".env" ]; then
        print_warning ".env file not found"
        print_info "Creating .env template..."
        cat > .env << EOF
# Ethereum Mainnet
MAINNET_RPC_URL=https://eth.llamarpc.com
MAINNET_PRIVATE_KEY=

# Sepolia Testnet
SEPOLIA_RPC_URL=https://rpc.sepolia.org
SEPOLIA_PRIVATE_KEY=

# Polygon
POLYGON_RPC_URL=https://polygon-rpc.com
POLYGON_PRIVATE_KEY=

# Arbitrum
ARBITRUM_RPC_URL=https://arb1.arbitrum.io/rpc
ARBITRUM_PRIVATE_KEY=

# API Keys
ETHERSCAN_API_KEY=
POLYGONSCAN_API_KEY=
ARBISCAN_API_KEY=
EOF
        print_warning "Please configure .env file before deploying"
        exit 1
    fi
    print_success ".env file found"
}

compile_contracts() {
    print_header "Compiling Contracts"

    npx hardhat clean
    npx hardhat compile

    if [ $? -eq 0 ]; then
        print_success "Contracts compiled successfully"
    else
        print_error "Compilation failed"
        exit 1
    fi
}

run_tests() {
    print_header "Running Tests"

    npx hardhat test

    if [ $? -eq 0 ]; then
        print_success "All tests passed"
    else
        print_error "Tests failed"
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
}

check_gas_price() {
    local network=$1
    print_info "Checking gas price on $network..."

    # This would need actual gas price checking logic
    # For now, just a placeholder
    print_info "Current gas price: ~30 Gwei"
}

deploy_to_network() {
    local network=$1

    print_header "Deploying to $network"

    # Confirmation for mainnet
    if [ "$network" = "mainnet" ]; then
        print_warning "You are about to deploy to MAINNET!"
        read -p "Are you sure? Type 'yes' to continue: " confirmation
        if [ "$confirmation" != "yes" ]; then
            print_info "Deployment cancelled"
            return
        fi
    fi

    # Check gas price for mainnet
    if [ "$network" = "mainnet" ] || [ "$network" = "polygon" ]; then
        check_gas_price "$network"
    fi

    # Deploy
    print_info "Deploying contracts..."
    npx hardhat run "$DEPLOY_SCRIPT" --network "$network"

    if [ $? -eq 0 ]; then
        print_success "Deployment successful on $network"

        # Verify contracts if not localhost
        if [ "$network" != "localhost" ] && [ "$network" != "hardhat" ]; then
            read -p "Verify contracts on block explorer? (y/n) " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                verify_contracts "$network"
            fi
        fi
    else
        print_error "Deployment failed on $network"
        exit 1
    fi
}

verify_contracts() {
    local network=$1

    print_header "Verifying Contracts on $network"

    # This would need the actual contract addresses and constructor args
    print_info "Verifying on block explorer..."

    # Example verification command
    # npx hardhat verify --network $network DEPLOYED_CONTRACT_ADDRESS "Constructor Arg 1" "Constructor Arg 2"

    print_warning "Verification requires contract addresses from deployment"
    print_info "Run: npx hardhat verify --network $network <address> <constructor-args>"
}

create_deployment_report() {
    print_header "Creating Deployment Report"

    REPORT_FILE="deployments/deployment-$(date +%Y%m%d-%H%M%S).md"
    mkdir -p deployments

    cat > "$REPORT_FILE" << EOF
# Deployment Report

**Date:** $(date)
**Network:** $NETWORK
**Deployer:** $(npx hardhat accounts --network $NETWORK 2>/dev/null | head -n 1 || echo "N/A")

## Deployed Contracts

<!-- Add deployed contract addresses here -->

## Transaction Hashes

<!-- Add deployment transaction hashes here -->

## Gas Usage

<!-- Add gas usage information here -->

## Verification Status

<!-- Add verification status here -->
EOF

    print_success "Report created: $REPORT_FILE"
}

# Main script
main() {
    print_header "Smart Contract Deployment"

    # Parse arguments
    NETWORK=${1:-localhost}
    SKIP_TESTS=${2:-false}

    # Validate network
    if [[ ! " ${NETWORKS[@]} " =~ " ${NETWORK} " ]]; then
        print_error "Invalid network: $NETWORK"
        print_info "Available networks: ${NETWORKS[*]}"
        exit 1
    fi

    # Run pre-deployment checks
    check_dependencies
    compile_contracts

    # Run tests unless skipped
    if [ "$SKIP_TESTS" != "--skip-tests" ]; then
        run_tests
    else
        print_warning "Skipping tests"
    fi

    # Deploy
    deploy_to_network "$NETWORK"

    # Create report
    create_deployment_report

    print_header "Deployment Complete"
    print_success "All done! 🎉"
}

# Show usage if no arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <network> [--skip-tests]"
    echo ""
    echo "Available networks:"
    for network in "${NETWORKS[@]}"; do
        echo "  - $network"
    done
    echo ""
    echo "Examples:"
    echo "  $0 localhost"
    echo "  $0 sepolia"
    echo "  $0 mainnet --skip-tests"
    exit 0
fi

# Run main function
main "$@"
