import os
import re
import smtplib
from email.message import EmailMessage
from datetime import datetime
from pathlib import Path
from utils.send_email import from_email, password, to_email


class BugReporter:

    @staticmethod
    def report_failed_test(
        test_name: str,
        error_message: str,
        steps: str = "N/A",
        trace_path: str = None,       # traces
    ):
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '_', test_name)
        os.makedirs("bug_reports", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename  = f"bug_reports/JIRA_{safe_name}_{timestamp}.txt"

        # Build trace after file was saved
        trace_section = ""
        if trace_path and Path(trace_path).exists():
            trace_section = (
                "[PLAYWRIGHT TRACE]\n"
                f"Trace file: {trace_path}\n"
                "View online: https://trace.playwright.dev\n"
                "→ Open the link and drag-and-drop the attached .zip\n\n"
            )

        report_content = (
            "=========================================\n"
            "NEW BUG DETECTED\n"
            "=========================================\n"
            f"Date:        {timestamp}\n"
            f"Test Failed: {test_name}\n"
            f"Environment: https://itea.co.il/en/\n"
            "=========================================\n\n"
            "[DESCRIPTION / STEPS]\n"
            f"{steps.strip()}\n\n"
            "[ACTUAL RESULT / ERROR]\n"
            f"{error_message}\n\n"
            f"{trace_section}"
            "[ALLURE REPORT]\n"
            "Local: allure serve ./allure-results\n"
            "=========================================\n"
        )

        with open(filename, "w") as file:
            file.write(report_content)

        print(f"\n Bug report saved: {filename}")

        BugReporter._send_email_alert(test_name, report_content, trace_path)

    @staticmethod
    def _send_email_alert(test_name: str, report_content: str, trace_path: str = None):
        if not (from_email and password and to_email):
            return

        recipients = to_email if isinstance(to_email, list) else [to_email]
        recipients = [r for r in recipients if r.strip()]
        if not recipients:
            return

        msg = EmailMessage()
        msg.set_content(report_content)
        msg['Subject'] = f"Automated Test Failure: {test_name}"
        msg['From']    = from_email
        msg['To']      = ", ".join(recipients)

        # Attach the trace zip if it exists
        if trace_path and Path(trace_path).exists():
            msg.add_attachment(
                Path(trace_path).read_bytes(),
                maintype="application",
                subtype="zip",
                filename=Path(trace_path).name,
            )
            print(f" Trace attached: {Path(trace_path).name}")

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(from_email, password)
                server.send_message(msg)
            print(f" Email sent to {msg['To']}")
        except Exception as e:
            print(f" Email failed: {e}")