"""Local single-workspace persistence; no scientific facts are synthesized here."""
from contextlib import contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
from threading import RLock
from uuid import uuid4
from werkzeug.exceptions import NotFound


def now() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def new_id() -> str:
    return uuid4().hex


class Store:
    """Transactional JSON records in SQLite, with managed private upload files.

    A single lock serializes transitions across request and worker threads. SQLite
    transactions persist complete snapshots; a provider call never holds the lock.
    Run one application process with this local worker implementation.
    """
    def __init__(self, directory: str):
        self.root = Path(directory).resolve()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.uploads = self.root / 'uploads'
        self.uploads.mkdir(exist_ok=True, mode=0o700)
        self.lock = RLock()
        with self.connection() as db:
            db.execute('CREATE TABLE IF NOT EXISTS records (kind TEXT NOT NULL, id TEXT NOT NULL, body TEXT NOT NULL, PRIMARY KEY(kind,id))')
        (self.root / 'workspace.sqlite3').chmod(0o600)

    @contextmanager
    def connection(self):
        with self.lock:
            db = sqlite3.connect(self.root / 'workspace.sqlite3', timeout=30)
            try:
                yield db
                db.commit()
            except BaseException:
                db.rollback()
                raise
            finally:
                db.close()

    def put(self, kind: str, record: dict) -> None:
        with self.connection() as db:
            db.execute('INSERT INTO records VALUES (?,?,?) ON CONFLICT(kind,id) DO UPDATE SET body=excluded.body',
                       (kind, record['id'], json.dumps(record, ensure_ascii=False, allow_nan=False)))

    def get(self, kind: str, record_id: str) -> dict:
        with self.connection() as db:
            row = db.execute('SELECT body FROM records WHERE kind=? AND id=?', (kind, record_id)).fetchone()
        if row is None:
            raise NotFound()
        return json.loads(row[0])

    def all(self, kind: str) -> list[dict]:
        with self.connection() as db:
            return [json.loads(row[0]) for row in db.execute('SELECT body FROM records WHERE kind=?', (kind,))]

    def delete(self, kind: str, record_id: str) -> None:
        with self.connection() as db:
            if db.execute('DELETE FROM records WHERE kind=? AND id=?', (kind, record_id)).rowcount == 0:
                raise NotFound()

    def event(self, record: dict, component: str, event_type: str, status: str = 'completed', **metadata) -> None:
        event = {'id': new_id(), 'timestamp': now(), 'component': component, 'type': event_type, 'status': status}
        if metadata:
            event['metadata'] = metadata
        record['events'].append(event)
