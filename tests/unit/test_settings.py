"""Unit tests for runtime configuration."""

import pytest

from shopscope.config import Settings


def test_default_settings_are_valid(monkeypatch):
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

    settings = Settings.from_env()
    settings.validate()

    assert settings.browser == "chromium"
    assert settings.headless is True
    assert settings.navigation_timeout_ms == 15_000


@pytest.mark.parametrize("browser", ["invalid", "chrome", ""])
def test_invalid_browser_is_rejected(monkeypatch, browser):
    monkeypatch.setenv("SHOP_SCOPE_BROWSER", browser)
    with pytest.raises(ValueError, match="Unsupported browser"):
        Settings.from_env().validate()


def test_non_positive_timeout_is_rejected(monkeypatch):
    monkeypatch.setenv("SHOP_SCOPE_NAV_TIMEOUT_MS", "0")
    with pytest.raises(ValueError, match="positive"):
        Settings.from_env().validate()
