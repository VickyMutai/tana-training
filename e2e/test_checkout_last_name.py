import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators import (
    USERNAME, PASSWORD, LOGIN_BUTTON, INVENTORY,
    ADD_BACKPACK, CART_LINK, CHECKOUT_BUTTON,
    FIRST_NAME, LAST_NAME,
)


@pytest.mark.parametrize(
    "username",
    ["standard_user", "problem_user"],
)
def test_checkout_preserves_last_name(username):
    driver = webdriver.Chrome()

    try:
        wait = WebDriverWait(driver, 10)
        driver.get("https://www.saucedemo.com/")

        wait.until(
            EC.visibility_of_element_located(USERNAME)
        ).send_keys(username)

        wait.until(
            EC.visibility_of_element_located(PASSWORD)
        ).send_keys("secret_sauce")

        wait.until(
            EC.element_to_be_clickable(LOGIN_BUTTON)
        ).click()

        wait.until(EC.visibility_of_element_located(INVENTORY))

        wait.until(
            EC.element_to_be_clickable(ADD_BACKPACK)
        ).click()

        wait.until(
            EC.element_to_be_clickable(CART_LINK)
        ).click()

        wait.until(
            EC.element_to_be_clickable(CHECKOUT_BUTTON)
        ).click()

        first_name = wait.until(
            EC.element_to_be_clickable(FIRST_NAME)
        )
        first_name.send_keys("QA")

        last_name = wait.until(
            EC.element_to_be_clickable(LAST_NAME)
        )
        last_name.send_keys("Tester")

        first_name.click()

        actual_last_name = last_name.get_attribute("value")

        assert actual_last_name == "Tester", (
            f"{username}: expected last name 'Tester', "
            f"but got {actual_last_name!r}"
        )

    finally:
        driver.quit()