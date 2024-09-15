import importlib.util
import sys
import os
from pathlib import Path
from inspect import getmembers, isfunction
from langchain_core.tools import StructuredTool


def __import_tools_from_folder(folder):
    tools = []

    for f in os.listdir(folder):
        if not f.endswith(".py") or f == "__init__.py":
            continue
        
        path = os.path.join(folder, f)
        name = f[:-3]

        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        members = getmembers(module, lambda p: type(p) is StructuredTool)
        tools.extend(
            map(lambda t: t[1], members)
        )

    return tools
    
__tool_folder = Path(__file__).parent
tools = __import_tools_from_folder(__tool_folder)