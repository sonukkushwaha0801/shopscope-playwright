"""Minimal consistent logging setup."""

import logging


def get_logger(name: str) -> logging.Logger:
    """Return a named logger; pytest controls handlers and log levels."""
    return logging.getLogger(name)
