# Contributing to Web3 Multi-Language Playground

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## 🎯 How to Contribute

### 1. Fork & Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/eth-gas-tracker.git
cd eth-gas-tracker

# Add upstream remote
git remote add upstream https://github.com/pavlenkotm/eth-gas-tracker.git
```

### 2. Create a Branch

```bash
# Create a new branch for your feature/fix
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### 3. Make Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new features
- Update documentation as needed

### 4. Commit Changes

Use conventional commit messages:

```bash
git commit -m "feat(solidity): add staking contract example"
git commit -m "fix(rust): correct anchor program initialization"
git commit -m "docs(readme): update installation instructions"
git commit -m "test(move): add integration tests for coin module"
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `style`: Code style changes (formatting, etc.)
- `chore`: Maintenance tasks

### 5. Push & Create Pull Request

```bash
# Push your branch
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

## 📝 Pull Request Guidelines

### PR Title Format

```
<type>(<scope>): <short description>

Examples:
feat(typescript): add NFT marketplace example
fix(go): resolve race condition in RPC client
docs(contributing): update contribution guidelines
```

### PR Description Template

```markdown
## Description
Brief description of the changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing
Describe the tests you ran

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix/feature works
- [ ] New and existing tests pass locally
```

## 🎨 Code Style Guidelines

### General

- Use consistent indentation (2 or 4 spaces, depending on language)
- Write descriptive variable and function names
- Keep functions small and focused
- Add comments for complex logic
- Remove commented-out code before committing

### Language-Specific

#### Solidity
```solidity
// Use NatSpec comments
/**
 * @notice Transfer tokens to a recipient
 * @param recipient The address to receive tokens
 * @param amount The amount of tokens to transfer
 */
function transfer(address recipient, uint256 amount) public returns (bool) {
    // Implementation
}
```

#### Rust
```rust
// Follow Rust naming conventions
// Use descriptive names and add documentation
/// Processes a counter increment
pub fn increment(ctx: Context<Update>) -> Result<()> {
    // Implementation
}
```

#### TypeScript
```typescript
// Use TypeScript types
// Follow ESLint rules
interface WalletConnection {
  address: string;
  chainId: number;
}

const connectWallet = async (): Promise<WalletConnection> => {
  // Implementation
};
```

## 🧪 Testing Requirements

### All Examples Must Include:

1. **Unit Tests**: Test individual functions/methods
2. **Integration Tests**: Test component interactions
3. **Documentation**: Explain how to run tests

### Example Test Commands

```bash
# Solidity/Hardhat
npx hardhat test

# Rust/Anchor
anchor test

# TypeScript
npm test

# Python
pytest

# Go
go test ./...
```

## 📚 Documentation Requirements

### Each New Example Must Include:

1. **README.md** with:
   - Description of the example
   - Prerequisites
   - Installation instructions
   - Usage examples
   - Testing instructions
   - Common issues and solutions

2. **Code Comments**:
   - Function/method documentation
   - Complex logic explanations
   - TODO comments for future improvements

3. **Examples**:
   - Working code examples
   - Configuration examples
   - Usage scenarios

## 🐛 Bug Reports

### Before Submitting

- Check existing issues
- Verify it's actually a bug
- Collect relevant information

### Bug Report Template

```markdown
## Bug Description
Clear and concise description

## To Reproduce
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. See error

## Expected Behavior
What you expected to happen

## Screenshots
If applicable

## Environment
- OS: [e.g., macOS 12.0]
- Node version: [e.g., 18.0.0]
- Other relevant info

## Additional Context
Any other information
```

## ✨ Feature Requests

### Feature Request Template

```markdown
## Feature Description
Clear and concise description

## Motivation
Why is this feature needed?

## Proposed Solution
How should it work?

## Alternatives Considered
Other approaches you've thought about

## Additional Context
Any other information
```

## 🎯 Adding New Language Examples

### Structure

```
examples/
└── new-language/
    └── example-name/
        ├── README.md
        ├── src/
        ├── tests/
        └── package/config files
```

### Requirements

1. **Working Code**: Must compile/run without errors
2. **Tests**: Include test suite
3. **Documentation**: Comprehensive README
4. **Dependencies**: List all dependencies
5. **License**: Must be MIT-compatible

### Example README Template

````markdown
# 🎯 [Language] [Example Name]

Brief description

## Features
- Feature 1
- Feature 2

## Prerequisites
- Dependency 1
- Dependency 2

## Installation

```bash
# Installation commands
```

## Usage

```bash
# Usage examples
```

## Testing

```bash
# Test commands
```

## License
MIT License
````

## 🔍 Code Review Process

### What Reviewers Look For

1. **Correctness**: Does the code work as intended?
2. **Tests**: Are there adequate tests?
3. **Documentation**: Is it well-documented?
4. **Style**: Does it follow style guidelines?
5. **Security**: Are there security concerns?
6. **Performance**: Are there performance issues?

### Responding to Reviews

- Be respectful and professional
- Address all feedback
- Explain your reasoning if you disagree
- Update your PR based on feedback
- Thank reviewers for their time

## 🚀 Release Process

### Version Numbering

We follow [Semantic Versioning](https://semver.org/):
- MAJOR: Breaking changes
- MINOR: New features (backwards-compatible)
- PATCH: Bug fixes

### Changelog

Update CHANGELOG.md with:
- New features
- Bug fixes
- Breaking changes
- Deprecations

## 💬 Communication

### Where to Ask Questions

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Bug reports and feature requests
- **Pull Requests**: Code-specific discussions

### Response Times

- We aim to respond within 48 hours
- Complex issues may take longer
- Be patient and respectful

## 🎖️ Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

## 📜 Code of Conduct

Please read and follow our [Code of Conduct](./CODE_OF_CONDUCT.md).

## 🙏 Thank You!

Your contributions help make Web3 development more accessible to everyone. We appreciate your time and effort!

---

**Questions?** Open a [Discussion](https://github.com/pavlenkotm/eth-gas-tracker/discussions) or [Issue](https://github.com/pavlenkotm/eth-gas-tracker/issues).
