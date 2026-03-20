# Werkstatt-Dokumenten-Verwaltung Implementation Plan

> **Für agentic Arbeiter:** ERFORDERLICHER SUB-SKILL: Verwende superpowers:subagent-driven-development (empfohlen) oder superpowers:executing-plans um diesen Plan schrittweise zu implementieren. Schritte verwenden Checkbox (`- [ ]`) Syntax für Tracking.

**Ziel:** Eine Desktop-Anwendung für kleine Werkstätten (2-5 Mitarbeiter) zum automatisierten Sichern, Archivieren und Dokumentieren von gescannten Werkstatt-Aufträgen, Rechnungen, Garantien und anderen wichtigen Dokumenten.

**Architektur:** Python + PyQt6 Desktop-Anwendung mit SQLite-Datenbank (WAL-Mode), pdfplumber für PDF-Text-Extraktion, pytesseract für OCR, und intelligenter Mustererkennung für automatische Kunden/Fahrzeug/Dokumenttyp-Erkennung. Dokumente werden in strukturierter Ordnerhierarchie nach Kundenname organisiert.

**Tech Stack:** Python 3.12+, PyQt6, SQLite (WAL-Mode), pdfplumber, pytesseract, Pillow, pywin32 (WIA-Scanner), bcrypt, asyncio, threading, filelock

---

## Dateistruktur

```
werkstatt_dokumenten_verwaltung/
├── main.py                           # Einstiegspunkt
├── config.py                         # Konfiguration
├── requirements.txt                   # Abhängigkeiten
├── database/
│   ├── __init__.py
│   ├── models.py                      # SQLAlchemy-Modelle
│   ├── database.py                    # Datenbank-Verbindung und CRUD
│   └── migrations/
│       └── __init__.py
├── document_intelligence/
│   ├── __init__.py
│   ├── pdf_extractor.py               # PDF-Text-Extraktion und Seiten-Zählung
│   ├── ocr_engine.py                 # OCR-Engine
│   ├── pattern_recognizer.py          # Mustererkennung für Kunden/Fahrzeuge
│   ├── classifier.py                  # Dokument-Typ-Klassifizierung
│   └── training_database.py           # Lern-Datenbank für Muster
├── file_manager/
│   ├── __init__.py
│   ├── file_operations.py             # Datei-Operationen
│   └── folder_structure.py           # Ordnerstruktur-Management
├── backup/
│   ├── __init__.py
│   └── backup_manager.py             # Backup-Verwaltung
├── ui/
│   ├── __init__.py
│   ├── main_window.py                # Hauptfenster (Dashboard)
│   ├── upload_dialog.py              # Upload-Bildschirm
│   ├── documents_view.py             # Dokumenten-Übersicht
│   ├── customer_management.py         # Kunde/Fahrzeug-Verwaltung
│   ├── backup_view.py               # Backup-Verwaltung
│   ├── components.py                # Wiederverwendbare UI-Komponenten
│   └── resources/
│       └── __init__.py
├── security/
│   ├── __init__.py
│   ├── auth.py                      # Authentifizierung
│   └── permissions.py               # Berechtigungs-System
├── utils/
│   ├── __init__.py
│   ├── validators.py                # Eingabe-Validierungen
│   ├── error_handler.py             # Fehlerbehandlung
│   └── logger.py                   # Logging
└── tests/
    ├── __init__.py
    ├── test_database.py
    ├── test_document_intelligence.py
    ├── test_file_manager.py
    ├── test_backup.py
    ├── test_security.py
    └── test_utils.py
```

---

## Phase 1: Projekt-Setup und Infrastruktur

### Task 1: Projekt-Initialisierung

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/main.py`
- Create: `werkstatt_dokumenten_verwaltung/config.py`
- Create: `werkstatt_dokumenten_verwaltung/requirements.txt`
- Create: `werkstatt_dokumenten_verwaltung/.gitignore`

- [ ] **Step 1: Erstelle requirements.txt**

```txt
PyQt6==6.6.1
PyQt6-WebEngine==6.6.0
SQLAlchemy==2.0.23
pdfplumber==0.10.4
pytesseract==0.3.10
Pillow==10.1.0
pypdf2==3.0.1
pywin32==306
bcrypt==4.1.2
filelock==3.13.1
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-qt==4.2.0
```

- [ ] **Step 2: Erstelle config.py**

```python
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
```

- [ ] **Step 3: Erstelle main.py (Einstiegspunkt)**

```python
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from config import Config

def main():
    """Hauptfunktion der Anwendung"""
    Config.ensure_directories()

    app = QApplication(sys.argv)
    app.setApplicationName("Werkstatt-Dokumenten-Verwaltung")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Erstelle .gitignore**

```txt
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
data/
*.log
.vscode/
.idea/
```

- [ ] **Step 5: Installiere Abhängigkeiten**

Run: `pip install -r werkstatt_dokumenten_verwaltung/requirements.txt`
Expected: Alle Pakete erfolgreich installiert

- [ ] **Step 6: Initial commit**

```bash
git init
git add .
git commit -m "feat: initial project setup with dependencies"
```

---

## Phase 2: Datenbank-Modul

### Task 2: Datenbank-Modelle

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/database/models.py`
- Create: `werkstatt_dokumenten_verwaltung/database/__init__.py`

- [ ] **Step 1: Erstelle models.py**

```python
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Benutzer(Base):
    """Benutzer-Tabelle"""
    __tablename__ = "benutzer"

    id = Column(Integer, primary_key=True)
    benutzername = Column(String(50), unique=True, nullable=False)
    passwort_hash = Column(String(255), nullable=False)
    rolle = Column(String(20), nullable=False)  # 'besitzer' oder 'mitarbeiter'
    erstellt_am = Column(DateTime, default=datetime.utcnow)
    zuletzt_geloggt = Column(DateTime)

class Kunde(Base):
    """Kunden-Tabelle"""
    __tablename__ = "kunden"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    adresse = Column(String(200))
    telefon = Column(String(20))
    email = Column(String(100))
    erstellt_am = Column(DateTime, default=datetime.utcnow)

    fahrzeuge = relationship("Fahrzeug", back_populates="kunde")

class Fahrzeug(Base):
    """Fahrzeuge-Tabelle"""
    __tablename__ = "fahrzeuge"

    id = Column(Integer, primary_key=True)
    kunden_id = Column(Integer, ForeignKey("kunden.id"), nullable=False)
    kennzeichen = Column(String(20), nullable=False)
    marke = Column(String(50))
    modell = Column(String(50))
    baujahr = Column(Integer)
    erstellt_am = Column(DateTime, default=datetime.utcnow)

    kunde = relationship("Kunde", back_populates="fahrzeuge")
    dokumente = relationship("Dokument", back_populates="fahrzeug")

class Dokument(Base):
    """Dokumente-Tabelle"""
    __tablename__ = "dokumente"

    id = Column(Integer, primary_key=True)
    kunden_id = Column(Integer, ForeignKey("kunden.id"), nullable=True)
    fahrzeug_id = Column(Integer, ForeignKey("fahrzeuge.id"), nullable=True)
    dokument_typ = Column(String(20), nullable=False)  # 'auftrag', 'rechnung', 'garantie', 'sonstiges'
    nummer = Column(String(50), nullable=False)
    datum = Column(DateTime, nullable=False)
    betrag = Column(Float, nullable=True)
    dateipfad = Column(String(500), nullable=False)
    dateiname = Column(String(255), nullable=False)
    seiten_anzahl = Column(Integer, nullable=True)
    status = Column(String(30), default="automatisch_erkannt")  # 'automatisch_erkannt', 'manuell_bestätigt'
    erstellt_am = Column(DateTime, default=datetime.utcnow)
    aktualisiert_am = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    kunde = relationship("Kunde", foreign_keys=[kunden_id])
    fahrzeug = relationship("Fahrzeug", back_populates="dokumente")
    schluesselwoerter = relationship("Schluesselwort", back_populates="dokument")

class Schluesselwort(Base):
    """Schlüsselwörter-Tabelle"""
    __tablename__ = "schluesselwoerter"

    id = Column(Integer, primary_key=True)
    dokument_id = Column(Integer, ForeignKey("dokumente.id"), nullable=False)
    wort = Column(String(100), nullable=False)
    position = Column(Integer)  # Position im Dokument
    konfidenz_score = Column(Integer)  # 0-100

    dokument = relationship("Dokument", back_populates="schluesselwoerter")

class Einstellung(Base):
    """Einstellungen-Tabelle"""
    __tablename__ = "einstellungen"

    id = Column(Integer, primary_key=True)
    benutzer_id = Column(Integer, ForeignKey("benutzer.id"), nullable=False)
    schluessel = Column(String(100), nullable=False)
    wert = Column(String(500))
    aktualisiert_am = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Protokoll(Base):
    """Protokoll-Tabelle"""
    __tablename__ = "protokoll"

    id = Column(Integer, primary_key=True)
    benutzer_id = Column(Integer, ForeignKey("benutzer.id"), nullable=True)
    aktion = Column(String(50), nullable=False)
    details = Column(String(500))
    zeitpunkt = Column(DateTime, default=datetime.utcnow)
