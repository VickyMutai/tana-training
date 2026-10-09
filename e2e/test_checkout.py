from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

from locators import (
    USERNAME, PASSWORD, LOGIN_BUTTON, INVENTORY,
    ADD_BACKPACK, CART_LINK, ITEM_NAME, ITEM_PRICE, CHECKOUT_BUTTON,
    FIRST_NAME, LAST_NAME, POSTAL_CODE, CONTINUE_BUTTON,
    TOTAL, FINISH_BUTTON, COMPLETE_HEADER, ERROR_MESSAGE,
)

from test_data import (
    BASE_URL,
    STANDARD_USER,
    PASSWORD as LOGIN_PASSWORD,
    CUSTOMER,
    PRODUCT_NAME,
    PRODUCT_PRICE,
    EXPECTED_TOTAL,
    ORDER_CONFIRMATION,
    MISSING_LAST_NAME_ERROR,
)


def test_add_to_cart_through_checkout(driver, wait):
    driver.get(BASE_URL)

    wait.until(
        EC.visibility_of_element_located(USERNAME)
    ).send_keys(STANDARD_USER)

    wait.until(
        EC.visibility_of_element_located(PASSWORD)
    ).send_keys(LOGIN_PASSWORD)

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
        EC.url_to_be(BASE_URL + "cart.html"),
        message="Cart page did not open",
    )

    cart_item = wait.until(
        EC.visibility_of_element_located(ITEM_NAME)
    )
    assert cart_item.text == PRODUCT_NAME, (
        f"Unexpected cart item: {cart_item.text!r}"
    )

    cart_price = wait.until(
        EC.visibility_of_element_located(ITEM_PRICE)
    )

    assert cart_price.text == PRODUCT_PRICE, (
        f"Expected cart price {PRODUCT_PRICE!r}, "
        f"got {cart_price.text!r}"
    )

    wait.until(
        EC.element_to_be_clickable(CHECKOUT_BUTTON)
    ).click()

    wait.until(
        EC.url_to_be(BASE_URL + "checkout-step-one.html"),
        message="Checkout information page did not open",
    )

    wait.until(
        EC.element_to_be_clickable(FIRST_NAME)
    ).send_keys(CUSTOMER["first_name"])

    wait.until(
        EC.element_to_be_clickable(LAST_NAME)
    ).send_keys(CUSTOMER["last_name"])

    postal_code = wait.until(
        EC.element_to_be_clickable(POSTAL_CODE)
    )
    postal_code.click()
    postal_code.clear()
    postal_code.send_keys(CUSTOMER["postal_code"])

    assert postal_code.get_attribute("value") == CUSTOMER["postal_code"], (
        "Postal code was not entered correctly: "
        f"{postal_code.get_attribute('value')!r}"
    )

    wait.until(
        EC.element_to_be_clickable(CONTINUE_BUTTON)
    ).click()

    try:
        wait.until(
            EC.url_to_be(BASE_URL + "checkout-step-two.html"),
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

        for error in driver.find_elements(*ERROR_MESSAGE):
            print(f"Page error: {error.text!r}")

        driver.save_screenshot("checkout_failure.png")
        print("Screenshot saved: checkout_failure.png")
        raise

    overview_item = wait.until(
        EC.visibility_of_element_located(ITEM_NAME)
    )
    assert overview_item.text == PRODUCT_NAME, (
        f"Unexpected overview item: {overview_item.text!r}"
    )

    total = wait.until(
        EC.visibility_of_element_located(TOTAL)
    )
    assert total.text == EXPECTED_TOTAL, (
        f"Unexpected order total: {total.text!r}"
    )

    wait.until(
        EC.element_to_be_clickable(FINISH_BUTTON)
    ).click()

    wait.until(
        EC.url_to_be(BASE_URL + "checkout-complete.html"),
        message="Checkout completion page did not open",
    )

    confirmation = wait.until(
        EC.visibility_of_element_located(COMPLETE_HEADER)
    )
    assert confirmation.text == ORDER_CONFIRMATION, (
        f"Unexpected confirmation: {confirmation.text!r}"
    )

def test_checkout_requires_last_name(driver, wait):
    driver.get(BASE_URL)

    wait.until(
        EC.element_to_be_clickable(USERNAME)
    ).send_keys(STANDARD_USER)

    wait.until(
        EC.element_to_be_clickable(PASSWORD)
    ).send_keys(LOGIN_PASSWORD)

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

    wait.until(EC.url_to_be(BASE_URL + "cart.html"))

    wait.until(
        EC.element_to_be_clickable(CHECKOUT_BUTTON)
    ).click()

    wait.until(
        EC.url_to_be(BASE_URL + "checkout-step-one.html")
    )

    wait.until(
        EC.element_to_be_clickable(FIRST_NAME)
    ).send_keys(CUSTOMER["first_name"])

    last_name = wait.until(
        EC.element_to_be_clickable(LAST_NAME)
    )
    last_name.clear()
    assert last_name.get_attribute("value") == ""

    postal_code = wait.until(
        EC.element_to_be_clickable(POSTAL_CODE)
    )
    postal_code.click()
    postal_code.clear()
    postal_code.send_keys(CUSTOMER["postal_code"])

    assert postal_code.get_attribute("value") == CUSTOMER["postal_code"]

    wait.until(
        EC.element_to_be_clickable(CONTINUE_BUTTON)
    ).click()

    error = wait.until(
        EC.visibility_of_element_located(ERROR_MESSAGE),
        message="Missing-last-name validation did not appear",
    )

    assert error.text == MISSING_LAST_NAME_ERROR, (
        f"Unexpected validation message: {error.text!r}"
    )

    assert driver.current_url == BASE_URL + "checkout-step-one.html", (
        "Checkout advanced despite the missing last name: "
        f"{driver.current_url}"
    )

