# Werkstatt-Dokumenten-Verwaltung

Eine Desktop-Anwendung für kleine Werkstätten (2-5 Mitarbeiter) zum automatisierten Sichern, Archivieren und Dokumentieren von gescannten Werkstatt-Aufträgen, Rechnungen, Garantien und anderen wichtigen Dokumenten.

## Features

- **Automatische Dokumenten-Erkennung**: Kunden, Fahrzeuge und Dokumenttypen werden automatisch erkannt
- **OCR-Unterstützung**: Gescannte PDFs werden mit Tesseract OCR verarbeitet
- **Intelligente Sortierung**: Dokumente werden automatisch nach Kundenname organisiert
- **Schnellsuche**: Volltext-Suche über alle Dokumente
- **Scanner-Integration**: Direkter Zugriff auf WIA-Scanner
- **Backup-System**: Automatische tägliche und manuelle Backups
- **Benutzerrollen**: Besitzer mit Vollzugriff, Mitarbeiter mit eingeschränktem Zugriff

## Installation

### Voraussetzungen

- Python 3.12+
- Windows-Betriebssystem
- Tesseract OCR (für OCR-Funktionalität)
- Scanner mit WIA-Unterstützung

### Installation

```bash
# 1. Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate

# 2. Abhängigkeiten installieren
pip install -r requirements.txt

# 3. Anwendung starten
python werkstatt_dokumenten_verwaltung/main.py
```

## Projektstruktur

```
werkstatt_dokumenten_verwaltung/
├── main.py                           # Einstiegspunkt
├── config.py                         # Konfiguration
├── requirements.txt                   # Abhängigkeiten
├── database/
│   ├── models.py                      # SQLAlchemy-Modelle
│   └── database.py                    # Datenbank-Verbindung
├── document_intelligence/
│   ├── pdf_extractor.py               # PDF-Text-Extraktion
│   ├── ocr_engine.py                 # OCR-Engine
│   ├── pattern_recognizer.py          # Mustererkennung
│   └── classifier.py                  # Dokument-Klassifizierung
├── file_manager/
│   ├── file_operations.py             # Datei-Operationen
│   └── folder_structure.py           # Ordnerstruktur
├── backup/
│   └── backup_manager.py             # Backup-Verwaltung
├── ui/
│   ├── main_window.py                # Hauptfenster
│   └── upload_dialog.py              # Upload-Dialog
├── security/
│   ├── auth.py                      # Authentifizierung
│   └── permissions.py               # Berechtigungen
└── utils/
    ├── validators.py                # Validatoren
    ├── error_handler.py             # Fehlerbehandlung
    └── logger.py                   # Logging
```

## Nutzung

### Start der Anwendung

```bash
cd werkstatt_dokumenten_verwaltung
python main.py
```

### Benutzerrollen

- **Besitzer**: Vollzugriff auf alle Funktionen
  - Dokumente hochladen, löschen, bearbeiten
  - Kunden anlegen und bearbeiten
  - Backups erstellen und wiederherstellen
  - Benutzer verwalten
  - Einstellungen ändern

- **Mitarbeiter**: Eingeschränkter Zugriff
  - Dokumente hochladen und bearbeiten
  - Fahrzeuge zuordnen

### Dokumenten-Workflow

1. **Dokument importieren**
   - Drag & Drop PDF/Bild-Datei
   - Oder scannen mit Scanner

2. **Automatische Erkennung**
   - System erkennt Kundenname, Fahrzeug, Dokumenttyp
   - Vorschläge werden angezeigt

3. **Manuelle Anpassung**
   - Vorschläge können korrigiert werden
   - Neue Informationen hinzugefügt

4. **Speichern**
   - Dokument wird in Datenbank gespeichert
   - Automatische Sortierung in Ordnerstruktur

## Entwicklungsstatus

### Implementiert

- ✅ Projektstruktur
- ✅ Datenbank-Modelle (Benutzer, Kunde, Fahrzeug, Dokument, etc.)
- ✅ Datenbank-Manager
- ✅ Grundlegende Konfiguration

### In Arbeit

Die meisten Komponenten sind noch in Implementierung. Für den vollständigen Funktionsumfang siehe die Dokumentation:

- [Dokument-Dokument](docs/superpowers/specs/2026-03-20-werkstatt-dokumenten-verwaltung-design.md)
- [Implementierungsplan](docs/superpowers/plans/2026-03-20-werkstatt-dokumenten-verwaltung.md)

## Technologie-Stack

- **Python 3.12+** - Hauptprogrammiersprache
- **PyQt6** - Moderne Desktop-Benutzeroberfläche
- **SQLite (WAL-Mode)** - Datenbank mit Write-Ahead Logging
- **pdfplumber** - PDF-Text-Extraktion
- **pytesseract** - OCR für gescannte Dokumente
- **Pillow** - Bildverarbeitung
- **bcrypt** - Sicheres Passwort-Hashing
- **asyncio** - Asynchrone Verarbeitung

## Dateisystem-Struktur

```
/Werkstatt-Dokumente/
├── Kunden/
│   ├── [KundenName]/
│   │   ├── Fahrzeuge/
│   │   │   ├── [Kennzeichen]/
│   │   │   │   ├── [Jahr]/
│   │   │   │   │   ├── Rechnungen/
│   │   │   │   │   ├── Aufträge/
│   │   │   │   │   └── Garantien/
├── Nicht_zugeordnet/
└── Backups/
    ├── Täglich/
    └── Manuell/
```

## Lizenz

TODO: Lizenz noch nicht festgelegt

## Mitwirkende

Entwickelt mit Unterstützung von Claude (Anthropic)

## Dokumentation

Ausführliche Dokumentation siehe:
- [Design-Dokument](docs/superpowers/specs/2026-03-20-werkstatt-dokumenten-verwaltung-design.md)
- [Implementierungsplan](docs/superpowers/plans/2026-03-20-werkstatt-dokumenten-verwaltung.md)
