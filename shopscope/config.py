"""Centralized environment configuration with explicit validation."""

from __future__ import annotations

import os
from dataclasses import dataclass
from urllib.parse import urlsplit


def _env_bool(name: str, default: bool) -> bool:
    """Parse a boolean environment variable without silently accepting typos."""
    raw = os.getenv(name)
    if raw is None:
        return default
    normalized = raw.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean (true/false, 1/0, yes/no, or on/off).")


def _env_positive_int(name: str, default: int) -> int:
    """Parse a positive integer environment variable with a useful error."""
    raw = os.getenv(name, str(default))
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer; received {raw!r}.") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero.")
    return value


@dataclass(frozen=True, slots=True)
class Settings:
    """Runtime settings loaded from environment variables."""

    environment: str = "local"
    browser: str = "chromium"
    headless: bool = True
    base_url: str = "https://playwright.dev"
    navigation_timeout_ms: int = 15_000
    action_timeout_ms: int = 5_000
    artifacts_dir: str = "test-results"

    @classmethod
    def from_env(cls) -> Settings:
        """Build settings from environment variables with safe defaults."""
        return cls(
            environment=os.getenv("SHOP_SCOPE_ENV", "local").strip() or "local",
            browser=os.getenv("SHOP_SCOPE_BROWSER", "chromium").strip().lower(),
            headless=_env_bool("SHOP_SCOPE_HEADLESS", True),
            base_url=os.getenv("SHOP_SCOPE_BASE_URL", "https://playwright.dev").strip().rstrip("/"),
            navigation_timeout_ms=_env_positive_int("SHOP_SCOPE_NAV_TIMEOUT_MS", 15_000),
            action_timeout_ms=_env_positive_int("SHOP_SCOPE_ACTION_TIMEOUT_MS", 5_000),
            artifacts_dir=os.getenv("SHOP_SCOPE_ARTIFACTS_DIR", "test-results").strip()
            or "test-results",
        )

    def validate(self) -> None:
        """Reject unsupported or unsafe configuration early."""
        if self.browser not in {"chromium", "firefox", "webkit"}:
            raise ValueError(
                f"Unsupported browser {self.browser!r}; choose chromium, firefox, or webkit."
            )
        if self.navigation_timeout_ms <= 0 or self.action_timeout_ms <= 0:
            raise ValueError("Timeout values must be positive.")
        parsed_url = urlsplit(self.base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.hostname:
            raise ValueError(
                "SHOP_SCOPE_BASE_URL must be an absolute HTTP or HTTPS URL with a hostname."
            )
