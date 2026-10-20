"""Tests for environment-based runtime settings."""

import pytest

from shopscope.config import Settings


@pytest.fixture(autouse=True)
def clean_settings_environment(monkeypatch):
    for key in (
        "SHOP_SCOPE_ENV",
        "SHOP_SCOPE_BROWSER",
        "SHOP_SCOPE_HEADLESS",
        "SHOP_SCOPE_BASE_URL",
        "SHOP_SCOPE_NAV_TIMEOUT_MS",
        "SHOP_SCOPE_ACTION_TIMEOUT_MS",
        "SHOP_SCOPE_ARTIFACTS_DIR",
    ):
        monkeypatch.delenv(key, raising=False)


def test_default_settings_are_valid() -> None:
    settings = Settings.from_env()
    settings.validate()

    assert settings.browser == "chromium"
    assert settings.headless is True
    assert settings.navigation_timeout_ms == 15_000
    assert settings.action_timeout_ms == 5_000


@pytest.mark.parametrize("browser", ["invalid", "chrome", ""])
def test_invalid_browser_is_rejected(monkeypatch, browser: str) -> None:
    monkeypatch.setenv("SHOP_SCOPE_BROWSER", browser)
    with pytest.raises(ValueError, match="Unsupported browser"):
        Settings.from_env().validate()


@pytest.mark.parametrize("value", ["0", "-1", "fast"])
def test_invalid_navigation_timeout_is_rejected(monkeypatch, value: str) -> None:
    monkeypatch.setenv("SHOP_SCOPE_NAV_TIMEOUT_MS", value)
    with pytest.raises(ValueError, match="SHOP_SCOPE_NAV_TIMEOUT_MS"):
        Settings.from_env()


@pytest.mark.parametrize("value", ["maybe", "enabled", "2"])
def test_invalid_headless_value_is_rejected(monkeypatch, value: str) -> None:
    monkeypatch.setenv("SHOP_SCOPE_HEADLESS", value)
    with pytest.raises(ValueError, match="SHOP_SCOPE_HEADLESS"):
        Settings.from_env()


@pytest.mark.parametrize(
    "url",
    ["file:///tmp/page.html", "localhost:8000", "https:///missing-host"],
)
def test_invalid_base_url_is_rejected(monkeypatch, url: str) -> None:
    monkeypatch.setenv("SHOP_SCOPE_BASE_URL", url)
    with pytest.raises(ValueError, match="absolute HTTP or HTTPS URL"):
        Settings.from_env().validate()


def test_false_headless_value_is_parsed(monkeypatch) -> None:
    monkeypatch.setenv("SHOP_SCOPE_HEADLESS", "false")
    assert Settings.from_env().headless is False
