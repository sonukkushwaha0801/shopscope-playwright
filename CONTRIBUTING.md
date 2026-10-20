# Contributing to ShopScope

Thanks for helping improve ShopScope. Keep changes small, testable, and aligned with the project's safety boundaries.

## Development setup

Use Python 3.12 or newer. From the repository root, create and activate a virtual environment, then install the project:

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test,dev]"
python -m playwright install chromium
```

If activation is restricted by local policy, use `.venv\Scripts\python.exe` instead of changing the PowerShell execution policy.

## Before opening a pull request

```powershell
python -m pytest tests/unit
python -m pytest tests/e2e
ruff check .
```

- Explain the problem and intended behavior.
- Add or update tests for behavior changes.
- Keep retailer-specific behavior out of shared core modules.
- Never commit credentials, cookies, authenticated browser state, or unreviewed test artifacts.
- Do not add CAPTCHA evasion, stealth, access-control circumvention, or rate-limit bypasses.
- Do not make real purchases in tests.
- Keep CI green and document environment-specific limitations.

## Code conventions

- Prefer type hints for public interfaces.
- Use Playwright auto-waiting and web-first assertions instead of arbitrary sleeps.
- Use `Decimal` for monetary values.
- Keep configuration explicit and validate it early.
