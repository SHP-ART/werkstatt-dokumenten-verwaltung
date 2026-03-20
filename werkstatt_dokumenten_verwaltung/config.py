from pathlib import Path
from typing import Optional

class Config:
    """Zentrale Konfiguration für die Anwendung"""

    # Pfade
    BASE_DIR = Path(__file__).parent
    DATABASE_PATH = BASE_DIR / "data" / "werkstatt.db"
    DOCUMENTS_PATH = BASE_DIR / "data" / "Kunden"
    BACKUP_PATH = BASE_DIR / "data" / "Backups"

    # Datenbank-Konfiguration
    DATABASE_TIMEOUT = 30  # Sekunden
    DATABASE_WAL_MODE = True

    # OCR-Konfiguration
    OCR_CONFIDENCE_THRESHOLD = 60  # %
    OCR_LANGUAGES = ["deu", "eng"]

    # Backup-Konfiguration
    DAILY_BACKUP_TIME = "00:00"  # Mitternacht
    DAILY_BACKUP_RETENTION_DAYS = 30

    # Sicherheits-Konfiguration
    PASSWORD_MIN_LENGTH = 8
    SESSION_TIMEOUT_MINUTES = 30

    @classmethod
    def ensure_directories(cls) -> None:
        """Erstellt alle erforderlichen Verzeichnisse"""
        cls.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
        cls.DOCUMENTS_PATH.mkdir(parents=True, exist_ok=True)
        cls.BACKUP_PATH.mkdir(parents=True, exist_ok=True)
        (cls.BACKUP_PATH / "Täglich").mkdir(parents=True, exist_ok=True)
        (cls.BACKUP_PATH / "Manuell").mkdir(parents=True, exist_ok=True)