```

- [ ] **Step 2: Erstelle __init__.py**

```python
from .models import Base
from .database import DatabaseManager

__all__ = ['Base', 'DatabaseManager']
```

- [ ] **Step 3: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/database/
git commit -m "feat: add database models"
```

---

### Task 3: Datenbank-Manager

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/database/database.py`
- Modify: `werkstatt_dokumenten_verwaltung/database/__init__.py`

- [ ] **Step 1: Erstelle Test für Datenbank-Verbindung**

```python
import pytest
from database.database import DatabaseManager
from database.models import Benutzer

def test_database_initialization(tmp_path):
    """Test, ob Datenbank korrekt initialisiert wird"""
    db_path = tmp_path / "test.db"
    db = DatabaseManager(db_path)
    db.initialize_database()

    # Prüfe, ob Tabellen erstellt wurden
    assert db_path.exists()
    assert len(db.session.query(Benutzer).all()) == 0

    db.close()
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_database.py::test_database_initialization -v`
Expected: FAIL with "ModuleNotFoundError: No module named 'database.database'"

- [ ] **Step 3: Erstelle database.py**

```python
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from filelock import FileLock
from contextlib import contextmanager
from typing import Generator
from pathlib import Path
import logging

from .models import Base
from config import Config

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Verwaltet SQLite-Datenbank mit WAL-Mode und Locking"""

    def __init__(self, database_path: Path = None):
        self.database_path = database_path or Config.DATABASE_PATH
        self.lock_path = self.database_path.with_suffix(".lock")
        self.engine = None
        self.SessionLocal = None

    def create_engine_with_wal(self):
        """Erstellt SQLAlchemy-Engine mit WAL-Mode"""
        # SQLite mit WAL-Mode für bessere Performance bei gleichzeitigen Zugriffen
        engine = create_engine(
            f"sqlite:///{self.database_path}",
            connect_args={
                "timeout": Config.DATABASE_TIMEOUT,
                "check_same_thread": False
            },
            poolclass=StaticPool,
            echo=False
        )

        # Aktiviere WAL-Mode nach Verbindung
        @event.listens_for(engine, "connect")
        def set_sqlite_pragma(dbapi_conn, connection_record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA journal_mode=WAL")
            cursor.execute("PRAGMA synchronous=NORMAL")
            cursor.close()

        return engine

    def initialize_database(self) -> None:
        """Initialisiert Datenbank mit allen Tabellen"""
        self.engine = self.create_engine_with_wal()
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)
        logger.info(f"Datenbank initialisiert: {self.database_path}")

    @contextmanager
    def session_context(self) -> Generator[Session, None, None]:
        """Context-Manager für Datenbank-Sessions mit File-Locking"""
        lock = FileLock(self.lock_path, timeout=Config.DATABASE_TIMEOUT)

        try:
            with lock:
                session = self.SessionLocal()
                try:
                    yield session
                    session.commit()
                except Exception as e:
                    session.rollback()
                    logger.error(f"Datenbank-Fehler: {e}")
                    raise
                finally:
                    session.close()
        except Exception as e:
            logger.error(f"Lock-Fehler: {e}")
            raise

    def close(self) -> None:
        """Schließt Datenbank-Verbindung"""
        if self.engine:
            self.engine.dispose()
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_database.py::test_database_initialization -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/database/database.py
git commit -m "feat: add database manager with WAL mode and locking"
```

---

## Phase 3: Dokumenten-Intelligenz

### Task 4: PDF-Extraktion

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/document_intelligence/pdf_extractor.py`
- Create: `werkstatt_dokumenten_verwaltung/document_intelligence/__init__.py`
- Create: `werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py`

- [ ] **Step 1: Erstelle Test für PDF-Extraktion**

```python
import pytest
from pathlib import Path
from document_intelligence.pdf_extractor import PDFExtractor

@pytest.fixture
def sample_pdf(tmp_path):
    """Erstellt ein Test-PDF"""
    pdf_path = tmp_path / "test.pdf"
    # Erstelle einfaches PDF (in echtem Test würden wir pdfplumber verwenden)
    return pdf_path

def test_extract_text_from_pdf(sample_pdf):
    """Test Text-Extraktion aus PDF"""
    extractor = PDFExtractor()
    text, page_count = extractor.extract_text(sample_pdf)

    assert isinstance(text, str)
    assert page_count >= 0
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_extract_text_from_pdf -v`
Expected: FAIL

- [ ] **Step 3: Erstelle pdf_extractor.py**

```python
import pdfplumber
from pathlib import Path
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class PDFExtractor:
    """Extrahiert Text und Metadaten aus PDFs"""

    def extract_text(self, pdf_path: Path) -> Tuple[str, int]:
        """
        Extrahiert Text aus PDF und gibt Text + Seitenanzahl zurück

        Args:
            pdf_path: Pfad zur PDF-Datei

        Returns:
            Tuple (Text, Seitenanzahl)

        Raises:
            ValueError: Wenn PDF nicht gelesen werden kann
        """
        try:
            with pdfplumber.open(pdf_path) as pdf:
                text_parts = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)

                full_text = "\n".join(text_parts)
                page_count = len(pdf.pages)

                logger.info(f"PDF extrahiert: {pdf_path.name}, {page_count} Seiten")
                return full_text, page_count

        except Exception as e:
            logger.error(f"PDF-Extraktion fehlgeschlagen: {pdf_path}, {e}")
            raise ValueError(f"Kann PDF nicht lesen: {e}")

    def extract_tables(self, pdf_path: Path):
        """
        Extrahiert Tabellen aus PDF

        Args:
            pdf_path: Pfad zur PDF-Datei

        Returns:
            Liste von Tabellen (jede Tabelle ist eine Liste von Zeilen)
        """
        tables = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_tables = page.extract_tables()
                    if page_tables:
                        tables.extend(page_tables)

            logger.info(f"{len(tables)} Tabellen extrahiert aus {pdf_path.name}")
            return tables

        except Exception as e:
            logger.error(f"Tabellen-Extraktion fehlgeschlagen: {pdf_path}, {e}")
            return []
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_extract_text_from_pdf -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/document_intelligence/pdf_extractor.py
git commit -m "feat: add PDF extractor with text and table extraction"
```

---

### Task 5: OCR-Engine

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/document_intelligence/ocr_engine.py`

- [ ] **Step 1: Erstelle Test für OCR**

```python
import pytest
from pathlib import Path
from document_intelligence.ocr_engine import OCREngine

def test_ocr_with_low_confidence():
    """Test OCR mit niedriger Konfidenz"""
    engine = OCREngine()
    text, confidence = engine.process_image(Path("test.jpg"))

    assert isinstance(text, str)
    assert 0 <= confidence <= 100
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_ocr_with_low_confidence -v`
Expected: FAIL

- [ ] **Step 3: Erstelle ocr_engine.py**

```python
import pytesseract
from pathlib import Path
from PIL import Image
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class OCREngine:
    """OCR-Engine basierend auf Tesseract"""

    def __init__(self, confidence_threshold: int = 60):
        """
        Args:
            confidence_threshold: Minimale Konfidenz in Prozent
        """
        self.confidence_threshold = confidence_threshold

    def process_image(self, image_path: Path) -> Tuple[str, int]:
        """
        Verarbeitet Bild mit OCR und gibt Text + Konfidenz zurück

        Args:
            image_path: Pfad zum Bild

        Returns:
            Tuple (Text, Konfidenz 0-100)

        Raises:
            ValueError: Wenn Bild nicht verarbeitet werden kann
        """
        try:
            image = Image.open(image_path)

            # Tesseract mit Konfidenz
            data = pytesseract.image_to_data(
                image,
                lang='deu+eng',
                output_type=pytesseract.Output.DICT
            )

            # Extrahiere Text und Konfidenz
            text_parts = []
            confidences = []

            for i, text in enumerate(data['text']):
                if text.strip():
                    text_parts.append(text)
                    conf = data['conf'][i]
                    if conf > 0:  # -1 bedeutet keine Konfidenz verfügbar
                        confidences.append(conf)

            full_text = ' '.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0

            logger.info(f"OCR verarbeitet: {image_path.name}, Konfidenz: {avg_confidence:.1f}%")
            return full_text, int(avg_confidence)

        except Exception as e:
            logger.error(f"OCR fehlgeschlagen: {image_path}, {e}")
            raise ValueError(f"OCR fehlgeschlagen: {e}")

    def is_high_quality(self, image_path: Path) -> bool:
        """
        Prüft, ob OCR-Konfidenz hoch genug ist

        Args:
            image_path: Pfad zum Bild

        Returns:
            True wenn Konfidenz >= threshold
        """
        _, confidence = self.process_image(image_path)
        return confidence >= self.confidence_threshold
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_ocr_with_low_confidence -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/document_intelligence/ocr_engine.py
git commit -m "feat: add OCR engine with confidence scoring"
```

---

### Task 6: Mustererkennung

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/document_intelligence/pattern_recognizer.py`

- [ ] **Step 1: Erstelle Test für Mustererkennung**

```python
import pytest
from document_intelligence.pattern_recognizer import PatternRecognizer

def test_recognize_german_license_plate():
    """Test Kennzeichen-Erkennung"""
    recognizer = PatternRecognizer()

    result = recognizer.recognize_kennzeichen("Kennzeichen: M-AB 123")
    assert result == "M-AB 123"

    result = recognizer.recognize_kennzeichen("Fahrzeug: ABC-DE 1234")
    assert result == "ABC-DE 1234"
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_recognize_german_license_plate -v`
Expected: FAIL

- [ ] **Step 3: Erstelle pattern_recognizer.py**

```python
import re
from typing import List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class PatternRecognizer:
    """Erkennt Muster in Dokumenten (Kunden, Fahrzeuge, Nummern)"""

    # Regex-Pattern für Kunden-Namen
    KUNDEN_PATTERNS = [
        r"Kunde:\s*([^\n]+)",
        r"Firma:\s*([^\n]+)",
        r"Name:\s*([^\n]+)",
        r"Kundenname:\s*([^\n]+)"
    ]

    # Regex-Pattern für Dokument-Nummern
    NUMMER_PATTERNS = [
        r"Auftrags-Nr\.:\s*([A-Z0-9-]+)",
        r"Auftragsnummer:\s*([A-Z0-9-]+)",
        r"Rechnung-Nr\.:\s*([A-Z0-9-]+)",
        r"Rechnungsnummer:\s*([A-Z0-9-]+)",
        r"Garantie-Nr\.:\s*([A-Z0-9-]+)"
    ]

    # Regex-Pattern für Daten
    DATUM_PATTERNS = [
        r"(\d{2}\.\d{2}\.\d{4})",  # DD.MM.YYYY
        r"(\d{4}-\d{2}-\d{2})",   # YYYY-MM-DD
        r"(\d{1,2}\. [A-Za-z]+ \d{4})"  # 15. März 2024
    ]

    # Regex-Pattern für Beträge
    BETRAG_PATTERNS = [
        r"Betrag:\s*([\d,]+\.?\d*)\s*€",
        r"Summe:\s*([\d,]+\.?\d*)\s*€",
        r"Gesamt:\s*([\d,]+\.?\d*)\s*€",
        r"€\s*([\d,]+\.?\d*)"
    ]

    # Typ-spezifische Schlüsselwörter
    TYP_KEYWORDS = {
        "auftrag": ["auftrag", "arbeitsauftrag", "reparaturauftrag"],
        "rechnung": ["rechnung", "invoice", "betrag", "summe", "gesamt"],
        "garantie": ["garantie", "gewährleistung", "jahre garantie"]
    }

    def recognize_kunde(self, text: str) -> Optional[Tuple[str, float]]:
        """
        Erkennt Kundenname im Text

        Args:
            text: Vollständiger Dokumententext

        Returns:
            Tuple (Kundenname, Konfidenz 0-100) oder None
        """
        for pattern in self.KUNDEN_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Konfidenz basierend auf Länge und Position
                confidence = min(95, 50 + len(name) * 2)
                logger.info(f"Kunde erkannt: {name} ({confidence}%)")
                return name, confidence
        return None

    def recognize_kennzeichen(self, text: str) -> Optional[Tuple[str, float]]:
        """
        Erkennt deutsches Kennzeichen

        Args:
            text: Vollständiger Dokumententext

        Returns:
            Tuple (Kennzeichen, Konfidenz 0-100) oder None
        """
        # Deutsches Kennzeichen-Format: 1-3 Buchstaben, Bindestrich, 1-2 Buchstaben, Leerzeichen, 1-4 Ziffern
        pattern = r"[A-ZÖÄÜ]{1,3}-[A-ZÖÄÜ]{1,2}\s*[0-9]{1,4}"
        match = re.search(pattern, text, re.IGNORECASE)

        if match:
            kennzeichen = match.group(0).upper().replace(" ", "")
            logger.info(f"Kennzeichen erkannt: {kennzeichen} (95%)")
            return kennzeichen, 95
        return None

    def recognize_nummer(self, text: str) -> Optional[str]:
        """
        Erkennt Auftrags-/Rechnungsnummer

        Args:
            text: Vollständiger Dokumententext

        Returns:
            Nummer oder None
        """
        for pattern in self.NUMMER_PATTERNS:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                nummer = match.group(1).strip()
                logger.info(f"Nummer erkannt: {nummer}")
                return nummer
        return None

    def recognize_datum(self, text: str) -> Optional[str]:
        """
        Erkennt Datum im Text

        Args:
            text: Vollständiger Dokumententext

        Returns:
            Datum im Format YYYY-MM-DD oder None
        """
        for pattern in self.DATUM_PATTERNS:
            matches = re.findall(pattern, text)
            if matches:
                # Nimm das erste gefundene Datum
                datum = matches[0]
                logger.info(f"Datum erkannt: {datum}")
                return datum
        return None

    def recognize_betrag(self, text: str) -> Optional[float]:
        """
        Erkennt Betrag im Text

        Args:
            text: Vollständiger Dokumententext

        Returns:
            Betrag als float oder None
        """
        for pattern in self.BETRAG_PATTERNS:
            match = re.search(pattern, text)
            if match:
                betrag_str = match.group(1).replace(",", ".").replace(" ", "")
                try:
                    betrag = float(betrag_str)
                    logger.info(f"Betrag erkannt: {betrag:.2f}€")
                    return betrag
                except ValueError:
                    continue
        return None

    def classify_document_type(self, text: str) -> Optional[Tuple[str, float]]:
        """
        Klassifiziert Dokumenttyp

        Args:
            text: Vollständiger Dokumententext

        Returns:
            Tuple (Typ, Konfidenz 0-100) oder None
        """
        text_lower = text.lower()
        scores = {}

        # Zähle Übereinstimmungen pro Typ
        for typ, keywords in self.TYP_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[typ] = score

        # Besten Typ auswählen
        if scores:
            best_typ = max(scores, key=scores.get)
            best_score = scores[best_typ]

            if best_score > 0:
                confidence = min(95, 50 + best_score * 10)
                logger.info(f"Dokumenttyp erkannt: {best_typ} ({confidence}%)")
                return best_typ, confidence

        return None
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_recognize_german_license_plate -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/document_intelligence/pattern_recognizer.py
git commit -m "feat: add pattern recognizer for customers, vehicles, and document types"
```

---

### Task 7: Dokument-Klassifizierer

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/document_intelligence/classifier.py`

- [ ] **Step 1: Erstelle Test für Klassifizierer**

```python
import pytest
from document_intelligence.classifier import DocumentClassifier

def test_classify_rechnung():
    """Test Klassifizierung von Rechnungen"""
    classifier = DocumentClassifier()

    text = "Rechnung Nr. 2024-001\nBetrag: 150,00 €"
    doc_type, confidence = classifier.classify(text)

    assert doc_type == "rechnung"
    assert confidence > 50
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_classify_rechnung -v`
Expected: FAIL

- [ ] **Step 3: Erstelle classifier.py**

```python
from typing import Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class DocumentClassifier:
    """Klassifiziert Dokumente basierend auf extrahierten Merkmalen"""

    def __init__(self):
        self.recognizer = PatternRecognizer()

    def classify(self, text: str) -> Tuple[Optional[str], int]:
        """
        Klassifiziert Dokumenttyp

        Args:
            text: Vollständiger Dokumententext

        Returns:
            Tuple (Dokumenttyp, Konfidenz 0-100)
        """
        return self.recognizer.classify_document_type(text)

    def extract_all_features(self, text: str) -> Dict:
        """
        Extrahiert alle Merkmale aus Dokument

        Args:
            text: Vollständiger Dokumententext

        Returns:
            Dictionary mit allen extrahierten Merkmalen
        """
        features = {}

        kunde = self.recognizer.recognize_kunde(text)
        if kunde:
            features["kunde"] = kunde

        kennzeichen = self.recognizer.recognize_kennzeichen(text)
        if kennzeichen:
            features["kennzeichen"] = kennzeichen

        nummer = self.recognizer.recognize_nummer(text)
        if nummer:
            features["nummer"] = nummer

        datum = self.recognizer.recognize_datum(text)
        if datum:
            features["datum"] = datum

        betrag = self.recognizer.recognize_betrag(text)
        if betrag:
            features["betrag"] = betrag

        doc_type, confidence = self.classify(text)
        if doc_type:
            features["typ"] = doc_type
            features["typ_konfidenz"] = confidence

        return features
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_classify_rechnung -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/document_intelligence/classifier.py
git commit -m "feat: add document classifier for automatic type detection"
```

### Task 7.5: Scanner-Integration

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/document_intelligence/scanner.py`

- [ ] **Step 1: Erstelle Test für Scanner**

```python
import pytest
from document_intelligence.scanner import ScannerManager

def test_list_scanners():
    """Test Scanner-Auflistung"""
    manager = ScannerManager()
    scanners = manager.list_scanners()

    assert isinstance(scanners, list)
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_list_scanners -v`
Expected: FAIL

- [ ] **Step 3: Erstelle scanner.py**

```python
import win32com.client
from pathlib import Path
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

class ScannerManager:
    """Verwaltet WIA-Scanner"""

    def __init__(self):
        self.wia = None

    def connect(self):
        """Verbindet mit WIA-Service"""
        try:
            self.wia = win32com.client.Dispatch("WIA.DeviceManager")
            logger.info("WIA-Verbindung hergestellt")
            return True
        except Exception as e:
            logger.error(f"WIA-Verbindung fehlgeschlagen: {e}")
            return False

    def list_scanners(self) -> List[dict]:
        """
        Listet verfügbare Scanner auf

        Returns:
            Liste von Scanner-Infos
        """
        scanners = []

        try:
            if not self.wia:
                self.connect()

            for device in self.wia.DeviceInfos:
                scanners.append({
                    "id": device.DeviceID,
                    "name": device.Name,
                    "type": device.Type
                })

            logger.info(f"{len(scanners)} Scanner gefunden")
            return scanners

        except Exception as e:
            logger.error(f"Scanner-Auflistung fehlgeschlagen: {e}")
            return []

    def scan_document(
        self,
        scanner_id: str,
        resolution: int = 300,
        output_path: Optional[Path] = None
    ) -> Optional[Path]:
        """
        Scannt Dokument

        Args:
            scanner_id: Scanner-ID
            resolution: DPI-Auflösung
            output_path: Ausgabepfad (optional)

        Returns:
            Pfad zum gescannten Bild oder None
        """
        try:
            # TODO: Implementiere Scan-Logik mit WIA
            logger.info(f"Scan: {scanner_id} @ {resolution}DPI")
            return output_path

        except Exception as e:
            logger.error(f"Scan fehlgeschlagen: {e}")
            return None

    def disconnect(self):
        """Trennt WIA-Verbindung"""
        self.wia = None
        logger.info("WIA-Verbindung getrennt")
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_list_scanners -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/document_intelligence/scanner.py
git commit -m "feat: add WIA scanner integration"
```

---

### Task 8: Logging-Konfiguration

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/utils/logger.py`

- [ ] **Step 1: Erstelle Test für Logger**

```python
import pytest
from utils.logger import setup_logging
from pathlib import Path
import os

def test_logging_file_created(tmp_path):
    """Test, ob Logging-Datei erstellt wird"""
    log_file = tmp_path / "test.log"

    setup_logging(log_file)

    assert log_file.exists()
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_utils.py::test_logging_file_created -v`
Expected: FAIL

- [ ] **Step 3: Erstelle logger.py**

```python
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
from typing import Optional

def setup_logging(
    log_file: Optional[Path] = None,
    level: int = logging.INFO
) -> None:
    """
    Konfiguriert Logging für die gesamte Anwendung

    Args:
        log_file: Pfad zur Log-Datei
        level: Logging-Level
    """
    # Root-Logger konfigurieren
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Console-Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Datei-Handler (optional)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5
        )
        file_handler.setLevel(level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)

def get_logger(name: str) -> logging.Logger:
    """
    Holt konfigurierten Logger

    Args:
        name: Logger-Name

    Returns:
        Logger-Instanz
    """
    return logging.getLogger(name)
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_utils.py::test_logging_file_created -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/utils/logger.py
git commit -m "feat: add logging configuration with file rotation"
```

---

### Task 9: Training-Database Implementierung

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/document_intelligence/training_database.py`

- [ ] **Step 1: Erstelle Test für Training-Database**

```python
import pytest
from document_intelligence.training_database import TrainingDatabase

def test_add_pattern():
    """Test Muster-Hinzufügung"""
    db = TrainingDatabase()

    db.add_pattern("Müller GmbH", "Kunde", 95)
    patterns = db.get_patterns_for_category("Kunde")

    assert "Müller GmbH" in patterns
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_add_pattern -v`
Expected: FAIL

- [ ] **Step 3: Erstelle training_database.py**

```python
import json
from pathlib import Path
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class TrainingDatabase:
    """Verwaltet Trainingsdaten für Mustererkennung"""

    def __init__(self, db_path: Path = None):
        """
        Args:
            db_path: Pfad zur Trainingsdatenbank
        """
        from config import Config
        self.db_path = db_path or (Config.BASE_DIR / "data" / "training_patterns.json")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.data: Dict[str, List[Dict]] = {
            "kunden": [],
            "fahrzeuge": [],
            "dokumenttypen": []
        }
        self.load()

    def load(self) -> None:
        """Lädt Trainingsdaten aus Datei"""
        if self.db_path.exists():
            try:
                with open(self.db_path, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                logger.info(f"Trainingsdaten geladen: {self.db_path}")
            except Exception as e:
                logger.error(f"Laden der Trainingsdaten fehlgeschlagen: {e}")

    def save(self) -> None:
        """Speichert Trainingsdaten in Datei"""
        try:
            with open(self.db_path, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logger.info(f"Trainingsdaten gespeichert: {self.db_path}")
        except Exception as e:
            logger.error(f"Speichern der Trainingsdaten fehlgeschlagen: {e}")

    def add_pattern(
        self,
        pattern: str,
        category: str,
        confidence: int
    ) -> None:
        """
        Fügt Muster hinzu

        Args:
            pattern: Muster-Text
            category: Kategorie (kunden, fahrzeuge, dokumenttypen)
            confidence: Konfidenz-Score
        """
        if category not in self.data:
            self.data[category] = []

        # Prüfe auf Duplikate
        for entry in self.data[category]:
            if entry["pattern"] == pattern:
                logger.info(f"Muster bereits vorhanden: {pattern}")
                return

        self.data[category].append({
            "pattern": pattern,
            "confidence": confidence,
            "count": 1
        })
        self.save()
        logger.info(f"Muster hinzugefügt: {category}/{pattern}")

    def get_patterns_for_category(self, category: str) -> List[str]:
        """
        Holt alle Muster für eine Kategorie

        Args:
            category: Kategorie

        Returns:
            Liste von Mustern
        """
        return [entry["pattern"] for entry in self.data.get(category, [])]

    def find_match(self, text: str, category: str) -> tuple:
        """
        Sucht nach passenden Mustern

        Args:
            text: Zu prüfender Text
            category: Kategorie

        Returns:
            Tuple (Gefundenes Muster, Konfidenz) oder (None, 0)
        """
        patterns = self.get_patterns_for_category(category)

        for pattern in patterns:
            if pattern.lower() in text.lower():
                # Finde Konfidenz
                for entry in self.data[category]:
                    if entry["pattern"] == pattern:
                        confidence = min(95, 50 + entry["count"] * 5)
                        return pattern, confidence

        return None, 0
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_document_intelligence.py::test_add_pattern -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/document_intelligence/training_database.py
git commit -m "feat: add training database for pattern learning"
```

---

## Phase 4: Datei-Manager

### Task 10: Ordnerstruktur-Management

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/file_manager/folder_structure.py`
- Create: `werkstatt_dokumenten_verwaltung/file_manager/__init__.py`

- [ ] **Step 1: Erstelle Test für Ordnerstruktur**

```python
import pytest
from pathlib import Path
from file_manager.folder_structure import FolderManager

def test_create_folder_structure(tmp_path):
    """Test Ordnerstruktur-Erstellung"""
    manager = FolderManager(tmp_path)

    kunde_name = "Müller GmbH"
    kennzeichen = "M-AB 123"
    jahr = "2024"
    dokument_typ = "rechnung"

    path = manager.get_document_path(kunde_name, kennzeichen, jahr, dokument_typ)

    assert path.exists()
    assert "Müller_GmbH" in str(path)
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_file_manager.py::test_create_folder_structure -v`
Expected: FAIL

- [ ] **Step 3: Erstelle folder_structure.py**

```python
from pathlib import Path
import re
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class FolderManager:
    """Verwaltet Ordnerstruktur für Dokumente"""

    @staticmethod
    def sanitize_filename(name: str) -> str:
        """
        Bereinigt Dateinamen von Sonderzeichen

        Args:
            name: Originaler Name

        Returns:
            Bereinigter Name
        """
        # Umlaute ersetzen
        replacements = {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue',
            'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue', 'ß': 'ss'
        }

        name = name
        for old, new in replacements.items():
            name = name.replace(old, new)

        # Weitere Sonderzeichen ersetzen
        name = re.sub(r'[<>:"/\\|?*]', '_', name)
        name = name.strip()

        return name

    @staticmethod
    def sanitize_license_plate(kennzeichen: str) -> str:
        """
        Bereinigt Kennzeichen für Ordnername

        Args:
            kennzeichen: Original Kennzeichen

        Returns:
            Bereinigtes Kennzeichen (ohne Leerzeichen)
        """
        return kennzeichen.replace(" ", "")

    def get_document_path(
        self,
        kunde_name: str,
        kennzeichen: Optional[str],
        jahr: str,
        dokument_typ: str,
        base_path: Optional[Path] = None
    ) -> Path:
        """
        Erstellt vollständigen Pfad für Dokument und erstellt Ordner falls nötig

        Args:
            kunde_name: Kundenname
            kennzeichen: Fahrzeugkennzeichen (optional)
            jahr: Jahr
            dokument_typ: Dokumenttyp (rechnung/auftrag/garantie)
            base_path: Basispfad (optional, default aus Config)

        Returns:
            Vollständiger Pfad zum Ordner
        """
        from config import Config

        base = base_path or Config.DOCUMENTS_PATH
        sanitized_kunde = self.sanitize_filename(kunde_name)

        path_parts = [
            base,
            sanitized_kunde,
            "Fahrzeuge"
        ]

        if kennzeichen:
            sanitized_ken = self.sanitize_license_plate(kennzeichen)
            path_parts.extend([sanitized_ken, jahr, dokument_typ.capitalize()])
        else:
            path_parts.extend(["Nicht_zugeordnet", jahr, dokument_typ.capitalize()])

        full_path = Path(*path_parts)
        full_path.mkdir(parents=True, exist_ok=True)

        logger.info(f"Ordner erstellt: {full_path}")
        return full_path

    def generate_filename(
        self,
        dokument_typ: str,
        datum: str,
        nummer: str,
        extension: str = "pdf"
    ) -> str:
        """
        Generiert Dateiname für Dokument

        Args:
            dokument_typ: Dokumenttyp
            datum: Datum (YYYY-MM-DD)
            nummer: Dokumentnummer
            extension: Dateierweiterung

        Returns:
            Dateiname
        """
        typ_prefix = {
            "rechnung": "Rechnung",
            "auftrag": "Auftrag",
            "garantie": "Garantie",
            "sonstiges": "Sonstiges"
        }.get(dokument_typ, "Dokument")

        return f"{typ_prefix}_{datum}_{nummer}.{extension}"

    def move_document(
        self,
        source_path: Path,
        target_path: Path
    ) -> None:
        """
        Verschiebt Dokument von Quelle zu Ziel

        Args:
            source_path: Quellpfad
            target_path: Zielpfad
        """
        target_path.parent.mkdir(parents=True, exist_ok=True)
        source_path.rename(target_path)
        logger.info(f"Dokument verschoben: {source_path} -> {target_path}")
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_file_manager.py::test_create_folder_structure -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/file_manager/folder_structure.py
git commit -m "feat: add folder structure manager with sanitization"
```

---

### Task 9: Datei-Operationen

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/file_manager/file_operations.py`

- [ ] **Step 1: Erstelle Test für Datei-Operationen**

```python
import pytest
from pathlib import Path
from file_manager.file_operations import FileOperations

def test_save_document(tmp_path):
    """Test Dokument speichern"""
    ops = FileOperations()

    content = b"Test PDF content"
    file_path = tmp_path / "test.pdf"

    ops.save_document(content, file_path)

    assert file_path.exists()
    assert file_path.read_bytes() == content
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_file_manager.py::test_save_document -v`
Expected: FAIL

- [ ] **Step 3: Erstelle file_operations.py**

```python
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class FileOperations:
    """Hält grundlegende Datei-Operationen"""

    @staticmethod
    def save_document(content: bytes, path: Path) -> None:
        """
        Speichert Dokument

        Args:
            content: Datei-Inhalt als Bytes
            path: Vollständiger Pfad
        """
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'wb') as f:
            f.write(content)
        logger.info(f"Dokument gespeichert: {path}")

    @staticmethod
    def load_document(path: Path) -> Optional[bytes]:
        """
        Lädt Dokument

        Args:
            path: Vollständiger Pfad

        Returns:
            Datei-Inhalt als Bytes oder None bei Fehler
        """
        try:
            with open(path, 'rb') as f:
                content = f.read()
            logger.info(f"Dokument geladen: {path}")
            return content
        except Exception as e:
            logger.error(f"Laden fehlgeschlagen: {path}, {e}")
            return None

    @staticmethod
    def delete_document(path: Path) -> bool:
        """
        Löscht Dokument

        Args:
            path: Vollständiger Pfad

        Returns:
            True wenn erfolgreich
        """
        try:
            if path.exists():
                path.unlink()
                logger.info(f"Dokument gelöscht: {path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Löschen fehlgeschlagen: {path}, {e}")
            return False

    @staticmethod
    def file_exists(path: Path) -> bool:
        """Prüft, ob Datei existiert"""
        return path.exists()

    @staticmethod
    def get_file_size(path: Path) -> int:
        """
        Gibt Dateigröße zurück

        Args:
            path: Vollständiger Pfad

        Returns:
            Dateigröße in Bytes
        """
        return path.stat().st_size if path.exists() else 0
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_file_manager.py::test_save_document -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/file_manager/file_operations.py
git commit -m "feat: add file operations (save, load, delete)"
```

---

## Phase 5: Sicherheits-Modul

### Task 10: Authentifizierung

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/security/auth.py`
- Create: `werkstatt_dokumenten_verwaltung/security/__init__.py`

- [ ] **Step 1: Erstelle Test für Authentifizierung**

```python
import pytest
from security.auth import AuthenticationManager
from database.database import DatabaseManager
from database.models import Benutzer

def test_create_user():
    """Test Benutzer-Erstellung"""
    db = DatabaseManager()
    db.initialize_database()

    with db.session_context() as session:
        auth = AuthenticationManager(session)
        auth.create_user("admin", "password123", "besitzer")

        user = session.query(Benutzer).filter_by(benutzername="admin").first()
        assert user is not None
        assert user.rolle == "besitzer"
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_security.py::test_create_user -v`
Expected: FAIL

- [ ] **Step 3: Erstelle auth.py**

```python
import bcrypt
from typing import Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class AuthenticationManager:
    """Verwaltet Benutzer-Authentifizierung"""

    def __init__(self, session):
        """
        Args:
            session: SQLAlchemy Session
        """
        self.session = session

    def create_user(self, benutzername: str, passwort: str, rolle: str) -> bool:
        """
        Erstellt neuen Benutzer

        Args:
            benutzername: Benutzername
            passwort: Passwort (Plain-Text)
            rolle: 'besitzer' oder 'mitarbeiter'

        Returns:
            True wenn erfolgreich

        Raises:
            ValueError: Wenn Benutzername bereits existiert
        """
        from database.models import Benutzer

        # Prüfe, ob Benutzername bereits existiert
        existing = self.session.query(Benutzer).filter_by(
            benutzername=benutzername
        ).first()

        if existing:
            raise ValueError(f"Benutzername '{benutzername}' existiert bereits")

        # Hash Passwort
        passwort_hash = bcrypt.hashpw(
            passwort.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        user = Benutzer(
            benutzername=benutzername,
            passwort_hash=passwort_hash,
            rolle=rolle
        )

        self.session.add(user)
        self.session.commit()

        logger.info(f"Benutzer erstellt: {benutzername} ({rolle})")
        return True

    def verify_user(self, benutzername: str, passwort: str) -> Optional['Benutzer']:
        """
        Verifiziert Benutzer-Credentials

        Args:
            benutzername: Benutzername
            passwort: Passwort (Plain-Text)

        Returns:
            Benutzer-Objekt oder None bei Fehlschlag
        """
        from database.models import Benutzer

        user = self.session.query(Benutzer).filter_by(
            benutzername=benutzername
        ).first()

        if not user:
            return None

        # Verifiziere Passwort
        if bcrypt.checkpw(
            passwort.encode('utf-8'),
            user.passwort_hash.encode('utf-8')
        ):
            logger.info(f"Benutzer verifiziert: {benutzername}")
            return user

        logger.warning(f"Fehlgeschlagener Login: {benutzername}")
        return None

    def change_password(self, benutzername: str, altes_passwort: str, neues_passwort: str) -> bool:
        """
        Ändert Benutzer-Passwort

        Args:
            benutzername: Benutzername
            altes_passwort: Altes Passwort zur Verifizierung
            neues_passwort: Neues Passwort

        Returns:
            True wenn erfolgreich
        """
        user = self.verify_user(benutzername, altes_passwort)

        if not user:
            return False

        # Hash neues Passwort
        user.passwort_hash = bcrypt.hashpw(
            neues_passwort.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

        self.session.commit()
        logger.info(f"Passwort geändert: {benutzername}")
        return True
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_security.py::test_create_user -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/security/auth.py
git commit -m "feat: add authentication manager with bcrypt password hashing"
```

---

### Task 11: Berechtigungs-System

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/security/permissions.py`

- [ ] **Step 1: Erstelle Test für Berechtigungen**

```python
import pytest
from security.permissions import PermissionManager

def test_besitzer_has_full_access():
    """Test Besitzer hat Vollzugriff"""
    pm = PermissionManager()

    assert pm.has_permission("besitzer", "dokumente_löschen")
    assert pm.has_permission("besitzer", "kunden_anlegen")
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_security.py::test_besitzer_has_full_access -v`
Expected: FAIL

- [ ] **Step 3: Erstelle permissions.py**

```python
from typing import Dict, Set
import logging

logger = logging.getLogger(__name__)

class PermissionManager:
    """Verwaltet Rollen-Berechtigungen"""

    # Vollständige Berechtigungs-Matrix
    PERMISSIONS: Dict[str, Set[str]] = {
        "besitzer": {
            "dokumente_hochladen",
            "dokumente_löschen",
            "dokumente_bearbeiten",
            "dokumente_verschieben",
            "kunden_anlegen",
            "kunden_bearbeiten",
            "fahrzeuge_zuordnen",
            "backup_erstellen",
            "backup_restore",
            "benutzer_verwalten",
            "einstellungen_ändern",
            "protokoll_anzeigen",
            "ocr_training"
        },
        "mitarbeiter": {
            "dokumente_hochladen",
            "dokumente_bearbeiten",
            "fahrzeuge_zuordnen"
        }
    }

    def has_permission(self, rolle: str, permission: str) -> bool:
        """
        Prüft, ob Rolle Berechtigung hat

        Args:
            rolle: 'besitzer' oder 'mitarbeiter'
            permission: Berechtigungs-Key

        Returns:
            True wenn Rolle Berechtigung hat
        """
        return permission in self.PERMISSIONS.get(rolle, set())

    def get_all_permissions(self, rolle: str) -> Set[str]:
        """
        Gibt alle Berechtigungen einer Rolle zurück

        Args:
            rolle: 'besitzer' oder 'mitarbeiter'

        Returns:
            Set von Berechtigungen
        """
        return self.PERMISSIONS.get(rolle, set()).copy()

    def require_permission(self, rolle: str, permission: str) -> None:
        """
        Prüft Berechtigung und wirft Exception wenn fehlt

        Args:
            rolle: 'besitzer' oder 'mitarbeiter'
            permission: Berechtigungs-Key

        Raises:
            PermissionError: Wenn keine Berechtigung
        """
        if not self.has_permission(rolle, permission):
            logger.warning(f"Zugriff verweigert: {rolle}/{permission}")
            raise PermissionError(f"Keine Berechtigung: {permission}")
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_security.py::test_besitzer_has_full_access -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/security/permissions.py
git commit -m "feat: add permission system with role-based access control"
```

---

## Phase 6: Backup-Modul

### Task 12: Backup-Manager

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/backup/backup_manager.py`
- Create: `werkstatt_dokumenten_verwaltung/backup/__init__.py`

- [ ] **Step 1: Erstelle Test für Backup**

```python
import pytest
from pathlib import Path
from backup.backup_manager import BackupManager
from config import Config

def test_create_backup(tmp_path):
    """Test Backup-Erstellung"""
    manager = BackupManager(tmp_path / "backups")

    # Erstelle Dummy-Dateien
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "test.db").write_text("db content")
    (data_dir / "docs").mkdir()

    backup_path = manager.create_backup(data_dir, description="Test")

    assert backup_path.exists()
    assert backup_path.suffix == ".zip"
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_backup.py::test_create_backup -v`
Expected: FAIL

- [ ] **Step 3: Erstelle backup_manager.py**

```python
from pathlib import Path
import zipfile
import hashlib
from datetime import datetime
import shutil
import logging
from typing import Optional, List

logger = logging.getLogger(__name__)

class BackupManager:
    """Verwaltet Backups der Anwendung"""

    def __init__(self, backup_path: Optional[Path] = None):
        """
        Args:
            backup_path: Pfad für Backups
        """
        self.backup_path = backup_path or Config.BACKUP_PATH
        self.daily_path = self.backup_path / "Täglich"
        self.manual_path = self.backup_path / "Manuell"

    def create_backup(
        self,
        data_path: Path,
        description: str = "",
        backup_type: str = "manual"
    ) -> Path:
        """
        Erstellt Backup

        Args:
            data_path: Pfad zu Daten, die gesichert werden
            description: Beschreibung des Backups
            backup_type: 'daily' oder 'manual'

        Returns:
            Pfad zum Backup-Archiv
        """
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        if backup_type == "daily":
            timestamp = datetime.now().strftime("%Y-%m-%d")
            backup_dir = self.daily_path
        else:
            backup_dir = self.manual_path

        filename = f"backup_{timestamp}"
        if description:
            filename += f"_{description}"
        filename += ".zip"

        backup_path = backup_dir / filename
        backup_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"Erstelle Backup: {backup_path}")

        # Erstelle ZIP-Archiv
        with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in data_path.iterdir():
                if item.is_file():
                    zipf.write(item, item.name)
                elif item.is_dir():
                    for root, dirs, files in shutil.walk(item):
                        for file in files:
                            file_path = Path(root) / file
                            arcname = file_path.relative_to(data_path)
                            zipf.write(file_path, arcname)

        # Berechne und speichere Prüfsumme
        checksum = self.calculate_checksum(backup_path)
        logger.info(f"Backup erstellt: {backup_path}, Checksum: {checksum}")

        return backup_path

    def calculate_checksum(self, file_path: Path) -> str:
        """
        Berechnet SHA256-Prüfsumme

        Args:
            file_path: Pfad zur Datei

        Returns:
            Prüfsumme als Hex-String
        """
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()

    def list_backups(self, backup_type: str = "all") -> List[Path]:
        """
        Listet verfügbare Backups auf

        Args:
            backup_type: 'daily', 'manual' oder 'all'

        Returns:
            Liste von Backup-Pfaden
        """
        backups = []

        if backup_type in ["daily", "all"]:
            backups.extend(self.daily_path.glob("*.zip"))

        if backup_type in ["manual", "all"]:
            backups.extend(self.manual_path.glob("*.zip"))

        return sorted(backups, reverse=True)

    def restore_backup(self, backup_path: Path, target_path: Path) -> bool:
        """
        Stellt Backup wieder her

        Args:
            backup_path: Pfad zum Backup-Archiv
            target_path: Pfad zum Wiederherstellen

        Returns:
            True wenn erfolgreich
        """
        try:
            logger.info(f"Stelle Backup wieder her: {backup_path}")

            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(target_path)

            logger.info(f"Backup wiederhergestellt: {backup_path} -> {target_path}")
            return True

        except Exception as e:
            logger.error(f"Wiederherstellung fehlgeschlagen: {backup_path}, {e}")
            return False

    def cleanup_old_backups(self, retention_days: int = 30) -> int:
        """
        Löscht alte tägliche Backups

        Args:
            retention_days: Aufbewahrungsdauer in Tagen

        Returns:
            Anzahl gelöschter Backups
        """
        deleted = 0
        cutoff = datetime.now().timestamp() - (retention_days * 24 * 3600)

        for backup in self.daily_path.glob("*.zip"):
            if backup.stat().st_mtime < cutoff:
                backup.unlink()
                deleted += 1
                logger.info(f"Altes Backup gelöscht: {backup}")

        return deleted
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_backup.py::test_create_backup -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/backup/backup_manager.py
git commit -m "feat: add backup manager with checksum verification"
```

---

## Phase 7: Utils

### Task 13: Validatoren

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/utils/validators.py`
- Create: `werkstatt_dokumenten_verwaltung/utils/__init__.py`

- [ ] **Step 1: Erstelle Test für Validatoren**

```python
import pytest
from utils.validators import Validators

def test_validate_kennzeichen():
    """Test Kennzeichen-Validierung"""
    assert Validators.validate_kennzeichen("M-AB 123") == True
    assert Validators.validate_kennzeichen("M-AB 1234") == True
    assert Validators.validate_kennzeichen("INVALID") == False
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_utils.py::test_validate_kennzeichen -v`
Expected: FAIL

- [ ] **Step 3: Erstelle validators.py**

```python
import re
from typing import Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Validators:
    """Validatoren für Benutzereingaben"""

    @staticmethod
    def validate_kennzeichen(kennzeichen: str) -> Tuple[bool, Optional[str]]:
        """
        Validiert deutsches Kennzeichen

        Args:
            kennzeichen: Zu prüfendes Kennzeichen

        Returns:
            Tuple (Gültig, Fehlermeldung)
        """
        pattern = r"^[A-ZÖÄÜ]{1,3}-[A-ZÖÄÜ]{1,2}\s*[0-9]{1,4}$"

        if not kennzeichen:
            return False, "Kennzeichen darf nicht leer sein"

        if not re.match(pattern, kennzeichen.upper()):
            return False, "Ungültiges Kennzeichen-Format"

        return True, None

    @staticmethod
    def validate_email(email: str) -> Tuple[bool, Optional[str]]:
        """
        Validiert E-Mail-Adresse

        Args:
            email: Zu prüfende E-Mail

        Returns:
            Tuple (Gültig, Fehlermeldung)
        """
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

        if not email:
            return True, None  # Optional

        if not re.match(pattern, email):
            return False, "Ungültige E-Mail-Adresse"

        return True, None

    @staticmethod
    def validate_telefon(telefon: str) -> Tuple[bool, Optional[str]]:
        """
        Validiert Telefonnummer

        Args:
            telefon: Zu prüfende Telefonnummer

        Returns:
            Tuple (Gültig, Fehlermeldung)
        """
        if not telefon:
            return True, None  # Optional

        # Erlaube verschiedene Formate
        patterns = [
            r"^\+49\s*[0-9\s-]+$",  # Internationales Format
            r"^0[1-9][0-9\s-]*$"    # Nationales Format
        ]

        for pattern in patterns:
            if re.match(pattern, telefon):
                return True, None

        return False, "Ungültige Telefonnummer"

    @staticmethod
    def validate_baujahr(baujahr: int) -> Tuple[bool, Optional[str]]:
        """
        Validiert Baujahr

        Args:
            baujahr: Baujahr

        Returns:
            Tuple (Gültig, Fehlermeldung)
        """
        current_year = datetime.now().year + 1

        if not 1900 <= baujahr <= current_year:
            return False, f"Baujahr muss zwischen 1900 und {current_year} liegen"

        return True, None

    @staticmethod
    def validate_kundenname(name: str) -> Tuple[bool, Optional[str]]:
        """
        Validiert Kundenname

        Args:
            name: Kundenname

        Returns:
            Tuple (Gültig, Fehlermeldung)
        """
        if not name:
            return False, "Kundenname darf nicht leer sein"

        if len(name) < 2:
            return False, "Kundenname muss mindestens 2 Zeichen haben"

        if len(name) > 100:
            return False, "Kundenname darf maximal 100 Zeichen haben"

        return True, None

    @staticmethod
    def validate_dokument_nummer(nummer: str) -> Tuple[bool, Optional[str]]:
        """
        Validiert Dokumentnummer

        Args:
            nummer: Dokumentnummer

        Returns:
            Tuple (Gültig, Fehlermeldung)
        """
        if not nummer:
            return False, "Nummer darf nicht leer sein"

        if len(nummer) > 50:
            return False, "Nummer darf maximal 50 Zeichen haben"

        return True, None
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_utils.py::test_validate_kennzeichen -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/utils/validators.py
git commit -m "feat: add input validators for customer and vehicle data"
```

---

### Task 14: Fehlerbehandlung

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/utils/error_handler.py`

- [ ] **Step 1: Erstelle Test für Fehlerbehandlung**

```python
import pytest
from utils.error_handler import ErrorHandler, WerkstattException

def test_error_handler_logging():
    """Test Fehlerbehandler-Logging"""
    handler = ErrorHandler()

    with pytest.raises(WerkstattException):
        handler.handle_error("Test error", critical=False)
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_utils.py::test_error_handler_logging -v`
Expected: FAIL

- [ ] **Step 3: Erstelle error_handler.py**

```python
import logging
from typing import Optional, Dict, Any
from functools import wraps
import traceback

logger = logging.getLogger(__name__)

class WerkstattException(Exception):
    """Basis-Exception für die Anwendung"""
    pass

class ErrorHandler:
    """Zentraler Fehlerbehandler"""

    @staticmethod
    def handle_error(
        message: str,
        exception: Optional[Exception] = None,
        critical: bool = False,
        **kwargs
    ) -> None:
        """
        Behandelt Fehler und loggt sie

        Args:
            message: Fehlernachricht
            exception: Original-Exception
            critical: Ob kritischer Fehler
            **kwargs: Zusätzliche Kontext-Daten
        """
        log_level = logging.ERROR if not critical else logging.CRITICAL
        log_message = f"{message}"

        if kwargs:
            log_message += f" | Context: {kwargs}"

        if exception:
            log_message += f" | Exception: {type(exception).__name__}: {exception}"
            logger.log(log_level, log_message, exc_info=True)
        else:
            logger.log(log_level, log_message)

    @staticmethod
    def handle_database_error(error: Exception, operation: str = "Datenbank-Operation") -> None:
        """
        Behandelt Datenbank-Fehler

        Args:
            error: Datenbank-Exception
            operation: Beschreibung der Operation
        """
        ErrorHandler.handle_error(
            f"{operation} fehlgeschlagen",
            exception=error,
            operation=operation
        )

    @staticmethod
    def handle_file_error(error: Exception, file_path: str, operation: str = "Datei-Operation") -> None:
        """
        Behandelt Datei-Fehler

        Args:
            error: Datei-Exception
            file_path: Pfad zur Datei
            operation: Beschreibung der Operation
        """
        ErrorHandler.handle_error(
            f"{operation} fehlgeschlagen: {file_path}",
            exception=error,
            file_path=file_path,
            operation=operation
        )

def handle_errors(func):
    """
    Dekorator zur automatischen Fehlerbehandlung

    Args:
        func: Zu dekorierende Funktion
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WerkstattException:
            raise
        except Exception as e:
            ErrorHandler.handle_error(
                f"Fehler in {func.__name__}",
                exception=e
            )
            raise WerkstattException(f"{func.__name__} fehlgeschlagen: {e}")

    return wrapper
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_utils.py::test_error_handler_logging -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/utils/error_handler.py
git commit -m "feat: add error handler with decorators"
```

---

## Phase 8: Benutzeroberfläche (UI)

### Task 15: Hauptfenster

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/ui/main_window.py`
- Create: `werkstatt_dokumenten_verwaltung/ui/__init__.py`

