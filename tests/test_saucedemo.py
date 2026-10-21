from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com/"
USER = "standard_user"
PASSWORD = "secret_sauce"


def login(driver, username=USER, password=PASSWORD):
    driver.get(BASE_URL)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()


def test_tc01_login_success(driver, screenshot):
    login(driver)
    wait = WebDriverWait(driver, 20, ignored_exceptions=(StaleElementReferenceException,))
    wait.until(EC.url_contains("inventory.html"))
    # Navigation can finish before React has rendered the Products heading.
    heading = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title")))
    wait.until(lambda d: d.find_element(By.CLASS_NAME, "title").text.strip() == "Products")
    assert heading.is_displayed()
    screenshot("PASS")


def test_tc02_login_wrong_password(driver, screenshot):
    login(driver, password="wrong_password")
    error = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
    )
    assert "Username and password do not match" in error.text
    screenshot("PASS")


def test_tc03_sort_prices_low_to_high(driver, screenshot):
    login(driver)
    wait = WebDriverWait(driver, 15)
    sort = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test='product-sort-container']")))
    Select(sort).select_by_value("lohi")
    prices = [float(e.text.replace("$", "")) for e in driver.find_elements(By.CLASS_NAME, "inventory_item_price")]
    assert len(prices) > 1
    assert prices == sorted(prices)
    screenshot("PASS")


def test_tc04_add_product_to_cart(driver, screenshot):
    login(driver)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    item = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name")))
    assert item.text == "Sauce Labs Backpack"
    assert driver.find_element(By.CLASS_NAME, "cart_quantity").text == "1"
    screenshot("PASS")


def test_tc05_remove_product_from_cart(driver, screenshot):
    login(driver)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    # Wait for cart navigation and retry if React replaces DOM elements.
    WebDriverWait(driver, 15).until(EC.url_contains("cart.html"))
    remove_button = (By.ID, "remove-sauce-labs-backpack")
    retry_wait = WebDriverWait(driver, 15, ignored_exceptions=(StaleElementReferenceException,))

    def remove_when_ready(d):
        button = EC.element_to_be_clickable(remove_button)(d)
        if not button:
            return False
        button.click()
        return True

    retry_wait.until(remove_when_ready)
    retry_wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "cart_item")))
    retry_wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "shopping_cart_badge")))
    screenshot("PASS")


def test_tc06_logout(driver, screenshot):
    login(driver)
    wait = WebDriverWait(driver, 15)
    wait.until(EC.element_to_be_clickable((By.ID, "react-burger-menu-btn"))).click()
    wait.until(EC.element_to_be_clickable((By.ID, "logout_sidebar_link"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "login-button")))
    assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/")
    screenshot("PASS")
