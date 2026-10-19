"""Shared page-object behavior."""

from playwright.sync_api import Page


class BasePage:
    """Base class for page objects; retailer-specific selectors stay in subclasses."""

    def __init__(self, page: Page) -> None:
        self.page = page

    def navigate(self, url: str) -> None:
        """Navigate to an explicit URL."""
        self.page.goto(url, wait_until="domcontentloaded")

    def page_title(self) -> str:
        """Return the current document title."""
        return self.page.title()
