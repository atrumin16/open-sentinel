# Contributing to OpenSentinel

Thank you for your interest in contributing to **OpenSentinel**, the self-hosted defensive telemetry and forensics suite.

---

## Code of Conduct
Please maintain professional, constructive, and zero-trust engineering standards across all interactions and technical reviews.

---

## Development Setup

Clone the repository and prepare your local virtual environment:

```bash
git clone https://github.com/atrumin16/open-sentinel.git
cd open-sentinel
python -m venv venv

# Windows PowerShell:
venv\Scripts\Activate.ps1

# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
pip install bandit flake8
```

---

## Pre-Commit Verification & Security Checklist

Before opening a Pull Request, verify your changes against our Zero-Trust standards:

### 1. Bytecode Compilation
Ensure all modified Python modules compile cleanly with zero syntax warnings:
```bash
python -m py_compile main.py
python -m py_compile src/**/*.py
```

### 2. Local SAST Security Audit
Run Bandit to check for common Common Weakness Enumerations (CWE):
```bash
bandit -r src/ main.py -ll
```

### 3. Secret Leak Prevention
- Never commit active API keys, Discord webhooks, Telegram bot tokens, or private `.pem` keys.
- Store test credentials exclusively in `.env` (which is gitignored).

---

## Pull Request Guidelines

1. Create a focused feature branch from `main`:
   ```bash
   git checkout -b feat/your-capability
   ```
2. Adhere to Conventional Commits (`feat:`, `fix:`, `sec:`, `docs:`, `ci:`).
3. If pair programming or using AI-assisted tooling (e.g. Claude Code), include the official co-authorship trailer:
   ```text
   Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
   ```
4. Open your Pull Request and ensure the automated Sentinel CI pipeline passes.
