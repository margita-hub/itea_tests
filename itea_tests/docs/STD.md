# Software Test Documentation (STD) - ITEA Automation

## 1. Introduction
This document describes the test scope, strategy, and environment for the automated testing of the **ITEA** web application.

### 1.1 Objective
To ensure the stability and functionality of core user flows (Login, Tea Menu, Checkout) using an automated regression suite.

## 2. Test Environment


| Component | Specification |
| :--- | :--- |
| **Framework** | Playwright (Python) |
| **Test Runner** | Pytest |
| **Browsers** | Chromium, Firefox, WebKit (Headless & Headed) |
| **Viewport** | 1920 x 1080 |
| **Base URL** | `https://itea.co.il` |
| **CI/CD** | GitHub Actions (Ubuntu Latest) |

## 3. Test Strategy
We utilize the **Page Object Model (POM)** design pattern to separate test logic from page mechanics.

### 3.1 Directory Structure
* **`pages/`**: Contains page classes (e.g., `LoginPage`, `TeaPage`) with element locators.
* **`tests/`**: Contains execution scripts (e.g., `test_login.py`).
* **`config/`**: Stores global settings and test data.

### 3.2 Execution Strategy
* **Smoke Tests**: Run on every Push to `main`.
* **Regression**: Run nightly or before release.
* **Visual Regression**: Snapshots stored in `tests/reference_images`.

## 4. Test Scope & Scenarios

### 4.1 Functional Testing

| ID | Feature | Test Case Description | Priority |
| :--- | :--- | :--- | :--- |
| **TC01** | Home Page | Verify homepage loads and title is correct | P0 |
| **TC02** | Navigation | Verify "Tea Menu" link redirects to product listing | P1 |
| **TC03** | Search | Verify searching for "Green Tea" returns results | P1 |
| **TC04** | Cart | Verify adding an item updates the cart counter | P0 |

### 4.2 Visual Testing
* Verify Home Page layout matches baseline.
* Verify Product Card component styling.

## 5. Deliverables
* **Test Report**: HTML report generated via `playwright-report`.
* **Screenshots**: Captured automatically on test failure.
* **Video**: Recorded for failed tests (configured in CI).

