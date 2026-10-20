from dataclasses import replace

import pytest

from shopscope.config import Settings


def test_default_settings_are_valid() -> None:
    settings = Settings()
    settings.validate()
    assert settings.browser == "chromium"
    assert settings.headless is True


def test_invalid_browser_is_rejected() -> None:
    with pytest.raises(ValueError, match="Unsupported browser"):
        replace(Settings(), browser="safari").validate()


def test_non_positive_timeout_is_rejected() -> None:
    with pytest.raises(ValueError, match="positive"):
        replace(Settings(), action_timeout_ms=0).validate()


def test_base_url_must_be_http_or_https() -> None:
    with pytest.raises(ValueError, match="absolute HTTP or HTTPS URL"):
        replace(Settings(), base_url="file:///tmp/page.html").validate()
