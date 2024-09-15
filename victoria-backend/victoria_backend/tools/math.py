from langchain.agents import tool

@tool
def add(a: int, b: int) -> int:
    """Adds the integers a and b."""
    return a + b

@tool
def subtract(a: int, b: int) -> int:
    """Subtracts the integers a and b."""
    return a - b

@tool
def multiply(a: int, b: int) -> int:
    """Multiplies the integers a and b."""
    return a * b

@tool
def divide(a: int, b: int) -> int:
    """Divides the integers a and b."""
    return a / b