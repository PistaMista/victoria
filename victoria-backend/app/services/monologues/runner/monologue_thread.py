import threading
from typing import Callable

class MonologueThread(threading.Thread):
    def __init__(
        self,
        monologue_id: int,
        on_finish: Callable[['MonologueThread'], None]
    ):
        super().__init__(name=f"monologue_{monologue_id}")
        self._id: int = monologue_id
        self._on_finish: Callable[['MonologueThread'], None] = on_finish
    

class AgenticMonologueThread(MonologueThread):
    def __init__(
        self,
        monologue_id: int,
        on_finish: Callable[[], None]
    ):
        super().__init__(
            monologue_id=f"monologue_{monologue_id}",
            on_finish=on_finish
        )