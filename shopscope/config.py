"""Centralized environment configuration."""

from dataclasses import dataclass
import os


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
    def from_env(cls) -> "Settings":
        """Build settings from environment variables with safe defaults."""
        return cls(
            environment=os.getenv("SHOP_SCOPE_ENV", "local"),
            browser=os.getenv("SHOP_SCOPE_BROWSER", "chromium").lower(),
            headless=os.getenv("SHOP_SCOPE_HEADLESS", "true").strip().lower()
            in {"1", "true", "yes", "on"},
            base_url=os.getenv("SHOP_SCOPE_BASE_URL", "https://playwright.dev").rstrip("/"),
            navigation_timeout_ms=int(os.getenv("SHOP_SCOPE_NAV_TIMEOUT_MS", "15000")),
            action_timeout_ms=int(os.getenv("SHOP_SCOPE_ACTION_TIMEOUT_MS", "5000")),
            artifacts_dir=os.getenv("SHOP_SCOPE_ARTIFACTS_DIR", "test-results"),
        )

    def validate(self) -> None:
        """Reject unsupported or unsafe configuration early."""
        if self.browser not in {"chromium", "firefox", "webkit"}:
            raise ValueError(
                f"Unsupported browser {self.browser!r}; choose chromium, firefox, or webkit."
            )
        if self.navigation_timeout_ms <= 0 or self.action_timeout_ms <= 0:
            raise ValueError("Timeout values must be positive.")
        if not self.base_url.startswith(("http://", "https://")):
            raise ValueError("SHOP_SCOPE_BASE_URL must start with http:// or https://.")
