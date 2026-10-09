from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from locators import (
    USERNAME, PASSWORD, LOGIN_BUTTON, INVENTORY,
    ADD_BACKPACK, CART_LINK, ITEM_NAME, CHECKOUT_BUTTON,
    FIRST_NAME, LAST_NAME, POSTAL_CODE, CONTINUE_BUTTON,
    TOTAL, FINISH_BUTTON, COMPLETE_HEADER, ERROR_MESSAGE,
)


def test_add_to_cart_through_checkout():
    driver = webdriver.Chrome()

    try:
        wait = WebDriverWait(driver, 10)
        base_url = "https://www.saucedemo.com/"
        driver.get(base_url)

        wait.until(
            EC.visibility_of_element_located(USERNAME)
        ).send_keys("standard_user")

        wait.until(
            EC.visibility_of_element_located(PASSWORD)
        ).send_keys("secret_sauce")

        wait.until(
            EC.element_to_be_clickable(LOGIN_BUTTON)
        ).click()

        wait.until(
            EC.visibility_of_element_located(INVENTORY),
            message="Inventory did not become visible after login",
        )

        wait.until(
            EC.element_to_be_clickable(ADD_BACKPACK)
        ).click()

        wait.until(
            EC.element_to_be_clickable(CART_LINK)
        ).click()

        wait.until(
            EC.url_to_be(base_url + "cart.html"),
            message="Cart page did not open",
        )

        cart_item = wait.until(
            EC.visibility_of_element_located(ITEM_NAME)
        )
        assert cart_item.text == "Sauce Labs Backpack", (
            f"Unexpected cart item: {cart_item.text!r}"
        )

        wait.until(
            EC.element_to_be_clickable(CHECKOUT_BUTTON)
        ).click()

        wait.until(
            EC.url_to_be(base_url + "checkout-step-one.html"),
            message="Checkout information page did not open",
        )

        wait.until(
            EC.visibility_of_element_located(FIRST_NAME)
        ).send_keys("Victoria")

        wait.until(
            EC.visibility_of_element_located(LAST_NAME)
        ).send_keys("Mutai")

        wait.until(
            EC.visibility_of_element_located(POSTAL_CODE)
        ).send_keys("30100")

        wait.until(
            EC.element_to_be_clickable(CONTINUE_BUTTON)
        ).click()

        try:
            wait.until(
                EC.url_to_be(base_url + "checkout-step-two.html"),
                message="Checkout overview did not open after Continue",
            )
        except TimeoutException:
            print(f"\nActual URL: {driver.current_url}")

            for label, locator in [
                ("First name", FIRST_NAME),
                ("Last name", LAST_NAME),
                ("Postal code", POSTAL_CODE),
            ]:
                elements = driver.find_elements(*locator)
                if elements:
                    value = elements[0].get_attribute("value")
                    print(f"{label}: {value!r}")

            errors = driver.find_elements(*ERROR_MESSAGE)
            for error in errors:
                print(f"Page error: {error.text!r}")

            driver.save_screenshot("checkout_failure.png")
            print("Screenshot saved: checkout_failure.png")
            raise

        overview_item = wait.until(
            EC.visibility_of_element_located(ITEM_NAME)
        )
        assert overview_item.text == "Sauce Labs Backpack", (
            f"Unexpected overview item: {overview_item.text!r}"
        )

        total = wait.until(
            EC.visibility_of_element_located(TOTAL)
        )
        assert total.text == "Total: $32.39", (
            f"Unexpected order total: {total.text!r}"
        )

        wait.until(
            EC.element_to_be_clickable(FINISH_BUTTON)
        ).click()

        wait.until(
            EC.url_to_be(base_url + "checkout-complete.html"),
            message="Checkout completion page did not open",
        )

        confirmation = wait.until(
            EC.visibility_of_element_located(COMPLETE_HEADER)
        )
        assert confirmation.text == "Thank you for your order!", (
            f"Unexpected confirmation: {confirmation.text!r}"
        )

    finally:
        driver.quit()