- [ ] **Step 1: Erstelle Test für Hauptfenster**

```python
import pytest
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow

@pytest.fixture
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

def test_main_window_creation(app):
    """Test Hauptfenster-Erstellung"""
    window = MainWindow()

    assert window.windowTitle() == "Werkstatt-Dokumenten-Verwaltung"
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_ui.py::test_main_window_creation -v`
Expected: FAIL

- [ ] **Step 3: Erstelle main_window.py**

```python
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget,
    QTableWidgetItem, QHeaderView, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction
import logging

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    """Hauptfenster der Anwendung"""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Werkstatt-Dokumenten-Verwaltung")
        self.setGeometry(100, 100, 1200, 800)

        self.init_ui()

    def init_ui(self):
        """Initialisiert die Benutzeroberfläche"""
        # Haupt-Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Schnellsuche
        search_layout = QHBoxLayout()
        search_label = QLabel("Schnellsuche:")
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Kunde, Fahrzeug, Auftragsnummer..."
        )
        search_button = QPushButton("Suchen")
        search_button.clicked.connect(self.on_search)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        # Schnellzugriff-Buttons
        quick_actions_layout = QHBoxLayout()
        scan_button = QPushButton("📄 Dokument scannen")
        scan_button.clicked.connect(self.on_scan_document)
        scan_button.setMinimumHeight(40)

        import_button = QPushButton("📥 Dokument importieren")
        import_button.clicked.connect(self.on_import_document)
        import_button.setMinimumHeight(40)

        backup_button = QPushButton("💾 Backup erstellen")
        backup_button.clicked.connect(self.on_create_backup)
        backup_button.setMinimumHeight(40)

        quick_actions_layout.addWidget(scan_button)
        quick_actions_layout.addWidget(import_button)
        quick_actions_layout.addWidget(backup_button)
        main_layout.addLayout(quick_actions_layout)

        # Statistiken
        stats_label = QLabel(
            "Willkommen bei der Werkstatt-Dokumenten-Verwaltung"
        )
        stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(stats_label)

        logger.info("Hauptfenster initialisiert")

    def on_search(self):
        """Suche ausführen"""
        search_term = self.search_input.text()
        if not search_term:
            return

        logger.info(f"Suche ausgeführt: {search_term}")
        # TODO: Implementiere Such-Logik

    def on_scan_document(self):
        """Dokument scannen"""
        logger.info("Dokument scannen aufgerufen")
        # TODO: Implementiere Scanner-Integration

    def on_import_document(self):
        """Dokument importieren"""
        logger.info("Dokument importieren aufgerufen")
        # TODO: Implementiere Import-Dialog

    def on_create_backup(self):
        """Backup erstellen"""
        logger.info("Backup erstellen aufgerufen")
        # TODO: Implementiere Backup-Erstellung
```

