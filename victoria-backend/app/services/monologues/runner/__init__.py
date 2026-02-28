from app.services.db import DatabaseService
import threading
from app.model.monologue import Monologue, MonologueStatus
from .monologue_thread import MonologueThread
from sqlalchemy import select
from typing import Callable


class RunnerService:
    def __init__(
        self,
        db_service: DatabaseService,
        thread_factory: Callable[
            [int, Callable[[MonologueThread], None]], MonologueThread
        ],
        thread_limit: int,
    ):
        self._db: DatabaseService = db_service
        self._limit: int = thread_limit
        self._thread_factory: Callable[
            [int, Callable[[MonologueThread], None]], MonologueThread
        ] = thread_factory
        self._running_threads: [MonologueThread] = []
        self._queued_threads: [MonologueThread] = []

    def start_monologue_process(self, monologue_id: int):
        processed_threads = set(self._running_threads) | set(self._queued_threads)
        already_running = any(t._id == monologue_id for t in processed_threads)

        if already_running:
            raise AlreadyRunningError(monologue_id)

        with self._db.session() as db:
            monologue = db.scalar(select(Monologue).where(Monologue.id == monologue_id))
            if monologue is None or monologue.is_finished():
                return

            thread = self._thread_factory(monologue_id, self.on_thread_exited)
            if len(self._running_threads) < self._limit:
                self._running_threads.append(thread)
                monologue.status = MonologueStatus.RUNNING
                thread.start()
            else:
                self._queued_threads.append(thread)
                monologue.status = MonologueStatus.PENDING

            db.commit()

    def on_thread_exited(self, t: MonologueThread):
        with self._db.session() as db:
            monologue = db.scalar(select(Monologue).where(Monologue.id == t._id))
            if not monologue is None and not monologue.is_finished():
                monologue.status = MonologueStatus.FAILURE
                db.commit()

        self._running_threads.remove(t)
        if self._queued_threads:
            new_t = self._queued_threads.pop(0)

            with self._db.session() as db:
                monologue = db.scalar(
                    select(Monologue).where(Monologue.id == new_t._id)
                )
                if not monologue is None:
                    monologue.status = MonologueStatus.RUNNING
                    db.commit()

            new_t.start()
            self._running_threads.append(new_t)


class AlreadyRunningError(Exception):
    def __init__(self, id: int):
        super().__init__(f"monologue with id {id} is already queued/running")
