import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_framework_can_assert_a_page(page: Page) -> None:
    """A deterministic browser test; no live retailer site is accessed."""
    page.set_content(
        """
        <!doctype html>
        <html lang="en">
          <head><title>ShopScope Test Store</title></head>
          <body>
            <main>
              <h1>Test Store</h1>
              <label for="search">Search products</label>
              <input id="search" type="search" />
              <button id="search-button">Search</button>
              <p id="status" role="status">Ready</p>
            </main>
            <script>
              document.querySelector("#search-button").addEventListener("click", () => {
                const query = document.querySelector("#search").value.trim();
                document.querySelector("#status").textContent =
                  query ? "Results for: " + query : "Enter a search term";
              });
            </script>
          </body>
        </html>
        """
    )
    expect(page).to_have_title("ShopScope Test Store")
    expect(page.get_by_role("heading", name="Test Store")).to_be_visible()
    page.get_by_role("searchbox", name="Search products").fill("wireless mouse")
    page.get_by_role("button", name="Search").click()
    expect(page.get_by_role("status")).to_have_text("Results for: wireless mouse")
