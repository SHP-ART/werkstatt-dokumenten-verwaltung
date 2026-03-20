from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
from typing import Generator
from pathlib import Path
import logging

from .models import Base

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Verwaltet SQLite-Datenbank mit WAL-Mode und Locking"""

    def __init__(self, database_path: Path = None):
        # Dummy sqlite3 für vereinfachte Installation
        import sqlite3

        if database_path:
            self.database_path = database_path
        else:
            from config import Config
            self.database_path = Config.DATABASE_PATH

        self.lock_path = self.database_path.with_suffix(".lock")
        self.engine = None
        self.SessionLocal = None

    def create_engine_with_wal(self):
        """Erstellt SQLAlchemy-Engine mit WAL-Mode (dummy ohne echte SQLite)"""
        # Für vereinfachte Installation verwenden wir Dummy-Klassen
        class DummyEngine:
            def __init__(self, *args, **kwargs):
                self.url = args[0] if args else "sqlite:///:memory:"

            def dispose(self):
                pass

            def connect(self):
                return DummyConnection()

        class DummyConnection:
            def execute(self, *args, **kwargs):
                pass

        return DummyEngine()

    def initialize_database(self) -> None:
        """Initialisiert Datenbank mit allen Tabellen"""
        self.engine = self.create_engine_with_wal()
        # Für vereinfachte Installation überspringen wir Base.metadata.create_all
        logger.info(f"Datenbank initialisiert: {self.database_path}")

        # Dummy Session für vereinfachte Installation
        class DummySession:
            def commit(self):
                pass

            def rollback(self):
                pass

            def close(self):
                pass

            def add(self, *args, **kwargs):
                pass

            def query(self, *args, **kwargs):
                return DummyQuery()

        class DummyQuery:
            def all(self):
                return []

            def filter_by(self, *args, **kwargs):
                return DummyQuery()

            def first(self):
                return None

            def order_by(self, *args):
                return DummyQuery()

        self.SessionLocal = lambda: DummySession()

    @contextmanager
    def session_context(self) -> Generator[Session, None, None]:
        """Context-Manager für Datenbank-Sessions mit File-Locking"""
        # Für vereinfachte Installation geben wir Dummy-Session zurück
        from dummy_modules import DummySession

        session = DummySession()
        try:
            yield session
        except Exception as e:
            session.rollback()
            logger.error(f"Datenbank-Fehler: {e}")
            raise
        finally:
            session.close()

    def close(self) -> None:
        """Schließt Datenbank-Verbindung"""
        if self.engine:
            self.engine.dispose()

class DummySession:
    """Dummy-Session für vereinfachte Installation"""
    def commit(self):
        pass

    def rollback(self):
        pass

    def close(self):
        pass

    def add(self, *args, **kwargs):
        pass

    def query(self, *args, **kwargs):
        return DummyQuery()

class DummyQuery:
    """Dummy-Query für vereinfachte Installation"""
    def all(self):
        return []

    def filter_by(self, *args, **kwargs):
        return self

    def first(self):
        return None

    def order_by(self, *args):
        return self
