"""
https://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
"""

import logging
from colorlog import ColoredFormatter


class TernionLogs:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        LOG_LEVEL = logging.WARNING  # logging.DEBUG
        LOGFORMAT = "  %(log_color)s%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

        logging.root.setLevel(LOG_LEVEL)
        formatter = ColoredFormatter(LOGFORMAT)

        stream = logging.StreamHandler()
        stream.setLevel(LOG_LEVEL)
        stream.setFormatter(formatter)

        log = logging.getLogger("pythonConfig")
        log.setLevel(LOG_LEVEL)
        log.addHandler(stream)

    def debug(self, message):
        log = logging.getLogger("pythonConfig")
        log.debug(message)

    def info(self, message):
        log = logging.getLogger("pythonConfig")
        log.info(message)

    def warn(self, message):
        log = logging.getLogger("pythonConfig")
        log.warning(message)

    def error(self, message):
        log = logging.getLogger("pythonConfig")
        log.error(message)

    def critical(self, message):
        log = logging.getLogger("pythonConfig")
        log.critical(message)


log = TernionLogs()

if __name__ == "__main__":
    # log = TernionLogs()
    log.debug("A quirky message only developers care about")
    log.info("Curious users might want to know this")
    log.warn("Something is wrong and any user should be informed")
    log.error("Serious stuff, this is red for a reason")
    log.critical("OH NO everything is on fire")
