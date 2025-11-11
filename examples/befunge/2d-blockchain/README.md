# Befunge - 2D Blockchain Programming

<div align="center">

🎮 **Navigate the blockchain in two dimensions**

![Difficulty](https://img.shields.io/badge/Difficulty-2D%20Maze-orange)
![Type](https://img.shields.io/badge/Type-Grid%20Based-blue)
![Paradigm](https://img.shields.io/badge/Paradigm-Stack%20%2B%20Grid-green)

</div>

## 🎯 Overview

**Befunge** is a two-dimensional esoteric programming language created in 1993 by Chris Pressey. Unlike traditional languages that flow top-to-bottom, Befunge code is laid out on a 2D grid and the program counter can move in any direction (up, down, left, right)! This makes it perfect for visualizing blockchain concepts like Merkle trees and transaction paths.

## 📚 Language Features

### The 2D Grid

Befunge programs are written on an 80x25 character grid:

```
> v      "Hello"
  >:#,_@
```

The `>` means "move right", `v` means "move down", etc.

### The Stack

Befunge uses a **stack** for all data operations, similar to the EVM!

```
5        Push 5
3        Push 3
+        Pop 5 and 3, push 8
.        Pop and print 8
```

### Direction Commands

| Command | Direction | Description |
|---------|-----------|-------------|
| `>` | Right | Move east |
| `<` | Left | Move west |
| `^` | Up | Move north |
| `v` | Down | Move south |
| `?` | Random | Move randomly |
| `_` | Horizontal | Pop: if 0 go right, else left |
| `|` | Vertical | Pop: if 0 go down, else up |
| `#` | Bridge | Skip next cell |

### Stack Commands

| Command | Description |
|---------|-------------|
| `0-9` | Push number 0-9 |
| `+` | Add top two |
| `-` | Subtract top two |
| `*` | Multiply top two |
| `/` | Divide top two |
| `%` | Modulo top two |
| `:` | Duplicate top |
| `\` | Swap top two |
| `$` | Discard top |

### I/O Commands

| Command | Description |
|---------|-------------|
| `.` | Pop and output as number |
| `,` | Pop and output as ASCII |
| `&` | Input number |
| `~` | Input character |

### String Mode

| Command | Description |
|---------|-------------|
| `"` | Toggle string mode |
| Inside `" "` | Push ASCII values |

### Special Commands

| Command | Description |
|---------|-------------|
| `@` | End program |
| `p` | Put (modify code) |
| `g` | Get (read code) |
| ` ` (space) | No operation |

## 🚀 Examples

### 1. Hello Blockchain (`hello_blockchain.bf`)

```befunge
"!niahckcolB olleH">:#,_@
```

**How it works:**
```
"!niahckcolB olleH"  → Push "Hello Blockchain!" backwards (string mode)
>                    → Move right
:#,_                 → Loop: dup, skip if 0, output char, horizontal if
@                    → End
```

**Output:** `Hello Blockchain!`

**Visualization:**
```
Start → "!" → "n" → "i" → ... → "H" → > → Output loop → @
```

### 2. ETH Address (`eth_address.bf`)

```befunge
"x0" ,,    v
v "ETH: "  <
>"Address: ",,,,,,,,,@
```

**Path flow:**
```
1. Push "0x" and output
2. Move down, then left
3. Push " :HTE" (backwards)
4. Move down, then right
5. Push "Address: " and output
6. End
```

### 3. Gas Calculator (`gas_calculator.bf`)

```befunge
55+           Get 10 (5+5 = base fee)
3             Push 3 (priority)
+             Add them (total = 13)
:.            Duplicate and print
" iewg"       Push " gwei" backwards
,,,,,,        Print 5 chars
@             End
```

**Output:** `13 gwei`

**Stack trace:**
```
[] → [5] → [5,5] → [10] → [10,3] → [13] → [13,13]
→ print 13 → [13] → [13,'g','w','e','i',' ']
→ print " gwei"
```

### 4. Block Counter (`block_counter.bf`)

```befunge
0             v
v "Block #"   <
>:#v_":" ,,,,,,,@
   >:#._55+,^
```

**Execution path:**
```
1. Push 0, move down
2. Push "Block #" backwards, move left
3. Output loop for string
4. Output number and newline
```

### 5. Merkle Hash (`merkle_hash.bf`)

```befunge
v           Start
>"Hash: ",,,,,,v
v "x0"        <
>,,:          v
25*v          ^
v  <
>"..."   ,,,@
```

Displays a mock Merkle root hash.

## 💻 Running the Examples

### Using Online Interpreter

1. Visit [befunge.tryitonline.net](https://befunge.tryitonline.net/)
2. Paste the code
3. Click "Run"
4. Watch the path tracer!

### Using pyfunge (Python)

```bash
# Install
pip install pyfunge

# Run examples
pyfunge hello_blockchain.bf
pyfunge gas_calculator.bf
pyfunge block_counter.bf
```

### Using cfunge (C - fastest)

```bash
# Install
git clone https://github.com/VorpalBlade/cfunge
cd cfunge
mkdir build && cd build
cmake ..
make

# Run
./cfunge ../examples/hello_blockchain.bf
```

### Writing Your Own Interpreter

```python
#!/usr/bin/env python3

class BefungeInterpreter:
    def __init__(self, code):
        self.grid = [list(line.ljust(80)) for line in code.split('\n')]
        self.grid += [[' '] * 80 for _ in range(25 - len(self.grid))]
        self.stack = []
        self.x, self.y = 0, 0
        self.dx, self.dy = 1, 0  # Direction: right
        self.string_mode = False

    def run(self):
        while True:
            cmd = self.grid[self.y][self.x]

            if self.string_mode:
                if cmd == '"':
                    self.string_mode = False
                else:
                    self.stack.append(ord(cmd))
            else:
                if cmd == '@':
                    break
                elif cmd == '>':
                    self.dx, self.dy = 1, 0
                elif cmd == '<':
                    self.dx, self.dy = -1, 0
                elif cmd == '^':
                    self.dx, self.dy = 0, -1
                elif cmd == 'v':
                    self.dx, self.dy = 0, 1
                elif cmd.isdigit():
                    self.stack.append(int(cmd))
                elif cmd == '+':
                    b, a = self.pop(), self.pop()
                    self.stack.append(a + b)
                elif cmd == '-':
                    b, a = self.pop(), self.pop()
                    self.stack.append(a - b)
                elif cmd == '*':
                    b, a = self.pop(), self.pop()
                    self.stack.append(a * b)
                elif cmd == '.':
                    print(self.pop(), end='')
                elif cmd == ',':
                    print(chr(self.pop()), end='')
                elif cmd == ':':
                    val = self.pop()
                    self.stack.append(val)
                    self.stack.append(val)
                elif cmd == '"':
                    self.string_mode = True
                elif cmd == '#':
                    self.x += self.dx
                    self.y += self.dy

            # Move to next cell
            self.x += self.dx
            self.y += self.dy

    def pop(self):
        return self.stack.pop() if self.stack else 0

# Run
with open('hello_blockchain.bf', 'r') as f:
    BefungeInterpreter(f.read()).run()
```

## 🎓 Why Befunge for Blockchain?

### 2D Visualization

Befunge's 2D nature is perfect for visualizing:

#### 1. Merkle Trees
```befunge
      Root
     /    \
   H1      H2
  /  \    /  \
 L1  L2  L3  L4
```

Can be represented as actual 2D code!

#### 2. Transaction Flow
```befunge
Sender → Validation → Network → Block → Receiver
  ↓         ↓           ↓        ↓        ↓
```

#### 3. State Transitions
```befunge
State0 → Action1 → State1 → Action2 → State2
   ↓        ↓         ↓        ↓         ↓
```

### Stack-Based Like EVM

Both Befunge and EVM use stack-based execution:

```befunge
Befunge:  5 3 +  → [5,3] → [8]
EVM:      PUSH1 5 PUSH1 3 ADD → [5,3] → [8]
```

### Self-Modifying Code

Befunge can modify itself (`p` command) - similar to smart contracts modifying storage!

```befunge
25*"A"01p  ; Put 'A' at position (0,1)
```

## 🧩 Advanced Blockchain Concepts

### 1. Simple Hash Function

```befunge
v              Start
>& :9%         Input number, modulo 256
"Hash: " ,,,,,,, .@
```

### 2. Block Validation

```befunge
v              Block number input
>&:0`          Check if > 0
#v_"INVALID"  ,,,,,,,@
  >"VALID"    ,,,,,@
```

### 3. Gas Metering

```befunge
v              Initialize gas
>55* :         Start with 25 gas
1-             Deduct 1 per operation
:0`            Check if > 0
#v_"OUT OF GAS"@
  >...         Continue execution
```

### 4. Merkle Proof Path

```befunge
v                        Start
>"Left" ,,,, v           Go left branch
v     "Right"<           Go right branch
>,,,,,       v           Output
>"Root!" ,,,,,@          Reach root
```

## 📊 Comparison Table

| Feature | Befunge | Brainfuck | Whitespace | Solidity |
|---------|---------|-----------|------------|----------|
| Dimensions | 2D | 1D (tape) | 1D | 1D |
| Memory Model | Grid + Stack | Tape | Stack + Heap | Storage + Stack |
| Readability | Visual | Minimal | Invisible | High |
| Direction | 4-way | Left/Right | N/A | Top-down |
| Self-Modify | Yes | No | No | Storage only |

## 🌟 Complex Example: Counter Loop

```befunge
0              v     Initialize counter to 0
v "Block: "    <     Push string
>,,,,,,,             Output string
:.                   Duplicate and output number
55+,                 Output newline (10)
1+                   Increment counter
:5-                  Check if counter == 5
#v_                  If not 0, go left (loop)
@                    End program
```

**Output:**
```
Block: 0
Block: 1
Block: 2
Block: 3
Block: 4
```

## 🎯 Challenges

Try implementing:

1. **Fibonacci Sequence**: Generate block rewards
2. **Prime Checker**: Validate block numbers
3. **Base Converter**: Hex ↔ Decimal
4. **Checksum Calculator**: Simple hash validation
5. **2D Maze Solver**: Navigate transaction paths

## 📚 Resources

- [Befunge-93 Specification](https://github.com/catseye/Befunge-93)
- [Online Interpreter](https://befunge.tryitonline.net/)
- [Esolang Wiki](https://esolangs.org/wiki/Befunge)
- [Befunge-98 (Extended)](https://github.com/catseye/Funge-98)
- [Example Programs](https://github.com/catseye/Befunge-93/tree/master/eg)

## 💡 Fun Facts

- Created in **1993** by Chris Pressey
- Designed to be **hard to compile**
- First 2D esoteric language
- **Befunge-93** limited to 80x25 grid
- **Befunge-98** supports unlimited grid (Funge-space)
- Can write **quines** (self-replicating programs)
- Used in **code golf** competitions
- Name is nonsense word (like "befuddled")

## 🎨 ASCII Art Programs

Befunge can create ASCII art that's also executable code!

```befunge
 vv  <      <
    2
    ^  ^<
 >  >  ^
   NEAT!
```

## 🧪 Self-Modifying Example

```befunge
0"!dlroW ,olleH">:#,_@
```

This can be modified at runtime to change output!

## 🚧 Limitations

- **Grid Size**: Limited to 80x25 in Befunge-93
- **No Functions**: No subroutine calls (in 93)
- **Debugging**: Extremely difficult to trace
- **Performance**: Interpreted, not compiled
- **Tooling**: Minimal IDE support

## 🎯 Key Takeaways

1. **2D Thinking**: Problems can be visualized spatially
2. **Stack Machines**: Core to many VMs (EVM, WASM, JVM)
3. **Direction Control**: Program flow can be non-linear
4. **Self-Modification**: Code as data (like smart contracts)
5. **Minimalism**: Complex behavior from simple rules

## 🏆 Advanced: 2D Merkle Tree

```befunge
        v Root
       / \
      v   v
     H1   H2
    /  \  /  \
   v  v v  v
  L1 L2 L3 L4
```

Actual code:
```befunge
v               Root calculation
>55*            Left hash
>68*            Right hash
+               Combine
:.              Output root
@               End
```

---

<div align="center">

**"Think in two dimensions, execute in all directions"** 🎮

*Demonstrating that blockchain logic can flow any direction*

**Navigate wisely!** →↓←↑

![Befunge](https://img.shields.io/badge/Befunge-2D%20Programming-orange?style=for-the-badge)

</div>

## 🗺️ Appendix: Command Reference Card

```
DIRECTIONS       STACK           I/O         LOGIC
>  East          0-9  Push       .  Number   _  H-If
<  West          +    Add        ,  Char     |  V-If
^  North         -    Sub        &  In-Num   #  Bridge
v  South         *    Mul        ~  In-Chr   @  End
?  Random        /    Div
               %    Mod        MEMORY
               :    Dup        p  Put
               \    Swap       g  Get
               $    Pop        "  String
```

---

<div align="center">

**May your path be true and your stack never underflow!** 📚↑

</div>
