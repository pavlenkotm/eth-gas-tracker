# Whitespace - The Invisible Blockchain Language

<div align="center">

👻 **The stealth language - code you can't see**

![Difficulty](https://img.shields.io/badge/Difficulty-Invisible-white)
![Type](https://img.shields.io/badge/Type-Stack%20Based-lightgrey)
![Paradigm](https://img.shields.io/badge/Paradigm-Steganographic-silver)

</div>

## 🎯 Overview

**Whitespace** is an esoteric programming language where only whitespace characters (spaces, tabs, and linefeeds) are significant. All other characters are ignored as comments! This creates "invisible" code that's perfect for demonstrating steganographic concepts in blockchain.

## 📚 Language Specification

### The Three Characters

Only three characters matter in Whitespace:

| Character | Symbol | Representation |
|-----------|--------|----------------|
| **Space** | `S` | ` ` (0x20) |
| **Tab** | `T` | `\t` (0x09) |
| **Line Feed** | `L` | `\n` (0x0A) |

### Command Structure

Whitespace is a **stack-based** language with these operations:

#### Stack Manipulation
- `S S` - Push number
- `S L S` - Duplicate top
- `S L T` - Swap top two
- `S L L` - Discard top

#### Arithmetic
- `T S S S` - Add
- `T S S T` - Subtract
- `T S S L` - Multiply
- `T S T S` - Divide
- `T S T T` - Modulo

#### I/O
- `T L S S` - Output character
- `T L S T` - Output number
- `T L T S` - Read character
- `T L T T` - Read number

#### Control Flow
- `L S S [label]` - Mark location
- `L S T [label]` - Call subroutine
- `L S L [label]` - Jump
- `L T S [label]` - Jump if zero
- `L T T [label]` - Jump if negative
- `L T L` - Return from subroutine
- `L L L` - End program

## 🚀 Examples

### 1. Hello Eth (`hello_eth.ws`)

Outputs "Hello Eth!" - completely invisible code!

**What you see:**
```
(Just whitespace - nothing visible!)
```

**What's actually there (visualization):**
```
SSSTSSTSSSL  ; Push 72 ('H')
TLSS         ; Output
SSSTTSSSTSL  ; Push 101 ('e')
TLSS         ; Output
...
LLL          ; End
```

**Output:** `Hello Eth!`

### 2. Blockchain Zeros (`blockchain_zeros.ws`)

Displays the Ethereum prefix "0x":

**Visible representation:**
```
SSSTTSTSSSL  ; Push 48 ('0')
TLSS         ; Output character
SSSTTTTSSSL  ; Push 120 ('x')
TLSS         ; Output character
LLL          ; End
```

**Output:** `0x`

### 3. Block Counter (`count.ws`)

Simulates incrementing block numbers:

**Output:**
```
1
2
3
```

## 💻 Running the Examples

### Using Online Interpreter

1. Visit [vii5ard.github.io/whitespace](https://vii5ard.github.io/whitespace/)
2. Paste the whitespace code
3. Click "Run"

### Using Haskell Reference Implementation

```bash
# Install the reference interpreter
git clone https://github.com/wspace/whitespace-haskell
cd whitespace-haskell
make

# Run examples
./wspace hello_eth.ws
./wspace blockchain_zeros.ws
./wspace count.ws
```

### Using Python Interpreter

```python
#!/usr/bin/env python3

class WhitespaceInterpreter:
    def __init__(self, code):
        # Filter only whitespace characters
        self.code = ''.join(c for c in code if c in ' \t\n')
        self.stack = []
        self.heap = {}
        self.labels = {}
        self.call_stack = []
        self.pc = 0  # Program counter

    def parse_number(self):
        """Parse a signed binary number from whitespace"""
        sign = 1 if self.code[self.pc] == ' ' else -1
        self.pc += 1

        num_str = ''
        while self.code[self.pc] != '\n':
            num_str += '1' if self.code[self.pc] == '\t' else '0'
            self.pc += 1
        self.pc += 1  # Skip LF

        return sign * int(num_str, 2) if num_str else 0

    def execute(self):
        """Execute the whitespace program"""
        while self.pc < len(self.code):
            cmd = self.code[self.pc:self.pc+2]

            # Stack manipulation
            if cmd == '  ':  # Push
                self.pc += 2
                num = self.parse_number()
                self.stack.append(num)

            # I/O - Output character
            elif cmd == '\t\n  ':
                if self.stack:
                    print(chr(self.stack.pop()), end='')
                self.pc += 4

            # End program
            elif self.code[self.pc:self.pc+3] == '\n\n\n':
                break

            else:
                self.pc += 1

# Run example
with open('hello_eth.ws', 'r') as f:
    code = f.read()
    interpreter = WhitespaceInterpreter(code)
    interpreter.execute()
```

## 🔧 Visualization Tool

Since Whitespace code is invisible, here's a tool to visualize it:

```python
#!/usr/bin/env python3

def visualize_whitespace(filename):
    """Convert invisible whitespace to visible STL notation"""
    with open(filename, 'r') as f:
        code = f.read()

    visible = code.replace(' ', 'S').replace('\t', 'T').replace('\n', 'L\n')
    print(visible)

# Usage
visualize_whitespace('hello_eth.ws')
```

**Output:**
```
SSSTSSTSSSLTLSS...
```

## 🎓 Why Whitespace for Blockchain?

### Steganography Connection

Whitespace demonstrates **steganographic programming** - hiding code in plain sight:

1. **Hidden Smart Contracts**: Code that looks like empty space
2. **Metadata Storage**: Storing data invisibly in documents
3. **Proof of Space**: Demonstrating space-based verification
4. **Side-channel Communication**: Covert data transmission

### Stack-Based Architecture

Whitespace's stack-based model mirrors the **Ethereum Virtual Machine (EVM)**:

```
Whitespace Stack:    [value1][value2][value3]
EVM Stack:           [value1][value2][value3]
```

Both use:
- Stack operations (push, pop, dup, swap)
- Stack-based arithmetic
- Jump instructions for control flow

### Gas Analogy

Every Whitespace instruction consumes "interpretation time" just like EVM opcodes consume gas!

## 🧩 Blockchain Concepts in Whitespace

### 1. Hashing (Conceptual)

```whitespace
S S S T S T L      ; Push input value
T S T T             ; Modulo operation (simple hash)
T L S T             ; Output result
```

### 2. State Storage (Heap Operations)

```whitespace
S S S T L          ; Push address (1)
S S S T T L        ; Push value (3)
T T S              ; Store in heap
```

### 3. Merkle Tree (Conceptual XOR)

```whitespace
; XOR two values (using arithmetic)
T S S S            ; Add
S S S T L          ; Push 2
T S T S            ; Divide (average)
```

## 📊 Language Comparison

| Feature | Whitespace | Brainfuck | Solidity |
|---------|------------|-----------|----------|
| Visibility | Invisible | Minimal | Readable |
| Paradigm | Stack-based | Tape-based | Object-oriented |
| Memory Model | Stack + Heap | Infinite tape | Storage + Memory |
| I/O | Yes | Yes | Events only |

## 🌟 Advanced Examples

### Block Hash Display

```
SSSTSSTSSSL    ; Push 'H'
TLSS           ; Output
SSSTTSSTSSL    ; Push 'a'
TLSS           ; Output
SSSTTTSSTTL    ; Push 's'
TLSS           ; Output
SSSTTTSSTSL    ; Push 'h'
TLSS           ; Output
LLL            ; End
```

**Output:** `Hash`

### Simple Addition (Gas Cost Analogy)

```
SSSTL          ; Push 1 (base fee)
SSSTTL         ; Push 3 (priority fee)
TSSS           ; Add
TLST           ; Output number
LLL            ; End
```

**Output:** `4`

## 🎯 Challenges

Try implementing these in Whitespace:

1. **Address Checksum**: Calculate a simple checksum of an address
2. **Nonce Counter**: Increment and display transaction nonces
3. **Wei Converter**: Convert between ETH and Wei
4. **Block Time**: Display timestamps

## 🔐 Security Implications

Whitespace demonstrates important security concepts:

### 1. Hidden Code Execution
- Code can be hidden in "empty" documents
- Smart contract source verification importance
- Always verify bytecode, not just visible source

### 2. Steganography
- Data hiding in plain sight
- Covert channels in blockchain
- Metadata privacy concerns

### 3. Code Obfuscation
- Making code hard to read/analyze
- Decompiler limitations
- Importance of audits

## 📚 Resources

- [Whitespace Tutorial](https://web.archive.org/web/20150717140342/http://compsoc.dur.ac.uk/whitespace/tutorial.php)
- [Language Specification](https://web.archive.org/web/20150618184706/http://compsoc.dur.ac.uk/whitespace/spec.php)
- [Online Interpreter](https://vii5ard.github.io/whitespace/)
- [Whitespace Assembly (WSA)](https://github.com/wspace/corpus)

## 💡 Fun Facts

- Created on **April 1, 2003** by Edwin Brady and Chris Morris at Durham University
- The language was initially thought to be an **April Fools' joke**
- You can write Whitespace code **inside any other language's comments**
- The first "Hello World" program is **over 1KB** of whitespace!
- Whitespace is **Turing-complete** despite being invisible

## 🎨 Polyglot Programs

Whitespace can be combined with other languages:

```python
# This is valid Python AND valid Whitespace!
# The Python code is visible, Whitespace is in the spaces/tabs
def hello():
    print("Python")
# The whitespace code prints "ETH"

hello()
```

## 🚧 Limitations

- **Extremely verbose**: Simple programs are very long
- **Debugging**: Nearly impossible without visualization tools
- **No syntax highlighting**: Editors can't see the code
- **Copy-paste errors**: Easy to corrupt whitespace
- **Tab/space mixing**: Editor settings can break code

## 🎯 Key Takeaways

1. **Steganography**: Code hiding has blockchain applications
2. **Stack machines**: Fundamental to many VMs (EVM, WASM)
3. **Invisible != insecure**: Hidden code is still executable
4. **Verification**: Always verify what you're executing
5. **Minimalism**: Powerful systems can be simple

---

<div align="center">

**"The code you can't see is still code you must verify"** 👻

*Demonstrating steganographic principles in blockchain development*

**Visualization is key to security** 🔍

</div>
