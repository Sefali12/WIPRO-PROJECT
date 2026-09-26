"""
logger.py
---------
One shared logger for the whole framework. Writes to both the console
(so you SEE it live while recording the demo) and to reports/logs/execution.log
(so there's an artifact you can show / attach as evidence of the run).
"""

import logging
import os
from datetime import datetime

_LOG_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "reports",
    "logs",
)
os.makedirs(_LOG_DIR, exist_ok=True)

_LOG_FILE = os.path.join(
    _LOG_DIR, f"execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)


def get_logger(name: str = "automation") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:  # avoid duplicate handlers on repeated imports
        return logger

    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(fmt)

    file_handler = logging.FileHandler(_LOG_FILE, encoding="utf-8")
    file_handler.setFormatter(fmt)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger
