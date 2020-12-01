"""Habit Server Utilities."""
import re


def is_valid_email_addr(addr):
    """Validate whether an email address is syntactically valid.

    :param addr str: email addres
    :returns bool: is valid?
    """
    if re.fullmatch(r"[^@]+@[^@]+\.[^@]+", addr):
        return True
    else:
        return False
