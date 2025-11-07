import pytest
from eth_utils import to_wei
from web3 import Web3

@pytest.fixture
def vault(accounts, project):
    """Deploy the SimpleVault contract"""
    return accounts[0].deploy(project.SimpleVault)

def test_initial_state(vault, accounts):
    """Test initial contract state"""
    assert vault.owner() == accounts[0].address
    assert vault.totalDeposits() == 0
    assert vault.withdrawalEnabled() == True

def test_deposit(vault, accounts):
    """Test depositing ETH"""
    deposit_amount = to_wei(1, 'ether')

    # Make deposit
    vault.deposit(value=deposit_amount, sender=accounts[1])

    # Verify balance
    assert vault.getBalance(accounts[1].address) == deposit_amount
    assert vault.totalDeposits() == deposit_amount

def test_deposit_too_small(vault, accounts):
    """Test deposit below minimum fails"""
    min_deposit = vault.getMinDeposit()

    with pytest.raises(Exception):
        vault.deposit(value=min_deposit - 1, sender=accounts[1])

def test_deposit_too_large(vault, accounts):
    """Test deposit above maximum fails"""
    max_deposit = vault.getMaxDeposit()

    with pytest.raises(Exception):
        vault.deposit(value=max_deposit + 1, sender=accounts[1])

def test_withdraw(vault, accounts):
    """Test withdrawing ETH"""
    deposit_amount = to_wei(1, 'ether')
    withdraw_amount = to_wei(0.5, 'ether')

    # Deposit first
    vault.deposit(value=deposit_amount, sender=accounts[1])

    # Get initial balance
    initial_balance = accounts[1].balance

    # Withdraw
    vault.withdraw(withdraw_amount, sender=accounts[1])

    # Verify balances
    assert vault.getBalance(accounts[1].address) == deposit_amount - withdraw_amount
    assert vault.totalDeposits() == deposit_amount - withdraw_amount

def test_withdraw_all(vault, accounts):
    """Test withdrawing all deposited ETH"""
    deposit_amount = to_wei(2, 'ether')

    # Deposit
    vault.deposit(value=deposit_amount, sender=accounts[1])

    # Withdraw all
    vault.withdrawAll(sender=accounts[1])

    # Verify balance is zero
    assert vault.getBalance(accounts[1].address) == 0

def test_withdraw_insufficient_balance(vault, accounts):
    """Test withdrawal with insufficient balance fails"""
    deposit_amount = to_wei(1, 'ether')
    withdraw_amount = to_wei(2, 'ether')

    vault.deposit(value=deposit_amount, sender=accounts[1])

    with pytest.raises(Exception):
        vault.withdraw(withdraw_amount, sender=accounts[1])

def test_toggle_withdrawals(vault, accounts):
    """Test enabling/disabling withdrawals"""
    deposit_amount = to_wei(1, 'ether')

    # Deposit
    vault.deposit(value=deposit_amount, sender=accounts[1])

    # Disable withdrawals
    vault.setWithdrawalEnabled(False, sender=accounts[0])
    assert vault.withdrawalEnabled() == False

    # Try to withdraw (should fail)
    with pytest.raises(Exception):
        vault.withdraw(deposit_amount, sender=accounts[1])

    # Re-enable withdrawals
    vault.setWithdrawalEnabled(True, sender=accounts[0])

    # Withdraw should work now
    vault.withdraw(deposit_amount, sender=accounts[1])

def test_transfer_ownership(vault, accounts):
    """Test ownership transfer"""
    new_owner = accounts[1].address

    # Transfer ownership
    vault.transferOwnership(new_owner, sender=accounts[0])

    # Verify new owner
    assert vault.owner() == new_owner

def test_only_owner_can_transfer_ownership(vault, accounts):
    """Test that only owner can transfer ownership"""
    with pytest.raises(Exception):
        vault.transferOwnership(accounts[2].address, sender=accounts[1])

def test_emergency_withdraw(vault, accounts):
    """Test emergency withdrawal by owner"""
    deposit_amount = to_wei(5, 'ether')

    # Multiple users deposit
    vault.deposit(value=deposit_amount, sender=accounts[1])
    vault.deposit(value=deposit_amount, sender=accounts[2])

    # Owner performs emergency withdrawal
    initial_owner_balance = accounts[0].balance
    vault.emergencyWithdraw(sender=accounts[0])

    # Verify contract balance is zero
    assert vault.getContractBalance() == 0

def test_multiple_deposits(vault, accounts):
    """Test multiple deposits from same account"""
    first_deposit = to_wei(1, 'ether')
    second_deposit = to_wei(2, 'ether')

    vault.deposit(value=first_deposit, sender=accounts[1])
    vault.deposit(value=second_deposit, sender=accounts[1])

    expected_balance = first_deposit + second_deposit
    assert vault.getBalance(accounts[1].address) == expected_balance
    assert vault.totalDeposits() == expected_balance