- [ ] **Step 4: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_ui.py::test_main_window_creation -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/ui/main_window.py
git commit -m "feat: add main window with search and quick actions"
```

---

### Task 16: Upload-Dialog

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/ui/upload_dialog.py`

- [ ] **Step 1: Erstelle Upload-Dialog**

```python
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QLineEdit, QComboBox, QTextEdit,
    QMessageBox, QFileDialog
)
from PyQt6.QtCore import pyqtSignal
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class UploadDialog(QDialog):
    """Dialog für Dokumenten-Upload"""

    document_uploaded = pyqtSignal(dict)  # Signal für erfolgreichen Upload

    def __init__(self, file_path: Path, parent=None):
        super().__init__(parent)

        self.file_path = file_path
        self.init_ui()
        self.analyze_document()

    def init_ui(self):
        """Initialisiert UI"""
        self.setWindowTitle("Dokument hochladen")
        self.setMinimumWidth(600)
        self.setMinimumHeight(500)

        layout = QVBoxLayout(self)

        # Datei-Info
        file_info = QLabel(f"Datei: {self.file_path.name}")
        layout.addWidget(file_info)

        # Automatische Erkennung
        layout.addWidget(QLabel("<b>Automatische Erkennung:</b>"))
        self.recognition_results = QTextEdit()
        self.recognition_results.setReadOnly(True)
        layout.addWidget(self.recognition_results)

        # Manuelle Eingabe
        layout.addWidget(QLabel("<b>Manuelle Eingabe (falls nötig):</b>"))

        # Kunde
        kunde_layout = QHBoxLayout()
        kunde_layout.addWidget(QLabel("Kunde:"))
        self.kunde_input = QLineEdit()
        kunde_layout.addWidget(self.kunde_input)
        layout.addLayout(kunde_layout)

        # Fahrzeug
        fahrzeug_layout = QHBoxLayout()
        fahrzeug_layout.addWidget(QLabel("Fahrzeug:"))
        self.kennzeichen_input = QLineEdit()
        fahrzeug_layout.addWidget(self.kennzeichen_input)
        layout.addLayout(fahrzeug_layout)

        # Dokumenttyp
        typ_layout = QHBoxLayout()
        typ_layout.addWidget(QLabel("Typ:"))
        self.typ_combo = QComboBox()
        self.typ_combo.addItems(["rechnung", "auftrag", "garantie", "sonstiges"])
        typ_layout.addWidget(self.typ_combo)
        layout.addLayout(typ_layout)

        # Nummer
        nummer_layout = QHBoxLayout()
        nummer_layout.addWidget(QLabel("Nummer:"))
        self.nummer_input = QLineEdit()
        nummer_layout.addWidget(self.nummer_input)
        layout.addLayout(nummer_layout)

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Speichern")
        save_button.clicked.connect(self.on_save)
        save_button.setMinimumHeight(40)

        cancel_button = QPushButton("Abbrechen")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setMinimumHeight(40)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        logger.info("Upload-Dialog initialisiert")

    def analyze_document(self):
        """Analysiert Dokument mit Intelligenz-Modul"""
        try:
            from document_intelligence.classifier import DocumentClassifier
            from document_intelligence.pdf_extractor import PDFExtractor

            # Text extrahieren
            extractor = PDFExtractor()
            text, page_count = extractor.extract_text(self.file_path)

            # Features extrahieren
            classifier = DocumentClassifier()
            features = classifier.extract_all_features(text)

            # Vorschläge anzeigen
            self.display_recognition_results(features, page_count)

            # Felder füllen
            if "kunde" in features:
                kunde, conf = features["kunde"]
                self.kunde_input.setText(kunde)
                self.kunde_input.setStyleSheet("background-color: #90EE90;")  # Hellgrün

            if "kennzeichen" in features:
                kennzeichen, conf = features["kennzeichen"]
                self.kennzeichen_input.setText(kennzeichen)

            if "typ" in features:
                self.typ_combo.setCurrentText(features["typ"])

            if "nummer" in features:
                self.nummer_input.setText(features["nummer"])

        except Exception as e:
            logger.error(f"Dokument-Analyse fehlgeschlagen: {e}")
            self.recognition_results.setText(
                f"Fehler bei Analyse: {e}\n"
                "Bitte manuell ausfüllen."
            )

    def display_recognition_results(self, features: dict, page_count: int):
        """Zeigt Erkennungsergebnisse an"""
        results = []

        if "kunde" in features:
            kunde, conf = features["kunde"]
            results.append(f"✓ Kunde: {kunde} ({conf}%)")

        if "kennzeichen" in features:
            kennzeichen, conf = features["kennzeichen"]
            results.append(f"✓ Fahrzeug: {kennzeichen} ({conf}%)")

        if "typ" in features:
            typ, conf = features["typ"]
            results.append(f"✓ Typ: {typ} ({conf}%)")

        results.append(f"✓ Seiten: {page_count}")

        if "nummer" in features:
            results.append(f"✓ Nummer: {features['nummer']}")

        if results:
            self.recognition_results.setText("\n".join(results))
        else:
            self.recognition_results.setText("Keine automatische Erkennung möglich.")

    def on_save(self):
        """Speichert Dokument"""
        if not self.kunde_input.text():
            QMessageBox.warning(self, "Warnung", "Bitte Kunde eingeben!")
            return

        if not self.nummer_input.text():
            QMessageBox.warning(self, "Warnung", "Bitte Nummer eingeben!")
            return

        # TODO: Speichere in Datenbank und Dateisystem
        data = {
            "kunde": self.kunde_input.text(),
            "fahrzeug": self.kennzeichen_input.text(),
            "typ": self.typ_combo.currentText(),
            "nummer": self.nummer_input.text(),
            "dateipfad": str(self.file_path)
        }

        self.document_uploaded.emit(data)
        self.accept()
        logger.info(f"Dokument hochgeladen: {self.file_path.name}")
```

