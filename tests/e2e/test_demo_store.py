"""End-to-end tests against the bundled local storefront."""

from playwright.sync_api import expect

from shopscope.pages.demo_store_page import DemoStorePage


def test_storefront_loads_and_lists_products(page, demo_store_url):
    store = DemoStorePage(page)
    store.open(demo_store_url)

    store.expect_title("ShopScope Demo Store")
    expect(page.get_by_role("heading", name="ShopScope Demo Store")).to_be_visible()
    store.expect_product_count(3)


def test_search_filters_products(page, demo_store_url):
    store = DemoStorePage(page)
    store.open(demo_store_url)

    store.search("mouse")

    store.expect_product_count(1)
    store.expect_product_visible("Wireless Mouse")
    expect(
        page.get_by_role("article").filter(
            has=page.get_by_role("heading", name="USB-C Hub")
        )
    ).to_be_hidden()
    expect(store.status_message).to_have_text("1 product(s) found.")


def test_empty_search_result_is_reported(page, demo_store_url):
    store = DemoStorePage(page)
    store.open(demo_store_url)

    store.search("not-a-real-product")

    store.expect_product_count(0)
    expect(store.status_message).to_have_text("No products found.")


def test_add_to_cart_updates_count(page, demo_store_url):
    store = DemoStorePage(page)
    store.open(demo_store_url)

    store.add_product_to_cart("Everyday Backpack")

    expect(store.cart_count).to_have_text("1")
    expect(store.status_message).to_have_text("Everyday Backpack added to cart.")
