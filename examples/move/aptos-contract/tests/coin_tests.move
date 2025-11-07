#[test_only]
module simple_coin::coin_tests {
    use std::signer;
    use simple_coin::coin::{Self, SimpleCoin};
    use aptos_framework::coin;

    #[test(owner = @simple_coin)]
    public fun test_initialize(owner: &signer) {
        // Initialize the coin
        coin::initialize(
            owner,
            b"Simple Coin",
            b"SMPL",
            8,
        );

        // Verify initialization
        assert!(coin::is_coin_initialized<SimpleCoin>(), 1);
    }

    #[test(owner = @simple_coin, recipient = @0x123)]
    public fun test_mint_and_balance(owner: &signer, recipient: &signer) {
        // Initialize
        coin::initialize_for_test(owner);

        let recipient_addr = signer::address_of(recipient);

        // Register recipient
        coin::register(recipient);

        // Mint coins
        coin::mint(owner, recipient_addr, 1000);

        // Check balance
        assert!(coin::balance_of(recipient_addr) == 1000, 2);
    }

    #[test(owner = @simple_coin, user1 = @0x123, user2 = @0x456)]
    public fun test_transfer(owner: &signer, user1: &signer, user2: &signer) {
        // Initialize
        coin::initialize_for_test(owner);

        let user1_addr = signer::address_of(user1);
        let user2_addr = signer::address_of(user2);

        // Register users
        coin::register(user1);
        coin::register(user2);

        // Mint to user1
        coin::mint(owner, user1_addr, 1000);

        // Transfer from user1 to user2
        coin::transfer(user1, user2_addr, 300);

        // Verify balances
        assert!(coin::balance_of(user1_addr) == 700, 3);
        assert!(coin::balance_of(user2_addr) == 300, 4);
    }

    #[test(owner = @simple_coin)]
    public fun test_burn(owner: &signer) {
        // Initialize
        coin::initialize_for_test(owner);

        let owner_addr = signer::address_of(owner);

        // Register owner
        coin::register(owner);

        // Mint coins
        coin::mint(owner, owner_addr, 1000);

        // Burn coins
        coin::burn(owner, 300);

        // Verify balance
        assert!(coin::balance_of(owner_addr) == 700, 5);
    }

    #[test(owner = @simple_coin)]
    public fun test_total_supply(owner: &signer) {
        // Initialize
        coin::initialize_for_test(owner);

        let owner_addr = signer::address_of(owner);

        // Register
        coin::register(owner);

        // Mint
        coin::mint(owner, owner_addr, 5000);

        // Check total supply
        assert!(coin::total_supply() == 5000, 6);

        // Burn some
        coin::burn(owner, 2000);

        // Check supply decreased
        assert!(coin::total_supply() == 3000, 7);
    }
}