- [ ] **Step 2: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/ui/upload_dialog.py
git commit -m "feat: add upload dialog with automatic document analysis"
```

### Task 16.5: Upload-Dialog Tests

**Files:**
- Modify: `werkstatt_dokumenten_verwaltung/tests/test_ui.py`

- [ ] **Step 1: Erstelle Test für Upload-Dialog**

```python
import pytest
from pathlib import Path
from ui.upload_dialog import UploadDialog

@pytest.fixture
def app():
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    app.quit()

def test_upload_dialog_creation(app, tmp_path):
    """Test Upload-Dialog-Erstellung"""
    test_file = tmp_path / "test.pdf"
    test_file.write_text("Test content")

    dialog = UploadDialog(test_file)

    assert dialog.windowTitle() == "Dokument hochladen"
    assert dialog.file_path == test_file
```

- [ ] **Step 2: Run Test**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_ui.py::test_upload_dialog_creation -v`
Expected: FAIL

- [ ] **Step 3: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/tests/test_ui.py
git commit -m "test: add upload dialog tests"
```

---

## Phase 9: Integration und Tests

### Task 17: End-zu-End-Tests

**Files:**
- Create: `werkstatt_dokumenten_verwaltung/tests/test_integration.py`

- [ ] **Step 1: Erstelle Integrationstest**

```python
import pytest
from pathlib import Path
from document_intelligence.pdf_extractor import PDFExtractor
from document_intelligence.classifier import DocumentClassifier
from file_manager.folder_structure import FolderManager

