
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
