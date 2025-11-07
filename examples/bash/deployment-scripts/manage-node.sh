#!/bin/bash

###############################################################################
# Ethereum Node Management Script
# Start, stop, and manage local Ethereum nodes
###############################################################################

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
HARDHAT_PORT=8545
GANACHE_PORT=7545
NODE_TYPE="hardhat"

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

start_hardhat() {
    print_info "Starting Hardhat node on port $HARDHAT_PORT..."

    # Check if already running
    if lsof -Pi :$HARDHAT_PORT -sTCP:LISTEN -t >/dev/null ; then
        print_error "Port $HARDHAT_PORT is already in use"
        exit 1
    fi

    npx hardhat node &
    NODE_PID=$!

    sleep 3

    if ps -p $NODE_PID > /dev/null; then
        print_success "Hardhat node started (PID: $NODE_PID)"
        echo $NODE_PID > .hardhat.pid
    else
        print_error "Failed to start Hardhat node"
        exit 1
    fi
}

start_ganache() {
    print_info "Starting Ganache on port $GANACHE_PORT..."

    if ! command -v ganache &> /dev/null; then
        print_error "Ganache not installed. Run: npm install -g ganache"
        exit 1
    fi

    ganache --port $GANACHE_PORT &
    NODE_PID=$!

    sleep 2

    print_success "Ganache started (PID: $NODE_PID)"
    echo $NODE_PID > .ganache.pid
}

stop_node() {
    print_info "Stopping Ethereum node..."

    if [ -f ".hardhat.pid" ]; then
        PID=$(cat .hardhat.pid)
        kill $PID 2>/dev/null && print_success "Hardhat node stopped" || print_error "Node not running"
        rm .hardhat.pid
    fi

    if [ -f ".ganache.pid" ]; then
        PID=$(cat .ganache.pid)
        kill $PID 2>/dev/null && print_success "Ganache stopped" || print_error "Node not running"
        rm .ganache.pid
    fi
}

status() {
    print_info "Checking node status..."

    if lsof -Pi :$HARDHAT_PORT -sTCP:LISTEN -t >/dev/null ; then
        print_success "Hardhat node running on port $HARDHAT_PORT"
    else
        print_info "Hardhat node not running"
    fi

    if lsof -Pi :$GANACHE_PORT -sTCP:LISTEN -t >/dev/null ; then
        print_success "Ganache running on port $GANACHE_PORT"
    else
        print_info "Ganache not running"
    fi
}

case "$1" in
    start)
        start_hardhat
        ;;
    start-ganache)
        start_ganache
        ;;
    stop)
        stop_node
        ;;
    restart)
        stop_node
        sleep 1
        start_hardhat
        ;;
    status)
        status
        ;;
    *)
        echo "Usage: $0 {start|start-ganache|stop|restart|status}"
        exit 1
        ;;
esac
