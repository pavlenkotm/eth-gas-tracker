module simple_coin::coin {
    use std::signer;
    use aptos_framework::coin::{Self, Coin, MintCapability, BurnCapability};
    use aptos_framework::account;
    use std::string;
    use std::option;

    /// Error codes
    const E_NOT_OWNER: u64 = 1;
    const E_INSUFFICIENT_BALANCE: u64 = 2;
    const E_ALREADY_INITIALIZED: u64 = 3;

    /// Struct representing the coin type
    struct SimpleCoin has key {}

    /// Capabilities stored under owner account
    struct Capabilities has key {
        mint_cap: MintCapability<SimpleCoin>,
        burn_cap: BurnCapability<SimpleCoin>,
        owner: address,
    }

    /// Initialize the coin
    public entry fun initialize(
        owner: &signer,
        name: vector<u8>,
        symbol: vector<u8>,
        decimals: u8,
    ) {
        let owner_addr = signer::address_of(owner);

        // Ensure not already initialized
        assert!(!exists<Capabilities>(owner_addr), E_ALREADY_INITIALIZED);

        // Initialize the coin
        let (burn_cap, freeze_cap, mint_cap) = coin::initialize<SimpleCoin>(
            owner,
            string::utf8(name),
            string::utf8(symbol),
            decimals,
            true, // monitor_supply
        );

        // Store capabilities
        move_to(owner, Capabilities {
            mint_cap,
            burn_cap,
            owner: owner_addr,
        });

        // Destroy freeze capability (not needed)
        coin::destroy_freeze_cap(freeze_cap);
    }

    /// Mint new coins (owner only)
    public entry fun mint(
        owner: &signer,
        recipient: address,
        amount: u64,
    ) acquires Capabilities {
        let owner_addr = signer::address_of(owner);
        let caps = borrow_global<Capabilities>(owner_addr);

        // Verify owner
        assert!(caps.owner == owner_addr, E_NOT_OWNER);

        // Register recipient if not already registered
        if (!coin::is_account_registered<SimpleCoin>(recipient)) {
            coin::register<SimpleCoin>(&account::create_signer_for_test(recipient));
        };

        // Mint coins
        let coins = coin::mint<SimpleCoin>(amount, &caps.mint_cap);
        coin::deposit(recipient, coins);
    }

    /// Burn coins from sender's account
    public entry fun burn(
        owner: &signer,
        amount: u64,
    ) acquires Capabilities {
        let owner_addr = signer::address_of(owner);
        let caps = borrow_global<Capabilities>(owner_addr);

        // Verify owner
        assert!(caps.owner == owner_addr, E_NOT_OWNER);

        // Withdraw and burn
        let coins = coin::withdraw<SimpleCoin>(owner, amount);
        coin::burn(coins, &caps.burn_cap);
    }

    /// Transfer coins
    public entry fun transfer(
        sender: &signer,
        recipient: address,
        amount: u64,
    ) {
        // Register recipient if needed
        if (!coin::is_account_registered<SimpleCoin>(recipient)) {
            coin::register<SimpleCoin>(&account::create_signer_for_test(recipient));
        };

        // Transfer
        coin::transfer<SimpleCoin>(sender, recipient, amount);
    }

    /// Register to receive coins
    public entry fun register(account: &signer) {
        coin::register<SimpleCoin>(account);
    }

    /// Get balance
    #[view]
    public fun balance_of(account: address): u64 {
        coin::balance<SimpleCoin>(account)
    }

    /// Get total supply
    #[view]
    public fun total_supply(): u128 {
        option::extract(&mut coin::supply<SimpleCoin>())
    }

    /// Check if account is registered
    #[view]
    public fun is_registered(account: address): bool {
        coin::is_account_registered<SimpleCoin>(account)
    }

    #[test_only]
    public fun initialize_for_test(
        owner: &signer,
    ): (BurnCapability<SimpleCoin>, MintCapability<SimpleCoin>) {
        let owner_addr = signer::address_of(owner);

        let (burn_cap, freeze_cap, mint_cap) = coin::initialize<SimpleCoin>(
            owner,
            string::utf8(b"Simple Coin"),
            string::utf8(b"SMPL"),
            8,
            true,
        );

        coin::destroy_freeze_cap(freeze_cap);

        move_to(owner, Capabilities {
            mint_cap,
            burn_cap,
            owner: owner_addr,
        });

        let caps = borrow_global<Capabilities>(owner_addr);
        (caps.burn_cap, caps.mint_cap)
    }
}
