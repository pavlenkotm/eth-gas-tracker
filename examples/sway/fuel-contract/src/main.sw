contract;

use std::{
    auth::msg_sender,
    call_frames::msg_asset_id,
    context::msg_amount,
    token::{
        burn,
        mint,
        transfer,
    },
    storage::storage_map::*,
};

abi TokenContract {
    #[storage(read, write)]
    fn initialize(initial_supply: u64, owner: Identity);

    #[storage(read)]
    fn get_balance(target: Identity) -> u64;

    #[storage(read, write)]
    fn transfer_tokens(amount: u64, recipient: Identity);

    #[storage(read, write)]
    fn mint_tokens(amount: u64, recipient: Identity);

    #[storage(read, write)]
    fn burn_tokens(amount: u64);

    #[storage(read)]
    fn get_total_supply() -> u64;
}

storage {
    total_supply: u64 = 0,
    balances: StorageMap<Identity, u64> = StorageMap {},
    owner: Identity = Identity::Address(Address::zero()),
    initialized: bool = false,
}

impl TokenContract for Contract {
    #[storage(read, write)]
    fn initialize(initial_supply: u64, owner: Identity) {
        require(!storage.initialized.read(), "Already initialized");

        storage.total_supply.write(initial_supply);
        storage.balances.insert(owner, initial_supply);
        storage.owner.write(owner);
        storage.initialized.write(true);

        log(InitializedEvent {
            owner,
            initial_supply,
        });
    }

    #[storage(read)]
    fn get_balance(target: Identity) -> u64 {
        match storage.balances.get(target).try_read() {
            Some(balance) => balance,
            None => 0,
        }
    }

    #[storage(read, write)]
    fn transfer_tokens(amount: u64, recipient: Identity) {
        let sender = msg_sender().unwrap();
        let sender_balance = Self::get_balance(sender);

        require(sender_balance >= amount, "Insufficient balance");

        storage.balances.insert(sender, sender_balance - amount);

        let recipient_balance = Self::get_balance(recipient);
        storage.balances.insert(recipient, recipient_balance + amount);

        log(TransferEvent {
            from: sender,
            to: recipient,
            amount,
        });
    }

    #[storage(read, write)]
    fn mint_tokens(amount: u64, recipient: Identity) {
        let sender = msg_sender().unwrap();
        require(sender == storage.owner.read(), "Only owner can mint");

        let current_supply = storage.total_supply.read();
        storage.total_supply.write(current_supply + amount);

        let recipient_balance = Self::get_balance(recipient);
        storage.balances.insert(recipient, recipient_balance + amount);

        log(MintEvent {
            to: recipient,
            amount,
        });
    }

    #[storage(read, write)]
    fn burn_tokens(amount: u64) {
        let sender = msg_sender().unwrap();
        let sender_balance = Self::get_balance(sender);

        require(sender_balance >= amount, "Insufficient balance");

        storage.balances.insert(sender, sender_balance - amount);

        let current_supply = storage.total_supply.read();
        storage.total_supply.write(current_supply - amount);

        log(BurnEvent {
            from: sender,
            amount,
        });
    }

    #[storage(read)]
    fn get_total_supply() -> u64 {
        storage.total_supply.read()
    }
}

struct InitializedEvent {
    owner: Identity,
    initial_supply: u64,
}

struct TransferEvent {
    from: Identity,
    to: Identity,
    amount: u64,
}

struct MintEvent {
    to: Identity,
    amount: u64,
}

struct BurnEvent {
    from: Identity,
    amount: u64,
}
