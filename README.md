# ShopScope

**Explore. Automate. Analyze.**

A reusable Python Playwright framework for e-commerce UI automation, multi-retailer testing, and future price-tracking integrations for Amazon India and Flipkart.

> **Project status:** Planning and foundation. Retailer-specific live-site automation and price monitoring are not part of the initial implementation.

## Goals

- Build a maintainable, reusable UI automation framework with Python, Playwright, and pytest.
- Separate shared test infrastructure from retailer-specific page objects and workflows.
- Make configuration, browser lifecycle, reporting, logging, and failure artifacts consistent.
- Keep any future price-tracking capability behind a provider interface so it can evolve independently of UI tests.
- Add CI and container support after the local test foundation is stable.

## Initial scope

The first implementation will focus on framework fundamentals and deterministic tests against a controlled or explicitly authorized test application:

- Typed, centralized configuration and environment-specific settings.
- pytest fixtures for Playwright, browser contexts, pages, and cleanup.
- Page-object and component patterns with explicit, robust locators.
- Reusable assertions and test data.
- Screenshots, traces, logs, and test reports on failure.
- A retailer-adapter boundary for future authorized integrations.
- Later milestones for GitHub Actions and Docker.

## Retailer and data-use boundaries

Amazon India and Flipkart are the intended learning context, but their live sites are not assumed to be authorized automation targets. Before building retailer-specific automation or collecting prices, verify the applicable terms and use an approved API, licensed data source, or explicit permission where required.

This project will not implement CAPTCHA evasion, stealth techniques, access-control circumvention, or rate-limit bypasses. It will not make real purchases. Checkout-related testing, if ever added, must use a controlled environment and test data.

A future price tracker should consume a documented provider interface rather than depend on selectors embedded in the core framework.

## Proposed architecture

The structure below is a target direction, not a claim that these modules already exist.

```text
shopscope-playwright/
├── config/
│   └── settings.py          # Centralized configuration
├── shopscope/
│   ├── core/                # Browser and shared framework services
│   ├── pages/               # Reusable page abstractions
│   ├── components/          # Reusable UI components
│   ├── adapters/            # Separate, authorized site integrations
│   └── tracking/            # Future provider-based price tracking
├── tests/
│   ├── unit/
│   └── e2e/
├── test-data/
├── reports/                 # Generated locally; do not commit artifacts
├── conftest.py
├── pytest.ini
├── pyproject.toml
├── .env.example
├── .gitignore
└── README.md
```

We will introduce folders only when there is a real need for them; the design should not become abstraction-heavy before the first tests work.

## Milestones

- [ ] **M0 — Define the foundation:** confirm local OS and Python environment; establish project conventions.
- [ ] **M1 — Bootstrap:** create the package, dependency configuration, pytest setup, and a minimal passing test.
- [ ] **M2 — Core framework:** add Playwright fixtures, configuration, and reliable browser lifecycle management.
- [ ] **M3 — Quality and diagnostics:** add logging, screenshots, traces, and useful failure reporting.
- [ ] **M4 — Page-object patterns:** validate reusable pages/components against a controlled test application.
- [ ] **M5 — Retailer adapters:** evaluate permitted integration options before writing any retailer-specific behavior.
- [ ] **M6 — CI and containers:** run tests in GitHub Actions and optionally Docker.
- [ ] **M7 — Price-tracking extension:** add a provider-based design only after an approved data source is identified.

## Development principles

1. Prefer Playwright's auto-waiting and web-first assertions over arbitrary sleeps.
2. Keep selectors and site-specific assumptions out of shared framework code.
3. Use environment variables for configuration and secrets; never commit credentials, cookies, or session state.
4. Make tests deterministic, independent, and safe to rerun.
5. Capture enough diagnostics to debug a failure without leaking sensitive data.

## Planned tooling

- Python
- Playwright for Python
- pytest
- pytest-playwright and/or project-owned fixtures, chosen during bootstrap
- Ruff for linting/formatting
- GitHub Actions for CI (later milestone)

Dependency versions and setup commands will be pinned and verified during the bootstrap milestone.

## License

No license has been added yet. Until a license is selected and committed, reuse and redistribution permissions should not be assumed.
