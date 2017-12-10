import logging
from functools import wraps

LOG_LEVELS = frozenset(['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL'])

logger = logging.getLogger(__name__)


def parse_loglevel(name):
    """Parse log level name and return log level integer value"""
    name = name.upper()

    if name in LOG_LEVELS:
        return getattr(logging, name, logging.INFO)

    return logging.INFO
