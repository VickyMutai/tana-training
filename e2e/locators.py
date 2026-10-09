from selenium.webdriver.common.by import By

USERNAME = (By.CSS_SELECTOR, '[data-test="username"]')
PASSWORD = (By.CSS_SELECTOR, '[data-test="password"]')
LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-test="login-button"]')
INVENTORY = (By.CSS_SELECTOR, '[data-test="inventory-container"]')
ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')
ADD_BACKPACK = (
    By.CSS_SELECTOR,
    '[data-test="add-to-cart-sauce-labs-backpack"]',
)
CART_LINK = (By.CSS_SELECTOR, '[data-test="shopping-cart-link"]')
ITEM_NAME = (By.CSS_SELECTOR, '[data-test="inventory-item-name"]')
CHECKOUT_BUTTON = (By.CSS_SELECTOR, '[data-test="checkout"]')
FIRST_NAME = (By.CSS_SELECTOR, '[data-test="firstName"]')
LAST_NAME = (By.CSS_SELECTOR, '[data-test="lastName"]')
POSTAL_CODE = (By.CSS_SELECTOR, '[data-test="postalCode"]')
CONTINUE_BUTTON = (By.CSS_SELECTOR, '[data-test="continue"]')
TOTAL = (By.CSS_SELECTOR, '[data-test="total-label"]')
FINISH_BUTTON = (By.CSS_SELECTOR, '[data-test="finish"]')
COMPLETE_HEADER = (By.CSS_SELECTOR, '[data-test="complete-header"]')