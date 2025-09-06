
class LLMService:
    pass

class Message:
    def __init__(self, content: str):
        self._content: str = content
    
    def __eq__(self, o: object) -> bool:
        return type(self) is type(o) and self._content == o._content

class SystemMessage(Message):
    pass

class AssistantMessage(Message):
    pass

class UserMessage(Message):
    pass

class NonexistentConnectionError(Exception):
    def __init__(id: int):
        super().__init__(f"the connection with id {id} does not exist")

class NonexistentModelError(Exception):
    def __init__(id: int):
        super().__init__(f"the model with id {id} does not exist")

class DisabledModelError(Exception):
    def __init__(id: int):
        super().__init__(f"the model with id {id} is disabled and cannot be used")

class OllamaCommunicationError(Exception):
    def __init__():
        super().__init__("failed to communicate with Ollama server")