#[starknet::contract]
mod ERC20Token {
    use starknet::ContractAddress;
    use starknet::get_caller_address;
    use core::integer::u256;

    #[storage]
    struct Storage {
        name: felt252,
        symbol: felt252,
        decimals: u8,
        total_supply: u256,
        balances: LegacyMap<ContractAddress, u256>,
        allowances: LegacyMap<(ContractAddress, ContractAddress), u256>,
    }

    #[event]
    #[derive(Drop, starknet::Event)]
    enum Event {
        Transfer: Transfer,
        Approval: Approval,
    }

    #[derive(Drop, starknet::Event)]
    struct Transfer {
        from: ContractAddress,
        to: ContractAddress,
        value: u256,
    }

    #[derive(Drop, starknet::Event)]
    struct Approval {
        owner: ContractAddress,
        spender: ContractAddress,
        value: u256,
    }

    #[constructor]
    fn constructor(
        ref self: ContractState,
        name: felt252,
        symbol: felt252,
        initial_supply: u256,
        recipient: ContractAddress
    ) {
        self.name.write(name);
        self.symbol.write(symbol);
        self.decimals.write(18);
        self.total_supply.write(initial_supply);
        self.balances.write(recipient, initial_supply);

        self.emit(Transfer {
            from: starknet::contract_address_const::<0>(),
            to: recipient,
            value: initial_supply
        });
    }

    #[external(v0)]
    fn transfer(ref self: ContractState, to: ContractAddress, amount: u256) -> bool {
        let caller = get_caller_address();
        self._transfer(caller, to, amount);
        true
    }

    #[external(v0)]
    fn approve(ref self: ContractState, spender: ContractAddress, amount: u256) -> bool {
        let caller = get_caller_address();
        self.allowances.write((caller, spender), amount);

        self.emit(Approval {
            owner: caller,
            spender: spender,
            value: amount
        });
        true
    }

    #[external(v0)]
    fn transfer_from(
        ref self: ContractState,
        from: ContractAddress,
        to: ContractAddress,
        amount: u256
    ) -> bool {
        let caller = get_caller_address();
        let current_allowance = self.allowances.read((from, caller));

        assert(current_allowance >= amount, 'Insufficient allowance');
        self.allowances.write((from, caller), current_allowance - amount);
        self._transfer(from, to, amount);
        true
    }

    #[external(v0)]
    fn balance_of(self: @ContractState, account: ContractAddress) -> u256 {
        self.balances.read(account)
    }

    #[external(v0)]
    fn allowance(
        self: @ContractState,
        owner: ContractAddress,
        spender: ContractAddress
    ) -> u256 {
        self.allowances.read((owner, spender))
    }

    #[external(v0)]
    fn total_supply(self: @ContractState) -> u256 {
        self.total_supply.read()
    }

    fn _transfer(
        ref self: ContractState,
        from: ContractAddress,
        to: ContractAddress,
        amount: u256
    ) {
        let from_balance = self.balances.read(from);
        assert(from_balance >= amount, 'Insufficient balance');

        self.balances.write(from, from_balance - amount);
        let to_balance = self.balances.read(to);
        self.balances.write(to, to_balance + amount);

        self.emit(Transfer { from, to, value: amount });
    }
}
