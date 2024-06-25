import os
from datetime import datetime, timezone



def DefaultTimestampStr() -> str:
    """
    Returns the current timestamp as a string.
    """
    current = datetime.now().timestamp()
    return str(int(current))


def DefaultUTCDatetime() -> str:
    """
    Returns:
        str: The current UTC datetime as a string in the format "%Y-%m-%d %H:%M:%S".
    """
    return (datetime.now(timezone.utc)).strftime("%Y-%m-%d %H:%M:%S")
