# API and UI Regression Suite

Automated regression tests for Restful-booker and Sauce Demo, using
pytest, requests and Selenium.

## Coverage

### Restful-booker API

- Create a booking and verify the returned data.
- Retrieve a newly created booking and compare its saved data.
- Update a booking with authentication and verify persistence.
- Delete a booking with authentication and verify removal.
- Reject unauthenticated updates and verify the booking is unchanged.
- Reject unauthenticated deletion and verify the booking is unchanged.
- Probe booking creation without the required firstname field.

API fixtures create fresh bookings and clean them up after each test.

### Sauce Demo UI

- Successful login.
- Incorrect-password login with exact error-message verification.
- Locked-account login with exact error-message verification.
- Add a backpack and verify its name and price in the cart.
- Complete checkout and verify the total and confirmation.
- Reject checkout when the last name is missing.
- Verify last-name preservation for standard_user and problem_user.

Each UI test uses a fresh Chrome browser. Locators are stored in
e2e/locators.py and UI test data in e2e/test_data.py.

## Setup

Requirements:

- Python 3.13 (the version used for the recorded runs).
- Google Chrome installed.
- Internet access to both applications and the browser-driver download.

From the repository root, create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows, activate it with:

```powershell
venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install requirements.txt
```

Selenium Manager automatically obtains the Chrome driver when needed.
No separate manual driver installation is normally required.

## Run the tests

Run commands from the repository root, which contains tests/ and e2e/.

Run the complete suite:

```bash
python -m pytest tests e2e -v --tb=short
```

Run only API tests:

```bash
python -m pytest tests -v --tb=short
```

Run only UI tests:

```bash
python -m pytest e2e -v --tb=short
```

Run one checkout test with diagnostic output:

```bash
python -m pytest e2e/test_checkout.py::test_add_to_cart_through_checkout -v -s --tb=short
```

Save two consecutive full runs:

```bash
python -m pytest tests e2e -v --tb=short > full_run_1.txt 2>&1
python -m pytest tests e2e -v --tb=short > full_run_2.txt 2>&1
```

Compare each test's outcome and the final counts. Execution times may differ.

## Known failures and result interpretation

The latest two full runs each collected 16 tests and produced:

- 14 passed.
- 2 failed.
- No reported setup or teardown errors.

The two failures were:

1. **Missing firstname:** Restful-booker returned 500 Internal Server Error.
   The test proposes a controlled 4xx rejection; the exact expected
   validation response requires confirmation.
2. **problem_user last name:** The entered last name was not preserved.
   The same assertion passed for standard_user.

These checks remain normal failing tests so the issues stay visible.
A run reproducing them exits with a nonzero status.

DELETE assertions use 201, following the API documentation's response
example despite its conflicting “Success 200” heading. Unauthenticated
DELETE returning 403 and GET after deletion returning 404 are explicitly
recorded assumptions requiring confirmation.

An earlier run timed out after clicking Finish during checkout.
Checkout passed in both latest runs, but the earlier intermittent
failure remains a stability concern.

Authenticated deletion currently appears in both API test files, so
the recorded count includes duplicate coverage.

## Deliberately not covered

- Reversed booking dates and incorrect field types, pending clarification
  of expected validation behaviour.
- PATCH updates and booking-list filtering.
- Other Sauce Demo products, sorting, removal and additional checkout
  validation combinations.
- Browsers other than Chrome.
- Performance, accessibility and comprehensive security testing.
- Real payment processing or fulfilment; Sauce Demo is a demo application.

Both applications are public shared environments. Tests verify the
selected journeys and do not establish complete product coverage.
