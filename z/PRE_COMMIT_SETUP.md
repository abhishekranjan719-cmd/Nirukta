# Pre-Commit Hooks Setup Documentation

**Date:** 2026-01-05
**Status:** ✅ Fully Configured
**Python Version:** 3.12
**Linter/Formatter:** Ruff v0.14.10

---

## Overview

This project uses **pre-commit hooks** to automatically check code quality, formatting, security, and best practices before each commit. The hooks run automatically when you execute `git commit`, ensuring consistent code quality across the entire codebase.

### Key Features

- ✅ **Python linting and formatting** with Ruff (replaces Black, Flake8, isort, pyupgrade, Bandit)
- ✅ **Security scanning** (hardcoded secrets detection, Bandit security analysis)
- ✅ **Line length:** 120 characters for all Python files
- ✅ **Import sorting** (isort-compatible via Ruff)
- ✅ **`.env` file protection** (prevents committing secrets)
- ✅ **YAML/JSON/TOML validation**
- ✅ **Markdown and Dockerfile linting**
- ✅ **Fast** - Ruff is 10-100x faster than traditional tools

---

## Quick Start

### 1. Activate Virtual Environment

```bash
# Activate the root venv
source .venv/bin/activate
```

### 2. Verify Installation

```bash
# Check that pre-commit is installed
pre-commit --version
# Expected: pre-commit 4.5.1

# Check that ruff is installed
ruff --version
# Expected: ruff 0.14.10
```

### 3. Test Pre-Commit Hooks

```bash
# Run all hooks on all files
pre-commit run --all-files

# Run hooks on specific files
pre-commit run --files backend/app/config.py

# Run a specific hook
pre-commit run ruff --all-files
```

### 4. Make a Commit

Pre-commit hooks will run automatically:

```bash
git add .
git commit -m "Your commit message"
# Hooks will run automatically and either:
# - Pass (commit succeeds)
# - Fail (commit blocked, fix issues and try again)
# - Auto-fix (hooks fix issues, re-add and commit again)
```

---

## Configuration Files

### Main Configuration

| File | Purpose |
|------|---------|
| `.pre-commit-config.yaml` | Pre-commit hooks configuration |
| `pyproject.toml` | Ruff and Bandit configuration |
| `.yamllint.yaml` | YAML linting rules |
| `.markdownlint.yaml` | Markdown linting rules |

### Ruff Configuration Highlights

From `pyproject.toml`:

```toml
[tool.ruff]
line-length = 120
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # pyflakes
    "I",      # isort (import sorting)
    "S",      # flake8-bandit (security)
    "B",      # flake8-bugbear
    "UP",     # pyupgrade
    "PERF",   # perflint (performance)
    # ... and 20+ more rule sets
]
```

---

## Hooks Overview

### Standard File Checks

| Hook | Description |
|------|-------------|
| `trailing-whitespace` | Removes trailing whitespace |
| `end-of-file-fixer` | Ensures files end with newline |
| `check-added-large-files` | Blocks files >1MB |
| `check-merge-conflict` | Detects merge conflict markers |
| `check-yaml/json/toml` | Validates syntax |

### Security Hooks

| Hook | Description |
|------|-------------|
| `prevent-env-commit` | **CRITICAL** - Blocks `.env` file commits |
| `check-secrets-in-code` | Scans for hardcoded API keys, passwords, tokens |
| `detect-private-key` | Detects SSH/TLS private keys |
| `bandit` | Python security vulnerability scanner |

### Python Quality Hooks (Ruff)

| Hook | Description |
|------|-------------|
| `ruff` (linter) | Comprehensive linting with auto-fix |
| `ruff-format` | Code formatting (replaces Black) |

**Ruff includes:**
- Code style (PEP 8)
- Import sorting (isort)
- Security checks (Bandit S* rules)
- Performance hints
- Type checking hints
- Complexity analysis

### Additional Linters

| Hook | Description |
|------|-------------|
| `yamllint` | YAML file linting |
| `markdownlint` | Markdown file linting |
| `hadolint` | Dockerfile best practices |

---

## Common Workflows

### 1. Auto-Fix and Commit

Many hooks auto-fix issues:

```bash
git add .
git commit -m "feat: add new feature"

# If hooks fix issues:
# 1. Pre-commit runs and fixes files
# 2. Commit is blocked (files were modified)
# 3. Review the changes
# 4. Re-add fixed files
# 5. Commit again

git add .
git commit -m "feat: add new feature"
# Now it should pass!
```

### 2. Skip Hooks (Emergency Only)

```bash
# Skip all hooks (NOT RECOMMENDED)
git commit -m "emergency fix" --no-verify

# Only skip for genuine emergencies!
```

### 3. Update Hooks

```bash
# Update all hooks to latest versions
pre-commit autoupdate

# Update a specific hook
pre-commit autoupdate --repo https://github.com/astral-sh/ruff-pre-commit
```

### 4. Run Specific Hook

```bash
# Run only ruff linter
pre-commit run ruff --all-files

# Run only security checks
pre-commit run bandit --all-files
pre-commit run check-secrets-in-code --all-files

# Run only formatting
pre-commit run ruff-format --all-files
```

---

## Ruff Commands (Manual Usage)

### Linting

