"""UI regression tests for SauceDemo.

Explicit waits handle asynchronous UI rendering in Chrome.
"""
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"
USER = "standard_user"
PASSWORD = "secret_sauce"
IGNORED = (StaleElementReferenceException, NoSuchElementException)


def wait_for(driver, seconds=25):
    return WebDriverWait(driver, seconds, poll_frequency=0.25, ignored_exceptions=IGNORED)


def click_when_ready(driver, locator):
    wait_for(driver).until(EC.element_to_be_clickable(locator)).click()


def login(driver, username=USER, password=PASSWORD):
    driver.get(BASE_URL)
    wait_for(driver).until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    click_when_ready(driver, (By.ID, "login-button"))


def wait_for_inventory(driver):
    wait_for(driver).until(EC.url_contains("inventory.html"))
    wait_for(driver).until(
        lambda d: d.find_element(By.CLASS_NAME, "title").text.strip() == "Products"
    )


def add_backpack(driver):
    wait_for_inventory(driver)
    click_when_ready(driver, (By.ID, "add-to-cart-sauce-labs-backpack"))
    # The badge sometimes updates after the click. Cart content is verified
    # after navigation instead of relying solely on the asynchronous badge.


def open_cart(driver):
    click_when_ready(driver, (By.CLASS_NAME, "shopping_cart_link"))
    wait_for(driver).until(EC.url_contains("cart.html"))
    wait_for(driver).until(EC.visibility_of_element_located((By.CLASS_NAME, "cart_list")))


def test_tc01_login_success(driver, screenshot):
    login(driver)
    wait_for_inventory(driver)
    screenshot("PASS")


def test_tc02_login_wrong_password(driver, screenshot):
    login(driver, password="wrong_password")
    wait_for(driver).until(
        lambda d: "Username and password do not match" in
        d.find_element(By.CSS_SELECTOR, "[data-test='error']").text
    )
    screenshot("PASS")


def test_tc03_sort_prices_low_to_high(driver, screenshot):
    login(driver)
    wait_for_inventory(driver)
    select_locator = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    wait_for(driver).until(EC.element_to_be_clickable(select_locator))
    Select(driver.find_element(*select_locator)).select_by_value("lohi")

    def sorted_prices(d):
        elements = d.find_elements(By.CLASS_NAME, "inventory_item_price")
        if len(elements) < 2:
            return False
        prices = [float(e.text.replace("$", "")) for e in elements]
        return prices == sorted(prices)

    wait_for(driver).until(sorted_prices)
    screenshot("PASS")


def test_tc04_add_product_to_cart(driver, screenshot):
    login(driver)
    add_backpack(driver)
    open_cart(driver)
    wait_for(driver).until(
        lambda d: d.find_element(By.CLASS_NAME, "inventory_item_name").text == "Sauce Labs Backpack"
        and d.find_element(By.CLASS_NAME, "cart_quantity").text == "1"
    )
    screenshot("PASS")


def test_tc05_remove_product_from_cart(driver, screenshot):
    login(driver)
    add_backpack(driver)
    open_cart(driver)
    wait_for(driver).until(
        lambda d: d.find_element(By.CLASS_NAME, "inventory_item_name").text == "Sauce Labs Backpack"
    )
    click_when_ready(driver, (By.ID, "remove-sauce-labs-backpack"))
    wait_for(driver).until(EC.invisibility_of_element_located((By.CLASS_NAME, "cart_item")))
    wait_for(driver).until(EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    screenshot("PASS")


def test_tc06_logout(driver, screenshot):
    login(driver)
    wait_for_inventory(driver)
    menu = (By.ID, "react-burger-menu-btn")
    logout = (By.ID, "logout_sidebar_link")
    click_when_ready(driver, menu)
    # Sidebar may animate or remount; wait for the actual visible logout link.
    wait_for(driver).until(EC.visibility_of_element_located(logout))
    click_when_ready(driver, logout)
    wait_for(driver).until(EC.visibility_of_element_located((By.ID, "login-button")))
    wait_for(driver).until(lambda d: d.current_url.rstrip("/") == BASE_URL.rstrip("/"))
    screenshot("PASS")
