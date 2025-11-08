/**
 * @title Ultra-Optimized Storage Contract in Yul
 * @notice Demonstrates low-level EVM programming with maximum gas efficiency
 * @dev Pure Yul implementation without Solidity wrapper
 */

object "Storage" {
    code {
        // Constructor code
        datacopy(0, dataoffset("runtime"), datasize("runtime"))
        return(0, datasize("runtime"))
    }

    object "runtime" {
        code {
            // Dispatcher: route calls based on function selector
            switch selector()

            // store(uint256) - 0x6057361d
            case 0x6057361d {
                let value := calldataload(0x04)
                sstore(0, value)
                emitStored(value)
            }

            // retrieve() - 0x2e64cec1
            case 0x2e64cec1 {
                let value := sload(0)
                returnUint(value)
            }

            // increment() - 0xd09de08a
            case 0xd09de08a {
                let oldValue := sload(0)
                let newValue := add(oldValue, 1)

                // Check for overflow
                if lt(newValue, oldValue) {
                    revertWithMessage("Overflow")
                }

                sstore(0, newValue)
                emitIncremented(oldValue, newValue)
            }

            // decrement() - 0x2baeceb7
            case 0x2baeceb7 {
                let oldValue := sload(0)

                // Check for underflow
                if iszero(oldValue) {
                    revertWithMessage("Underflow")
                }

                let newValue := sub(oldValue, 1)
                sstore(0, newValue)
                emitDecremented(oldValue, newValue)
            }

            // multiply(uint256) - 0xc8a4ac9c
            case 0xc8a4ac9c {
                let multiplier := calldataload(0x04)
                let oldValue := sload(0)
                let newValue := mul(oldValue, multiplier)

                // Check for overflow
                if and(iszero(iszero(multiplier)), iszero(eq(div(newValue, multiplier), oldValue))) {
                    revertWithMessage("Overflow")
                }

                sstore(0, newValue)
                emitMultiplied(oldValue, newValue, multiplier)
            }

            // Default: revert on unknown function
            default {
                revert(0, 0)
            }

            // Helper: extract function selector from calldata
            function selector() -> s {
                s := div(calldataload(0), 0x100000000000000000000000000000000000000000000000000000000)
            }

            // Helper: return a uint256 value
            function returnUint(value) {
                mstore(0, value)
                return(0, 0x20)
            }

            // Helper: revert with error message
            function revertWithMessage(message) {
                let length := mload(message)
                let offset := add(message, 0x20)
                revert(offset, length)
            }

            // Event: ValueStored(uint256 value)
            function emitStored(value) {
                mstore(0, value)
                log1(0, 0x20, 0x93fe6d397c74fdf1402a8b72e47b68512f0510d7b98a4bc4cbdf6ac7108b3c59)
            }

            // Event: ValueIncremented(uint256 oldValue, uint256 newValue)
            function emitIncremented(oldValue, newValue) {
                mstore(0, oldValue)
                mstore(0x20, newValue)
                log1(0, 0x40, 0x35f03c6e4cb3b14293ffb8d6b0e0e0e0c0e0e0e0e0e0e0e0e0e0e0e0e0e0e001)
            }

            // Event: ValueDecremented(uint256 oldValue, uint256 newValue)
            function emitDecremented(oldValue, newValue) {
                mstore(0, oldValue)
                mstore(0x20, newValue)
                log1(0, 0x40, 0x35f03c6e4cb3b14293ffb8d6b0e0e0e0c0e0e0e0e0e0e0e0e0e0e0e0e0e0e002)
            }

            // Event: ValueMultiplied(uint256 oldValue, uint256 newValue, uint256 multiplier)
            function emitMultiplied(oldValue, newValue, multiplier) {
                mstore(0, oldValue)
                mstore(0x20, newValue)
                mstore(0x40, multiplier)
                log1(0, 0x60, 0x35f03c6e4cb3b14293ffb8d6b0e0e0e0c0e0e0e0e0e0e0e0e0e0e0e0e0e0e003)
            }
        }
    }
}