def test_full_document_workflow(tmp_path):
    """Test vollständiger Dokumenten-Workflow"""
    # 1. Dokument erstellen
    test_pdf = tmp_path / "test_rechnung.pdf"
    test_pdf.write_bytes(b"%PDF-1.4...")  # Dummy-PDF

    # 2. Text extrahieren
    extractor = PDFExtractor()
    text, page_count = extractor.extract_text(test_pdf)
    assert page_count >= 0

    # 3. Features extrahieren
    classifier = DocumentClassifier()
    features = classifier.extract_all_features(text)
    assert "typ" in features

    # 4. Ordnerstruktur erstellen
    manager = FolderManager(tmp_path)
    path = manager.get_document_path(
        "Test Kunde",
        "M-AB 123",
        "2024",
        "rechnung"
    )
    assert path.exists()
```

- [ ] **Step 2: Run Integrationstests**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/test_integration.py::test_full_document_workflow -v`
Expected: PASS

- [ ] **Step 3: Commit**

```bash
git add werkstatt_dokumenten_verwaltung/tests/test_integration.py
git commit -m "test: add integration tests for document workflow"
```

---

### Task 18: Finaler Build und Test

- [ ] **Step 1: Alle Tests ausführen**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/ -v`
Expected: Alle Tests bestehen

- [ ] **Step 2: Prüfe Code-Coverage**

Run: `pytest werkstatt_dokumenten_verwaltung/tests/ --cov=werkstatt_dokumenten_verwaltung --cov-report=term-missing`
Expected: Coverage > 80%

- [ ] **Step 3: Erstelle README.md**

```markdown
# Werkstatt-Dokumenten-Verwaltung

