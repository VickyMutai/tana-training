import pytest
from selenium.webdriver.support import expected_conditions as EC

from locators import (
    USERNAME, PASSWORD, LOGIN_BUTTON, INVENTORY,
    ADD_BACKPACK, CART_LINK, CHECKOUT_BUTTON,
    FIRST_NAME, LAST_NAME,
)

from test_data import (
    BASE_URL,
    STANDARD_USER,
    PROBLEM_USER,
    PASSWORD as LOGIN_PASSWORD,
    CUSTOMER,
)


@pytest.mark.parametrize(
    "username",
    [STANDARD_USER, PROBLEM_USER],
)
def test_checkout_preserves_last_name(driver, wait, username):
    driver.get(BASE_URL)

    wait.until(
        EC.element_to_be_clickable(USERNAME)
    ).send_keys(username)

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

    wait.until(
        EC.url_to_be(BASE_URL + "cart.html"),
        message="Cart page did not open",
    )

    wait.until(
        EC.element_to_be_clickable(CHECKOUT_BUTTON)
    ).click()

    wait.until(
        EC.url_to_be(BASE_URL + "checkout-step-one.html"),
        message="Checkout information page did not open",
    )

    first_name = wait.until(
        EC.element_to_be_clickable(FIRST_NAME)
    )
    first_name.send_keys(CUSTOMER["first_name"])

    last_name = wait.until(
        EC.element_to_be_clickable(LAST_NAME)
    )
    last_name.send_keys(CUSTOMER["last_name"])

    first_name.click()

    actual_last_name = last_name.get_attribute("value")

    assert actual_last_name == CUSTOMER["last_name"], (
        f"{username}: expected last name "
        f"{CUSTOMER['last_name']!r}, but got {actual_last_name!r}"
    )