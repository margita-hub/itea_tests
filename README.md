# iTea Test Automation Framework

A comprehensive UI test automation framework for [iTea](https://itea.co.il) e-commerce platform.

## 🚀 Features
- **Modern Tech Stack**: Python, Playwright, Pytest
- **Design Pattern**: Page Object Model (POM)
- **Reporting**: Allure Reports - interactive visual test reports
- **Automated Bug Reporting**: Generates bug reports on test failures
- **Email Notifications**: SMTP email alert on critical failures
- **CI/CD**: GitHub Actions with automatic Allure report publishing

## 🛠 Prerequisites
- Python 3.10+
- Node.js (for Allure CLI)
- Allure CLI: `brew install allure` (Mac) / `scoop install allure` (Windows)

## 📦 Quick Start

**1. Clone:**
```bash
git clone https://github.com/margita-hub/itea_tests.git
cd itea_tests
```

**2. Install everything:**
```bash
pip install -r requirements.txt
playwright install chromium
```

**3. Run tests + generate report:**
```bash
pytest
allure serve allure-results
```

That's it! 🎉

## 🏃 Running Specific Tests

```bash
# All tests
pytest

# Specific category
pytest tests/test_login.py -v
pytest tests/test_cart.py -v
pytest tests/test_select_options_product.py -v
```

## 📊 Allure Report

```bash
# Run tests (auto-generates allure-results/)
pytest

# View interactive report
allure serve allure-results
```

> ⚠️ Must run `pytest` first before `allure serve`!

## 🌐 Live CI Report
👉 https://margita-hub.github.io/itea_tests/

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


## 🤖 CI/CD

[![Tests](https://github.com/margita-hub/itea_tests/actions/workflows/playwright-tests.yml/badge.svg)](https://github.com/margita-hub/itea_tests/actions)

Tests run automatically on every push.

### 🍴 Forking This Project
1. Fork the repository
2. Enable GitHub Pages: Settings → Pages → gh-pages branch
3. Add secrets (optional - for email notifications):
   - `EMAIL_USER` - Gmail address
   - `EMAIL_PASS` - Gmail app password
   - `EMAIL_TO` - Recipient email(s)
4. Push code → CI runs automatically!