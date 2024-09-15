from langchain.agents import tool
from datetime import datetime

@tool
def today() -> str:
    """Returns today's date in YEAR-MONTH-DAY DAY_OF_WEEK format."""
    return datetime.today().strftime("%Y-%m-%d %A")

@tool
def time() -> str:
    """Returns the current time in HOURS:MINUTES:SECONDS format."""
    return datetime.now().strftime("%H:%M:%S")