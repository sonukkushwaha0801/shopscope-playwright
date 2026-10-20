"""Shared pytest fixtures and diagnostics for browser tests."""

from collections.abc import Generator
from pathlib import Path

import pytest

from shopscope.config import Settings
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright

ROOT = Path(__file__).resolve().parent
DEMO_STORE = ROOT / "tests" / "fixtures" / "demo_store.html"


@pytest.fixture(scope="session")
def settings() -> Settings:
    config = Settings.from_env()
    config.validate()
    return config


@pytest.fixture(scope="session")
def playwright_instance() -> Generator[Playwright, None, None]:
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(
    playwright_instance: Playwright, settings: Settings
) -> Generator[Browser, None, None]:
    browser_type = getattr(playwright_instance, settings.browser)
    instance = browser_type.launch(headless=settings.headless)
    yield instance
    instance.close()


@pytest.fixture
def context(browser: Browser) -> Generator[BrowserContext, None, None]:
    browser_context = browser.new_context(viewport={"width": 1440, "height": 900})
    yield browser_context
    browser_context.close()


@pytest.fixture
def page(
    context: BrowserContext, request: pytest.FixtureRequest, settings: Settings
) -> Generator[Page, None, None]:
    current_page = context.new_page()
    current_page.set_default_timeout(settings.action_timeout_ms)
    current_page.set_default_navigation_timeout(settings.navigation_timeout_ms)
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    yield current_page

    report = getattr(request.node, "rep_call", None)
    failed = report is not None and report.failed
    if failed:
        artifacts = Path(settings.artifacts_dir)
        artifacts.mkdir(parents=True, exist_ok=True)
        safe_name = "".join(
            character if character.isalnum() or character in "-_" else "_"
            for character in request.node.nodeid
        )
        current_page.screenshot(
            path=str(artifacts / f"{safe_name}.png"),
            full_page=True,
        )
        context.tracing.stop(path=str(artifacts / f"{safe_name}.trace.zip"))
    else:
        context.tracing.stop()
    current_page.close()


@pytest.fixture
def demo_store_url() -> str:
    """Return a file URL for the bundled local storefront."""
    return DEMO_STORE.as_uri()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item, call: pytest.CallInfo[object]
) -> Generator[None, None, None]:
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)
