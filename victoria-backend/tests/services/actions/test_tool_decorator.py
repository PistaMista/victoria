import pytest
from unittest import mock
from typing import List
from app.services.action import TOOL_REGISTRY
from app.services.action.tool import tool, UnannotatedActionParamError, InvalidActionParamTypeError

def test_tool_decorator_decorated_function_is_still_callable():
    # Arrange
    TOOL_REGISTRY.clear()
    outer_func = mock.MagicMock()
    
    # Act
    @tool
    def inner_func(p1: str, p2: str):
        outer_func(p1, p2)
    
    inner_func("lol", "wee")
    
    # Assert
    outer_func.assert_called_once_with("lol", "wee")
    
    

def test_tool_decorator_registers_action_with_proper_name():
    # Arrange
    TOOL_REGISTRY.clear()

    # Act
    @tool
    def my_mega_func():
        pass
    
    # Assert
    assert len(TOOL_REGISTRY) == 1
    assert TOOL_REGISTRY[0].function_name == "my_mega_func"

    # Teardown
    TOOL_REGISTRY.clear()

def test_tool_decorator_registers_action_with_proper_parameters():
    # Arrange
    TOOL_REGISTRY.clear()

    # Act
    @tool
    def my_mega_func(description: str, count: int, amount: float, enabled: bool, float_list: List[float], int_list: List[int]):
        pass
    
    # Assert
    assert TOOL_REGISTRY[0].function_param_schema == {
        "description": "str",
        "count": "int",
        "amount": "float",
        "enabled": "bool",
        "float_list": "typing.List[float]",
        "int_list": "typing.List[int]"
    }

    # Teardown
    TOOL_REGISTRY.clear()
    

def test_tool_decorator_registers_action_so_that_it_is_executable():
    # Arrange
    TOOL_REGISTRY.clear()
    outer_func = mock.MagicMock()

    # Act
    @tool
    def my_mega_func(description: str, count: int):
        outer_func(description, count)
        
    # Currently, the imported action function only has access to selected objects passed into its
    # namespace by the ActionService. It cannot use any other objects defined in the script its contained
    # in.
    #
    # TODO: Make it so that the imported action can use any symbols that are well-defined within the containing script.
    namespace = {
        "tool": lambda x: x,
        "outer_func": outer_func
    }
    exec(TOOL_REGISTRY[0].function_source_code, namespace)
    namespace["my_mega_func"]("desc", 42)
    
    # Assert
    outer_func.assert_called_once_with("desc", 42)

def test_tool_decorator_registers_action_docstring():
    # Arrange
    TOOL_REGISTRY.clear()

    # Act
    @tool
    def my_doc_func(desc: str):
        """This function has a docstring!"""
        print("lol")
    
    # Assert
    assert TOOL_REGISTRY[0].function_docstring == "This function has a docstring!"
    
def test_tool_decorator_registers_complex_action():
    # Arrange
    TOOL_REGISTRY.clear()

    # Act
    @tool
    def factorial(x: int):
        """Calculates the factorial of x."""
        if x <= 0:
            return 1
        return x * factorial(x - 1)
    
    namespace = {
        "tool": lambda f: f
    }
    exec(TOOL_REGISTRY[0].function_source_code, namespace)
    res = namespace["factorial"](4)

    # Assert
    assert TOOL_REGISTRY[0].function_name == "factorial"
    assert TOOL_REGISTRY[0].function_param_schema == {
        "x": "int"
    }
    assert TOOL_REGISTRY[0].function_docstring == "Calculates the factorial of x."
    assert res == 24
    

def test_tool_decorator_registers_multiple_actions():
    # Arrange
    TOOL_REGISTRY.clear()

    # Act
    @tool
    def add(a: float, b: int):
        """Adds a and b."""
        return a + b
    
    @tool
    def sub(a: int, b: float):
        """Subtracts b from a."""
        return a - b
    
    # Assert
    assert TOOL_REGISTRY[0].function_name == "add"
    assert TOOL_REGISTRY[0].function_param_schema == {
        "a": "float",
        "b": "int"
    }
    assert TOOL_REGISTRY[0].function_docstring == "Adds a and b."

    assert TOOL_REGISTRY[1].function_name == "sub"
    assert TOOL_REGISTRY[1].function_param_schema == {
        "a": "int",
        "b": "float"
    }
    assert TOOL_REGISTRY[1].function_docstring == "Subtracts b from a."
    

def test_tool_decorator_throws_when_registering_action_with_unannotated_parameter():
    # Arrange
    TOOL_REGISTRY.clear()

    # Act / Assert
    with pytest.raises(UnannotatedActionParamError):
        @tool
        def sub(a: int, b, c: int):
            """Subtracts b from a."""
            return a - b

    # Assert
    assert not TOOL_REGISTRY

def test_tool_decorator_throws_when_registering_action_with_invalid_parameter_types():
    # Only POSITION_OR_KEYWORD and VAR_KEYWORD are allowed
    # Arrange
    TOOL_REGISTRY.clear()

    # Act / Assert
    with pytest.raises(InvalidActionParamTypeError):
        @tool
        def sub(*args):
            """Subtracts b from a."""
            return a - b

    with pytest.raises(InvalidActionParamTypeError):
        @tool
        def sub(a: int, b: int, /, c: int, d: int):
            """Subtracts b from a."""
            return a - b

    with pytest.raises(InvalidActionParamTypeError):
        @tool
        def sub(a: int, b: int, *, c: int, d: int):
            """Subtracts b from a."""
            return a - b

    # Assert
    assert not TOOL_REGISTRY
