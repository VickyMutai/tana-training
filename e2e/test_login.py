from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators import USERNAME, PASSWORD, LOGIN_BUTTON, INVENTORY, ERROR_MESSAGE


def test_successful_login():
    driver = webdriver.Chrome()

    try:
        wait = WebDriverWait(driver, 10)
        driver.get("https://www.saucedemo.com/")

        wait.until(
            EC.visibility_of_element_located(USERNAME)
        ).send_keys("standard_user")

        wait.until(
            EC.visibility_of_element_located(PASSWORD)
        ).send_keys("secret_sauce")

        wait.until(
            EC.element_to_be_clickable(LOGIN_BUTTON)
        ).click()

        inventory = wait.until(
            EC.visibility_of_element_located(INVENTORY),
            message="Inventory did not become visible after login",
        )

        assert driver.current_url == "https://www.saucedemo.com/inventory.html"
        assert inventory.is_displayed(), "Inventory is not displayed"

    finally:
        driver.quit()

def test_failed_login():
    driver = webdriver.Chrome()
    try:
        wait = WebDriverWait(driver, 10)
        driver.get("https://www.saucedemo.com/")

        wait.until(
            EC.visibility_of_element_located(USERNAME)
        ).send_keys("standard_user")

        wait.until(
            EC.visibility_of_element_located(PASSWORD)
        ).send_keys("wrong_password")

        wait.until(
            EC.element_to_be_clickable(LOGIN_BUTTON)
        ).click()

        error = wait.until(
            EC.visibility_of_element_located(ERROR_MESSAGE),
            message="Login error message did not appear",
        )

        assert error.text == (
            "Epic sadface: Username and password do not match "
            "any user in this service"
        ), f"Unexpected error text: {error.text!r}"

        assert driver.current_url == "https://www.saucedemo.com/"
        assert not driver.find_elements(*INVENTORY), (
            "Inventory appeared after a rejected login"
        )

    finally:
        driver.quit()