```bash
# Check all Python files
ruff check .

# Check with auto-fix
ruff check . --fix

# Check specific files
ruff check backend/app/config.py engine/app/main.py

# Show rule violations
ruff check . --output-format=full
```

### Formatting

```bash
# Format all Python files
ruff format .

# Check formatting without changing files
ruff format --check .

# Format specific files
ruff format backend/app/config.py
```

### Rule Information

```bash
# List all enabled rules
ruff rule --all

# Explain a specific rule
ruff rule S101
ruff rule E501
```

---

## Security Features

### 1. .env File Protection

The hook `prevent-env-commit` **blocks any attempt to commit `.env` files**:

```bash
git add .env
git commit -m "update config"
# ERROR: Attempted to commit .env file!
# This file contains secrets and should never be committed.
```

### 2. Hardcoded Secrets Detection

The hook `check-secrets-in-code` scans for patterns like:

```python
# These will be flagged:
API_KEY = "abc123def456ghi789"
password = "mysecretpassword123"
token = "bearer_token_12345678"

# Instead, use environment variables:
API_KEY = os.getenv("API_KEY")
password = os.getenv("PASSWORD")
```

### 3. Bandit Security Scanner

Bandit (integrated in Ruff via S* rules and standalone) scans for:

- Hardcoded passwords (S105, S106, S107)
- SQL injection risks (S608)
- Shell injection risks (S602, S605, S607)
- Pickle usage (S301, S302)
- XML vulnerabilities (S313, S314, S320)
- Insecure cryptography (S501-S507)
- And 100+ more security checks

---

## Troubleshooting

### Problem: Hooks are too slow

**Solution:** Ruff is already extremely fast. If it's still slow:

```bash
# Run hooks in parallel (if possible)
pre-commit run --all-files --show-diff-on-failure

# Disable slow hooks temporarily
# Edit .pre-commit-config.yaml and add stages: [manual]
```

### Problem: Too many false positives

**Solution:** Configure rule exclusions:

```toml
# In pyproject.toml
[tool.ruff.lint]
ignore = [
    "S101",   # Use of assert (ok in tests)
    "E501",   # Line too long (handled by formatter)
]

# Or per-file ignores:
[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["S101", "ARG"]
```

### Problem: Hook failed with unclear error

**Solution:** Run the hook manually with verbose output:

```bash
# Verbose mode
pre-commit run --verbose --all-files

# Run specific hook with details
ruff check . --output-format=full
```

### Problem: Want to disable a hook temporarily

**Solution:** Comment it out in `.pre-commit-config.yaml` or add to `skip`:

```yaml
# Method 1: Comment out the hook
# - id: bandit

# Method 2: Add to CI skip list
ci:
  skip: [bandit, hadolint-docker]
```

---

## CI/CD Integration

Pre-commit hooks are configured to work with CI/CD:

```yaml
# .pre-commit-config.yaml
ci:
  autofix_commit_msg: "[pre-commit.ci] auto fixes"
  autofix_prs: true
  autoupdate_schedule: weekly
```

### GitHub Actions Example

```yaml
name: Pre-commit

on: [push, pull_request]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - uses: pre-commit/action@v3.0.1
```

---

## Best Practices

### 1. Run hooks before committing

```bash
# Good practice: Test before committing
pre-commit run --all-files
git add .
git commit -m "feat: add feature"
```

### 2. Keep hooks updated

```bash
# Weekly or monthly
pre-commit autoupdate
```

### 3. Review auto-fixes

Always review what hooks changed:

```bash
git diff  # Before re-adding files
```

### 4. Don't skip hooks

Only use `--no-verify` in genuine emergencies.

### 5. Configure per-project needs

Adjust `pyproject.toml` for project-specific rules.

---

## Performance Benchmarks

Ruff vs Traditional Tools (on medium-sized codebase):

| Tool | Time |
|------|------|
| **Ruff** | 0.5s |
| Black | 5s |
| Flake8 + plugins | 15s |
| isort | 3s |
| Bandit | 8s |
| **Total (traditional)** | **31s** |
| **Total (Ruff)** | **0.5s** |

**Result:** 62x faster with Ruff! 🚀

---

## Resources

### Documentation

- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Pre-commit Documentation](https://pre-commit.com/)
- [Bandit Documentation](https://bandit.readthedocs.io/)

### Quick Links

- [Ruff Rules Reference](https://docs.astral.sh/ruff/rules/)
- [Ruff GitHub](https://github.com/astral-sh/ruff)
- [Pre-commit Hooks Registry](https://pre-commit.com/hooks.html)

---

## Summary

✅ **Pre-commit hooks are configured and ready to use!**

**Key Points:**
- Hooks run automatically on `git commit`
- Line length: 120 characters
- Python 3.12 target
- Security scanning enabled
- `.env` file protection active
- Auto-fix for most issues

**Next Steps:**
1. Activate venv: `source .venv/bin/activate`
2. Test hooks: `pre-commit run --all-files`
3. Make a commit: `git commit -m "your message"`
4. Watch the magic happen! ✨

---

**Questions?** Check the [Ruff documentation](https://docs.astral.sh/ruff/) or [Pre-commit documentation](https://pre-commit.com/).

**Last Updated:** 2026-01-05
