from datetime import datetime


def is_valid_date(date_string: str) -> bool:
    """
    Returns True if date_string is a valid date
    in MMDDYYYY format.
    """

    try:
        datetime.strptime(date_string, "%m%d%Y")
        return True
    except ValueError:
        return False