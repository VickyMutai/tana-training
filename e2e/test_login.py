from selenium.webdriver.support import expected_conditions as EC

from locators import (
    USERNAME,
    PASSWORD,
    LOGIN_BUTTON,
    INVENTORY,
    ERROR_MESSAGE,
)

from test_data import (
    BASE_URL,
    STANDARD_USER,
    LOCKED_OUT_USER,
    PASSWORD as LOGIN_PASSWORD,
    INVALID_PASSWORD,
    INVALID_LOGIN_ERROR,
    LOCKED_OUT_ERROR
)


def test_successful_login(driver, wait):
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

    wait.until(
        EC.url_to_be(BASE_URL + "inventory.html"),
        message="Inventory page did not open after login",
    )

    inventory = wait.until(
        EC.visibility_of_element_located(INVENTORY),
        message="Inventory was not visible after login",
    )

    assert inventory.is_displayed(), "Inventory is not displayed"


def test_failed_login(driver, wait):
    driver.get(BASE_URL)

    wait.until(
        EC.element_to_be_clickable(USERNAME)
    ).send_keys(STANDARD_USER)

    wait.until(
        EC.element_to_be_clickable(PASSWORD)
    ).send_keys(INVALID_PASSWORD)

    wait.until(
        EC.element_to_be_clickable(LOGIN_BUTTON)
    ).click()

    error = wait.until(
        EC.visibility_of_element_located(ERROR_MESSAGE),
        message="Login error message did not appear",
    )

    assert error.text == INVALID_LOGIN_ERROR, (
        f"Unexpected error text: {error.text!r}"
    )

    assert driver.current_url == BASE_URL, (
        f"Rejected login navigated to: {driver.current_url}"
    )

    assert not driver.find_elements(*INVENTORY), (
        "Inventory appeared after a rejected login"
    )

def test_locked_out_user_cannot_login(driver, wait):
    driver.get(BASE_URL)

    wait.until(
        EC.element_to_be_clickable(USERNAME)
    ).send_keys(LOCKED_OUT_USER)

    wait.until(
        EC.element_to_be_clickable(PASSWORD)
    ).send_keys(LOGIN_PASSWORD)

    wait.until(
        EC.element_to_be_clickable(LOGIN_BUTTON)
    ).click()

    error = wait.until(
        EC.visibility_of_element_located(ERROR_MESSAGE),
        message="Locked-account error did not appear",
    )

    assert error.text == LOCKED_OUT_ERROR, (
        f"Unexpected error text: {error.text!r}"
    )

    assert driver.current_url == BASE_URL, (
        f"Locked account navigated to: {driver.current_url}"
    )

    assert not driver.find_elements(*INVENTORY), (
        "Inventory appeared for a locked account"
    )