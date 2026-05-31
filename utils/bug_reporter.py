import os
import re
import smtplib
from email.message import EmailMessage
from datetime import datetime
from utils.send_email import from_email, password, to_email


class BugReporter:
    @staticmethod
    def report_failed_test(test_name: str, error_message: str, steps: str = "N/A"): #(By adding = "N/A", it makes the parameter optional. If a test doesn't have a docstring, it will just default to printing "N/A" instead of crashing).
        safe_test_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', test_name)
        os.makedirs("bug_reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filename = f"bug_reports/JIRA_{safe_test_name}_{timestamp}.txt"

        report_content = f"""=========================================
        🚨 NEW BUG DETECTED 🚨
        =========================================
        Date: {timestamp}
        Test Failed: {test_name}
        Environment: https://itea.co.il/en/
        =========================================

        [DESCRIPTION / STEPS]
        {steps.strip()}

        [ACTUAL RESULT / ERROR]
        {error_message}

        [ALLURE REPORT]
        To view the full stack trace, screenshots, and logs, open the Allure Report!
        Local Command: allure serve ./allure-results
        CI/CD Link: https://your-ci-server.com/allure-reports/latest

        ========================================="""
        with open(filename, "w") as file:
            file.write(report_content)
        print(f"\n✅ Bug Report saved to: {filename}")

        if from_email and password and to_email and to_email != [""]:
            subject = f"🚨 Automated Test Failure: {test_name}"
            msg = EmailMessage()
            msg.set_content(report_content)
            msg['Subject'] = subject
            msg['From'] = from_email
            msg['To'] = ", ".join(to_email)

            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.login(from_email, password)
                    server.send_message(msg)
                print(f"📧 Email successfully sent to {msg['To']}!")
            except Exception as e:
                print(f"❌ Failed to send email: {e}")