#logs
#screenshots
from enum import Enum
import logging
import allure



class LogLevel(Enum):
    DEBUG = 1
    INFO = 2
    WARNING = 3
    ERROR = 4
    CRITICAL = 5

def log_message(logger, message: str, level: LogLevel, attach_to_allure: bool = True):
    if level == LogLevel.INFO:
        logger.info(message)
    elif level == LogLevel.WARNING:
        logger.warning(message)
    elif level == LogLevel.ERROR:
        logger.error(message)
    elif level == LogLevel.CRITICAL:
        logger.critical(message)
    elif level == LogLevel.DEBUG:
        logger.debug(message)

    if attach_to_allure:
        allure.attach(
            message,
            name = f"(Log ( { level.name.upper() } ))",
            attachment_type = allure.attachment_type.TEXT
        )

def take_screenshot(page, name: str = "screenshot"):
    try:
        screenshot_data = page.screenshot(type="png")
        allure.attach(
            screenshot_data,
            name = name,
            attachment_type = allure.attachment_type.PNG
        )
        return screenshot_data

    except Exception:
        return None


