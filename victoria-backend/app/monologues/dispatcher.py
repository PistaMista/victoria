import threading
from sqlalchemy import event
from sqlalchemy.orm import Session

# TODO: Use a fixed thread pool instead of spawning a thread for each event

class Dispatcher(threading.Thread):
    def __init__(self):
        super().__init__(name='dispatcher', daemon=True)
        self.monologue_threads: [threading.Thread] = []
        self._stop_event: threading.Event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def run(self):
        # event.listen(Event, 'after_commit', after_commit)

        self._stop_event.wait()

        for t in self.monologue_threads:
            t.join(timeout=1.0)
    
def after_commit(session: Session):
    for obj in session.new:
        if isinstance(obj, Event):
            threading.Thread(target=monologue_thread, args=(), daemon=True).start()
        
def monologue_thread():
    threading.Event().wait()