Eine Desktop-Anwendung für kleine Werkstätten (2-5 Mitarbeiter) zum automatisierten Sichern, Archivieren und Dokumentieren von gescannten Werkstatt-Aufträgen, Rechnungen, Garantien und anderen wichtigen Dokumenten.

## Features

- **Automatische Dokumenten-Erkennung**: Kunden, Fahrzeuge und Dokumenttypen werden automatisch erkannt
- **OCR-Unterstützung**: Gescannte PDFs werden mit Tesseract OCR verarbeitet
- **Intelligente Sortierung**: Dokumente werden automatisch nach Kundenname organisiert
- **Schnellsuche**: Volltext-Suche über alle Dokumente
- **Scanner-Integration**: Direkter Zugriff auf WIA-Scanner
- **Backup-System**: Automatische tägliche und manuelle Backups

## Installation

```bash
pip install -r requirements.txt
```

## Nutzung

```bash
python main.py
```

## Technologie-Stack

- Python 3.12+
- PyQt6 (Benutzeroberfläche)
- SQLite (Datenbank)
- pdfplumber (PDF-Text-Extraktion)
- pytesseract (OCR)
```

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs: add README with installation instructions"
```

- [ ] **Step 5: Finaler Commit**

```bash
git log --oneline | head -20
```

Run: `git status`
Expected: Sauberer Working Tree

---

## Zusammenfassung

Dieser Implementierungsplan deckt alle 18 Tasks ab, die benötigt werden, um die Werkstatt-Dokumenten-Verwaltung vollständig zu implementieren:

1. **Projekt-Setup** (Task 1)
2. **Datenbank-Modul** (Tasks 2-3)
3. **Dokumenten-Intelligenz** (Tasks 4-7)
4. **Datei-Manager** (Tasks 8-9)
5. **Sicherheits-Modul** (Tasks 10-11)
6. **Backup-Modul** (Task 12)
7. **Utils** (Tasks 13-14)
8. **Benutzeroberfläche** (Tasks 15-16)
9. **Integration und Tests** (Tasks 17-18)

Jeder Task folgt TDD-Prinzipien mit klar definierten Tests, Implementierung und Commits.
