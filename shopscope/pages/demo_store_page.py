"""Page object for the bundled, deterministic demo storefront."""

from playwright.sync_api import Locator, Page, expect


class DemoStorePage:
    """Encapsulate selectors and interactions for the local test storefront."""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.search_input = page.get_by_role("searchbox", name="Search products")
        self.search_button = page.get_by_role("button", name="Search")
        self.product_cards = page.locator('[data-testid="product-card"]:not([hidden])')
        self.cart_count = page.get_by_test_id("cart-count")
        self.status_message = page.get_by_role("status")

    def open(self, url: str) -> None:
        self.page.goto(url, wait_until="domcontentloaded")

    def search(self, query: str) -> None:
        self.search_input.fill(query)
        self.search_button.click()

    def product(self, name: str) -> Locator:
        return self.page.get_by_role("article").filter(
            has=self.page.get_by_role("heading", name=name)
        )

    def add_product_to_cart(self, name: str) -> None:
        self.product(name).get_by_role("button", name="Add to cart").click()

    def expect_title(self, title: str) -> None:
        """Assert the current page title using a web-first assertion."""
        expect(self.page).to_have_title(title)

    def expect_product_visible(self, name: str) -> None:
        expect(self.product(name)).to_be_visible()

    def expect_product_count(self, count: int) -> None:
        expect(self.product_cards).to_have_count(count)
