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

## 📁 Project Structure
```text
itea_tests/
├── pages/                  # Page Object Model classes
│   ├── locators.py         # Centralized CSS/XPath selectors
│   ├── home_page.py
│   ├── tea_page.py
│   └── ...
├── tests/                  # Pytest test suites
│   ├── test_e2e_flows.py
│   ├── test_filtering_and_sorting.py
│   ├── test_home_page.py
│   ├── test_login.py
│   ├── test_math_validations.py
│   └── test_navigation.py
├── utils/                  # Helper utilities
│   ├── bug_reporter.py     # Jira-style ticket generation
│   └── send_email.py       # SMTP integrations
├── bug_reports/            # Auto-generated txt files on failure
└── pytest.ini              # Pytest configuration
```
