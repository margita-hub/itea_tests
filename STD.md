# Software Test Description (STD)
**Project**: iTea E-Commerce Automation Framework
**Author**: Margita Muratova
**Date**: May 2026

---

## 1. Introduction
### 1.1 Purpose
This Software Test Description (STD) outlines the detailed test architecture, scenarios, and execution strategies for the automated UI testing of the `itea.co.il` website. The framework ensures the functional integrity of core e-commerce workflows.

### 1.2 Scope
The scope of this automation encompasses:
- Header navigation and complex hover-state menus.
- Product filtering, sorting, and category validation.
- User Authentication (Login flows).
- E2E Shopping Cart & Wishlist operations.
- Mathematical validation of shipping rules and dynamic discounts.
- UI verifications (social links, images, buttons).

## 2. Test Environment
- **Automation Tool**: Playwright for Python
- **Test Runner**: Pytest
- **Browsers**: Chromium (Headless / UI mode)
- **Reporting**: Allure Framework
- **Integration**: SMTP Email Client, Local File System Bug Reporter

## 3. Test Strategy & Architecture
### 3.1 Design Pattern
The framework is built strictly upon the **Page Object Model (POM)**. Locators are centralized in `pages/locators.py` allowing for highly maintainable and readable code.

### 3.2 Automated Bug Lifecycle
Utilizing Pytest hooks (`conftest.py`), the framework intercepts test failures. Upon failure:
1. A Jira-formatted text file is generated in the `bug_reports/` directory capturing the exact test name, timestamp, and trace.
2. The `utils/send_email.py` module dispatches an email alert to the QA/Dev team detailing the failure.

---

## 4. Test Scenarios (Current Coverage: 32 Tests)

### TS-01: Authentication & Login (`test_login.py`)
- **Objective**: Verify secure access to the platform.
- **Test Cases**:
  - Valid Login success.
  - Invalid Login (wrong username/password).
  - Empty fields validation.
  - *Note: Bypasses Cloudflare captchas using specific Pytest skip decorators where applicable.*

### TS-02: Advanced Navigation (`test_navigation.py`)
- **Objective**: Validate main header routing and H1 headers.
- **Test Cases**:
  - Static Categories: Navigate to Tea, Teaware, Coffee.
  - Special Categories: Navigate to Sale, validating the URL and `.onsale` badge existence on every loaded product.

### TS-03: Dynamic Filtering & Sorting (`test_filtering_and_sorting.py`)
- **Objective**: Verify that deeply nested UI components route to correct taxonomy endpoints.
- **Test Cases**:
  - Parameterized hover dropdowns (`Choose tea` > `Feelings` > `relaxation`, etc.) verified against expected URLs and H1 text.
  - Ascending & Descending price sorting. Validated mathematically using Regex price extraction across paginated elements.

### TS-04: End-to-End Workflows (`test_e2e_flows.py`)
- **Objective**: Simulate real user behavior from entry to checkout.
- **Test Cases**:
  - Smart Discount Shopping: Scans for items >= 20% discount (adds to cart) vs < 20% (adds to wishlist).
  - Empty cart behavior: Verifies 'Return to shop' functionality.
  - Add multiple items to the cart across different pages, bypassing lazy loading constraints.

### TS-05: Mathematical Validations (`test_math_validations.py`)
- **Objective**: Ensure the business logic behind shipping costs is pixel-perfect.
- **Test Cases**:
  - Tracks the "₪200 for Free Shipping" progress bar.
  - Calculates added cart value dynamically, asserts the remaining required amount drops by the exact float value of the items added.

### TS-06: UI & Grids (`test_home_page.py`, `test_ui_grids.py`)
- **Objective**: Verify static visual elements.
- **Test Cases**:
  - Verifies exact URL redirects for Social Media links (Facebook, Instagram, YouTube) enforcing strict browser context switching.
  - Logo presence and image hash validations.
  - Verifies every product in a lazy-loaded grid successfully injects a Wishlist heart icon.

## 5. Future Enhancements (Path to 40 Tests)
To complete the framework, the following areas will be automated:
1. **Cart Modifications**: Updating item quantities, deleting items, and verifying auto-refresh totals.
2. **Footer Validations**: Legal pages, Shipping policy navigation.
3. **Wishlist Sync**: Verifying items added to wishlist sync accurately to the user account dashboard.
4. **Language Localization**: Verifying the Hebrew language toggle successfully redirects the locale path and alters specific DOM text.

## 6. Execution Instructions
Run the entire suite securely:
`NODE_TLS_REJECT_UNAUTHORIZED=0 pytest -v --alluredir=allure-results`

---
*End of Document*
