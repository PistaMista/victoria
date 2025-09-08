import inspect
import builtins
import textwrap
from typing import get_type_hints
from app.model.action import Action
from app.model.agent import Agent
from app.model.trigger import Trigger
from app.model.monologue import Monologue
from app.model.language_model import LanguageModel
from app.model.llm_connection import LLMConnection

TOOL_REGISTRY = []

def serialize_type(t):
    if t in vars(builtins).values():
        # For a builtin type x, eval(repr(x)) != x
        return t.__name__
    else:
        return repr(t)

def convert_to_action(func) -> Action:
    func_name = func.__name__
    raw_source = inspect.getsource(func)
    cleaned_source = textwrap.dedent(raw_source)
    doc = inspect.getdoc(func) or ""

    signature = inspect.signature(func)
    type_hints = get_type_hints(func)
    
    param_schema = {}
    
    for name, param in signature.parameters.items():
        if not param.kind in [inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.VAR_KEYWORD]:
            raise InvalidActionParamTypeError(name)
        
        if param.annotation == inspect._empty:
            raise UnannotatedActionParamError(name)
        
        param_schema[name] = serialize_type(type_hints.get(name))
    
    action = Action(
        function_name=func_name,
        function_param_schema=param_schema,
        function_source_code=cleaned_source,
        function_docstring=doc
    )

    return action
    

def tool(func):
    action = convert_to_action(func)
    TOOL_REGISTRY.append(action)
    return func

class UnannotatedActionParamError(Exception):
    def __init__(self, param_name: str):
        super().__init__(f"parameter '{param_name}' is missing a type annotation")

class InvalidActionParamTypeError(Exception):
    def __init__(self, param_name: str):
        super().__init__(f"invalid parameter in function signature: {param_name} - only POSITIONAL_OR_KEYWORD and VAR_KEYWORD are allowed")