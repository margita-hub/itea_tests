# iTea Test Automation Framework

A comprehensive, robust, and scalable UI test automation framework built for the [iTea (itea.co.il)](https://itea.co.il) e-commerce platform.

## 🚀 Features
- **Modern Tech Stack**: Python, Playwright, Pytest.
- **Design Pattern**: Page Object Model (POM) for maximum reusability and clean architecture.
- **Reporting**: Integrated with **Allure Reports** for rich, interactive visual test reports.
- **Automated Bug Reporting**: Automatically generates Jira-style `.txt` bug reports on test failures.
- **Email Notifications**: Triggers an SMTP email alert instantly when a critical bug is found.
- **Complex UI Handling**: Advanced logic for lazy-loaded product grids, multi-level hover dropdowns, and dynamic locators.
- **Mathematical Validations**: Dynamically calculates and verifies "Free Shipping" thresholds based on floating-point cart math.
- **Smart Discount Logic**: Programmatically identifies products on sale, calculates discount percentages, and builds a cart conditionally.

## 🛠 Prerequisites
- Python 3.10+
- Node.js (for Allure Command Line - optional but recommended)
- `pip` package manager

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd itea_tests
   ```

2. **Install Python dependencies:**
   ```bash
   pip install pytest playwright pytest-playwright allure-pytest
   ```

3. **Install Playwright Browsers:**
   ```bash
   playwright install chromium
   ```

4. **Environment Setup (.env):**
   Create a `.env` file in the root directory for automated email notifications:
   ```env
   SENDER_EMAIL=your_email@gmail.com
   SENDER_PASSWORD=your_app_password
   RECEIVER_EMAIL=receiver_email@gmail.com
   ```

## 🏃‍♂️ Running Tests

**Run all tests:**
```bash
pytest -v
```

**Run specific test categories:**
```bash
pytest tests/test_login.py -v
pytest tests/test_filtering_and_sorting.py -v
```

**Generate and view Allure Report:**
```bash
pytest --alluredir=allure-results
allure serve allure-results
```

## 🎯 Select-Options Product Tests ✨ NEW

**Test Coverage:**
- 7 passing tests for bundle/select-options products
- ProductPage class for product detail pages
- Toast notification bug detection system
- Cross-platform sleep prevention (Mac/Windows/Linux)

**Run select-options tests:**
```bash
pytest tests/test_select_options_product.py -v
```

**Test Cases:**
1. ✅ Option selection validation
2. ✅ Error message display
3. ✅ Clear option selection
4. ✅ Add to wishlist
5. ✅ Add to cart (5 parametrized scenarios)

**Bugs Detected:**
- False toast message on "Select options" button - shows "added to cart" but product not actually added until reaching product detail page

## 🤖 GitHub Actions CI/CD

Automated testing on GitHub:
```bash
# .github/workflows/playwright-tests.yml
- Runs on push/PR to main/master/develop
- Tests Python 3.11 & 3.12
- Generates Allure reports
- Creates bug report artifacts
```

**View workflow:** `.github/workflows/playwright-tests.yml`

## 📁 Project Structure
```text
itea_tests/
├── pages/                      # Page Object Model classes
│   ├── locators.py             # Centralized CSS/XPath selectors
│   ├── base_page.py            # Parent class — shared methods for all pages
│   ├── home_page.py
│   ├── tea_page.py
│   ├── cart_page.py
│   ├── wishlist_page.py
│   ├── login_page.py
│   ├── teawear_page.py
│   └── coffee_page.py
├── tests/                      # Pytest test suites
│   ├── test_e2e_flows.py
│   ├── test_filtering_and_sorting.py
│   ├── test_home_page.py
│   ├── test_login.py
│   ├── test_math_validations.py
│   ├── test_navigation.py
│   ├── test_tea_page.py
│   ├── test_teawear.py
│   └── test_ui_grids.py
├── Services/                   # Business logic layer
│   └── shopping_service.py     # Smart discount shopping loop
├── config/
│   └── config.py               # All URLs and settings
├── utils/                      # Helper utilities
│   ├── bug_reporter.py         # Jira-style ticket generation
│   ├── send_email.py           # SMTP email alerts
│   ├── logger.py               # Logging setup
│   └── validation.py           # App validation helpers
├── bug_reports/                # Auto-generated .txt files on failure
├── reference_images/           # Saved logo hash for comparison
├── allure-results/             # Generated at runtime — do not commit
├── conftest.py                 # Fixtures — browser setup and page objects
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── .env                        # Credentials — never commit
└── .env.example                # Credentials template
```

## Email alerts setup

When a test fails, an email alert is sent automatically.

1. Copy `.env.example` to `.env`
2. Fill in your Gmail credentials:
   - `EMAIL_FROM` — Gmail address to send from
   - `EMAIL_PASSWORD` — Gmail App Password (not your real password)
   - `EMAIL_TO` — one or more recipients, comma-separated

> To generate a Gmail App Password:
> Google Account → Security → 2-Step Verification → App Passwords