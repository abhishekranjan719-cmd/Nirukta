# Pre-Commit Hooks - Quick Start

**Setup Time:** 2 minutes
**Python Version:** 3.12
**Line Length:** 120 characters

---

## Automated Setup (Recommended)

```bash
# Run the setup script
./scripts/setup-pre-commit.sh
```

That's it! The script will:
1. Create Python 3.12 venv (if needed)
2. Install all dependencies
3. Install git hooks
4. (Optional) Test on all files

---

## Manual Setup

```bash
# 1. Create venv with Python 3.12
uv venv --python 3.12
source .venv/bin/activate

# 2. Install dependencies
uv pip install pre-commit ruff "bandit[toml]"

# 3. Install hooks
pre-commit install
pre-commit install --hook-type commit-msg

# 4. Test (optional)
pre-commit run --all-files
```

---

## Usage

### Automatic (on commit)

```bash
git add .
git commit -m "feat: add new feature"
# Hooks run automatically!
```

### Manual

```bash
# Run all hooks
pre-commit run --all-files

# Run specific hook
pre-commit run ruff --all-files

# Run on specific files
pre-commit run --files backend/app/config.py
```

---

## What's Included

✅ **Ruff** - Fast Python linter & formatter (replaces Black, Flake8, isort)
✅ **Security** - Hardcoded secrets detection, Bandit scanner
✅ **File checks** - YAML, JSON, TOML validation
✅ **Protection** - `.env` file commit blocking
✅ **Linting** - Markdown, Dockerfile checks

---

## Configuration

All configuration is in:
- `pyproject.toml` - Ruff & Bandit settings
- `.pre-commit-config.yaml` - Pre-commit hooks
- `.yamllint.yaml` - YAML rules
- `.markdownlint.yaml` - Markdown rules

**Key Setting:** Line length = 120 characters

---

## Common Commands

```bash
# Fix Python code style
ruff check . --fix

# Format Python code
ruff format .

# Check without fixing
ruff check .
ruff format --check .

# Update hooks
pre-commit autoupdate

# Skip hooks (emergency only!)
git commit --no-verify
```

---

## Troubleshooting

### "Command not found: pre-commit"

```bash
source .venv/bin/activate
```

### "Hooks too slow"

Ruff is already 10-100x faster than traditional tools!

### "Too many errors"

Auto-fix most of them:

```bash
ruff check . --fix
ruff format .
```

---

## Full Documentation

See [PRE_COMMIT_SETUP.md](./PRE_COMMIT_SETUP.md) for:
- Detailed configuration
- All hooks explained
- Performance benchmarks
- CI/CD integration
- Best practices

---

## Quick Reference

| Task | Command |
|------|---------|
| Setup | `./scripts/setup-pre-commit.sh` |
| Run all hooks | `pre-commit run --all-files` |
| Fix Python style | `ruff check . --fix && ruff format .` |
| Check formatting | `ruff format --check .` |
| Update hooks | `pre-commit autoupdate` |
| Skip hooks | `git commit --no-verify` |

---

**Need help?** Check [PRE_COMMIT_SETUP.md](./PRE_COMMIT_SETUP.md) or run `ruff --help`
