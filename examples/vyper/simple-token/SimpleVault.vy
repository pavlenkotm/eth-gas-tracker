# @version ^0.3.10
"""
@title Simple Vault
@author Web3 Multi-Language Playground
@notice A simple vault contract for depositing and withdrawing ETH
@dev Demonstrates Vyper syntax and best practices
"""

# Events
event Deposit:
    depositor: indexed(address)
    amount: uint256
    balance: uint256

event Withdrawal:
    withdrawer: indexed(address)
    amount: uint256
    balance: uint256

event OwnershipTransferred:
    previousOwner: indexed(address)
    newOwner: indexed(address)

# State variables
owner: public(address)
balances: public(HashMap[address, uint256])
totalDeposits: public(uint256)
withdrawalEnabled: public(bool)

# Constants
MIN_DEPOSIT: constant(uint256) = 10 ** 15  # 0.001 ETH
MAX_DEPOSIT: constant(uint256) = 100 * 10 ** 18  # 100 ETH

@external
def __init__():
    """
    @notice Contract constructor
    @dev Initializes the contract with deployer as owner
    """
    self.owner = msg.sender
    self.withdrawalEnabled = True

@external
@payable
def deposit():
    """
    @notice Deposit ETH into the vault
    @dev Minimum deposit is 0.001 ETH, maximum is 100 ETH
    """
    assert msg.value >= MIN_DEPOSIT, "Deposit too small"
    assert msg.value <= MAX_DEPOSIT, "Deposit too large"

    self.balances[msg.sender] += msg.value
    self.totalDeposits += msg.value

    log Deposit(msg.sender, msg.value, self.balances[msg.sender])

@external
def withdraw(amount: uint256):
    """
    @notice Withdraw ETH from the vault
    @param amount Amount to withdraw in wei
    @dev Caller must have sufficient balance
    """
    assert self.withdrawalEnabled, "Withdrawals are disabled"
    assert amount > 0, "Amount must be greater than 0"
    assert self.balances[msg.sender] >= amount, "Insufficient balance"

    self.balances[msg.sender] -= amount
    self.totalDeposits -= amount

    send(msg.sender, amount)

    log Withdrawal(msg.sender, amount, self.balances[msg.sender])

@external
def withdrawAll():
    """
    @notice Withdraw all deposited ETH
    @dev Convenience function to withdraw entire balance
    """
    amount: uint256 = self.balances[msg.sender]
    assert amount > 0, "No balance to withdraw"

    self.withdraw(amount)

@view
@external
def getBalance(account: address) -> uint256:
    """
    @notice Get the balance of an account
    @param account The address to query
    @return The balance in wei
    """
    return self.balances[account]

@view
@external
def getContractBalance() -> uint256:
    """
    @notice Get the total ETH held by the contract
    @return The contract balance in wei
    """
    return self.balance

@external
def setWithdrawalEnabled(enabled: bool):
    """
    @notice Enable or disable withdrawals
    @param enabled True to enable, false to disable
    @dev Only owner can call this function
    """
    assert msg.sender == self.owner, "Only owner can toggle withdrawals"
    self.withdrawalEnabled = enabled

@external
def transferOwnership(newOwner: address):
    """
    @notice Transfer ownership to a new address
    @param newOwner The address of the new owner
    @dev Only current owner can transfer ownership
    """
    assert msg.sender == self.owner, "Only owner can transfer ownership"
    assert newOwner != empty(address), "New owner cannot be zero address"

    oldOwner: address = self.owner
    self.owner = newOwner

    log OwnershipTransferred(oldOwner, newOwner)

@external
def emergencyWithdraw():
    """
    @notice Emergency withdrawal function for owner
    @dev Allows owner to withdraw all ETH in emergency situations
    """
    assert msg.sender == self.owner, "Only owner can emergency withdraw"

    amount: uint256 = self.balance
    send(self.owner, amount)

@view
@external
def getMinDeposit() -> uint256:
    """
    @notice Get the minimum deposit amount
    @return Minimum deposit in wei
    """
    return MIN_DEPOSIT

@view
@external
def getMaxDeposit() -> uint256:
    """
    @notice Get the maximum deposit amount
    @return Maximum deposit in wei
    """
    return MAX_DEPOSIT
