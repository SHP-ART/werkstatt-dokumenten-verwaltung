# Werkstatt-Dokumenten-Verwaltung - Design-Dokument

**Datum:** 2026-03-20
**Status:** Überarbeitung 1 (Review-Fehler behoben)
**Version:** 1.1

## Zusammenfassung

Eine Desktop-Anwendung für kleine Werkstätten (2-5 Mitarbeiter) zum automatisierten Sichern, Archivieren und Dokumentieren von gescannten Werkstatt-Aufträgen, Rechnungen, Garantien und anderen wichtigen Dokumenten. Das System erkennt automatisch Kunden, Fahrzeuge und Dokumenttypen und organisiert Dokumente in einer klaren Ordnerstruktur.

## Design-Entscheidungen und Risiko-Mitigation

**Entscheidung: SQLite mit WAL-Mode**
- Risiko: SQLite auf Netzwerkfreigabe hat Limitationen bei gleichzeitigen Schreibzugriffen
- Mitigation: WAL-Mode (Write-Ahead Logging) + Warteschlange + Retry-Logic
- Alternativ bei Problemen: Migration zu Client-Server-Architektur (Phase 2)

**Performance-Ziele:**
- OCR-Prozessierung: < 10 Sekunden pro Seite
- Suchdauer: < 2 Sekunden bei 10.000 Dokumenten
- Startzeit: < 5 Sekunden
- Gleichzeitige Benutzer: Bis zu 5 ohne nennenswerte Performance-Einbußen

## Anforderungen

### Zielgruppe
- Kleine Werkstatt mit 2-5 Mitarbeitern
- Besitzer mit Vollzugriff, Mitarbeiter mit eingeschränktem Zugriff

### Funktionsanforderungen
- Sichern und Archivieren von gescannten Dokumenten
- Automatische Erkennung von Kunden, Fahrzeugen und Dokumenttypen
- Sortierung von Aufträgen nach Kunden
- Organisierte Speicherung in Ordnerstruktur nach Kundenname
- Schnelle Suche nach Dokumenten
- Scanner-Integration
- Drag & Drop Import
- Automatische und manuelle Backups

### Nicht-funktionale Anforderungen
- Desktop-Anwendung für Windows
- Moderne und visuell ansprechende UI
- Gemeinsamer Zugriff über lokale Netzwerkfreigabe
- Ausfallsichere Backup-Lösung

## Systemarchitektur

### Hauptkomponenten

1. **Hauptanwendung (Python + PyQt6)**
   - Desktop-App mit moderner UI
   - Verbindet sich zur SQLite-Datenbank
   - Verwaltet Dokumente im Dateisystem

2. **Datenbank-Modul**
   - SQLite-Datenbank auf Netzwerkfreigabe
   - Speichert Metadaten, Such-Index, Benutzereinstellungen
   - Speichert extrahierte Schlüsselwörter und Klassifizierungsergebnisse
   - SQLite-Transaktionen für gleichzeitige Zugriffe

3. **Dokumenten-Intelligenz-Modul**
   - PDF-Text-Extraktion (pdfplumber)
   - OCR für gescannte PDFs (Tesseract/pytesseract)
   - Schlüsselwort-Erkennung: Kundenname, Auftragsnummer, Fahrzeugkennzeichen, Datum, Betrag
   - Dokument-Klassifizierung: Auftrag, Rechnung, Garantie, sonstiges
   - Auto-Vorschlag für Kunde/Fahrzeug basierend auf Inhalt

4. **Datei-Manager**
   - Verwaltet PDFs/Bilder auf der Netzwerkfreigabe
   - Struktur: `/Kunden/[KundenName]/Fahrzeuge/[Kennzeichen]/[Jahr]/[Dokumenttyp]_[Nummer].pdf`
   - Automatische Ordnererstellung basierend auf erkanntem Kundenamen

5. **Backup-Modul**
   - Tägliches automatisches Backup (Zeit konfigurierbar)
   - Manuelle Backups vor wichtigen Änderungen
   - Speichert Datenbank-Datei und Dokument-Verzeichnis

## Datenbankstruktur

### Tabellen

**benutzer**
- id (PK)
- benutzername
- passwort_hash
- rolle (besitzer/mitarbeiter)
- erstellt_am
- zuletzt_geloggt

**kunden**
- id (PK)
- name
- adresse
- telefon
- email
- erstellt_am

**fahrzeuge**
- id (PK)
- kunden_id (FK)
- kennzeichen
- marke
- modell
- baujahr
- erstellt_am

**dokumente**
- id (PK)
- kunden_id (FK, NULL wenn nicht zugeordnet)
- fahrzeug_id (FK, NULL)
- dokument_typ (auftrag/rechnung/garantie/sonstiges)
- nummer (fortlaufend pro Kunde/Jahr)
- datum
- betrag
- dateipfad
- dateiname
- seiten_anzahl
- status (automatisch_erkannt/manuell_bestätigt)
- erstellt_am
- aktualisiert_am

**schluesselwoerter**
- id (PK)
- dokument_id (FK)
- wort
- position
- konfidenz_score (0-100)

**einstellungen**
- id (PK)
- benutzer_id (FK)
- schluessel
- wert
- aktualisiert_am

**protokoll**
- id (PK)
- benutzer_id (FK)
- aktion
- details
- zeitpunkt

### Indizes und Volltext-Suche

**Performance-Indizes:**
```sql
CREATE INDEX idx_dokumente_kunden_id ON dokumente(kunden_id);
CREATE INDEX idx_dokumente_fahrzeug_id ON dokumente(fahrzeug_id);
CREATE INDEX idx_dokumente_datum ON dokumente(datum);
CREATE INDEX idx_dokumente_typ ON dokumente(dokument_typ);
CREATE INDEX idx_fahrzeuge_kunden_id ON fahrzeuge(kunden_id);
```

**Volltext-Suche (FTS5):**
```sql
CREATE VIRTUAL TABLE dokumente_fts USING fts5(
    kundenname,
    fahrzeugkennzeichen,
    dokumentinhalt,
    content=dokumente,
    content_rowid=id
);
```

Suchfelder:
- Kunde (vollständiger Name, Suche nach Wortteilen)
- Fahrzeug (Kennzeichen)
- Auftragsnummer/Rechnungsnummer (exakt)
- Datum (Bereichssuche)
- Betrag (Bereichssuche)
- Volltext im Dokumenteninhalt

## Benutzeroberfläche

### Hauptbildschirme

1. **Hauptfenster (Dashboard)**
   - Schnellsuche (Fahrzeug, Kunde, Auftragsnummer)
   - Letzte Dokumente
   - Schnellzugriff-Buttons
   - Statistiken

2. **Dokumenten-Upload-Bildschirm**
   - Drag & Drop Zone
   - Scanner-Button
   - Vorschau des Dokuments
   - Automatische Erkennung-Anzeige
   - Manuelles Override möglich

3. **Dokumenten-Übersicht**
   - Filterleiste
   - Tabelle mit Ergebnissen
   - Kontextmenü

4. **Kunde/Fahrzeug-Verwaltung**
   - Kunden-Anlegen/Bearbeiten
   - Fahrzeuge zuordnen
   - Kundenübersicht

5. **Backup-Verwaltung**
   - Backup-Status
   - Manuelles Backup
   - Backup-Historie

## Dokumenten-Intelligenz

### PDF-Text-Extraktion
- Bibliothek: pdfplumber
- Extrahiert Text aus strukturierten PDFs
- Erkennt Tabellen und Layout
- **PDF-Seiten-Zählung**: `pdf_reader.pages` für `seiten_anzahl`-Feld

### OCR
- Bibliothek: pytesseract (Tesseract OCR)
- Sprachen: Deutsch (deu) + Englisch (eng)
- Qualitätsschwellen: Konfidenz > 60%
- **Asynchrone Verarbeitung**: OCR im Hintergrund, Status-Indikator
- **Asynchrone Queue**: Mehrere OCR-Jobs parallel möglich

### Mustererkennung (Phase 1: Regex-basiert)
- **Kunden**: Regex-Pattern für typische Formate
  - `"Kunde: (.*)"` `"Firma: (.*)"` `"Name: (.*)"`
  - Training: Besitzer kann Kundennamen manuell markieren, System lernt Muster
- **Fahrzeuge**: Kennzeichen-Regex `^[A-Z]{1,3}-[A-Z]{1,2} [0-9]{1,4}$`
  - Verknüpfung mit bekannten Fahrzeugen in Datenbank
- **Dokument-Typ**: Schlüsselwort-basiert
  - Aufträge: "Auftrag", "Arbeitsauftrag"
  - Rechnungen: "Rechnung", "Invoice", "Betrag"
  - Garantien: "Garantie", "Gewährleistung"
- **Phase 2**: Bayes-Klassifikator für verbesserte Genauigkeit (optional)

### OCR-Training und Lernen
- **Initial-Training**: System lernt aus den ersten 50 manuell zugeordneten Dokumenten
- **Trainingsdatenbank**: Speichert erkannte Muster und Konfidenz-Scores
- **Besitzer-Interface**: "Muster markieren" zur Verbesserung
- **Kontinuierliches Lernen**: Jede manuelle Bestätigung verbessert das System

### Konfidenz-System
- <50%: Manuelle Überprüfung erforderlich, keine Vorschläge
- 50-80%: Vorschlag anzeigen, Bestätigung erfordern
- >80%: Automatische Übernahme mit Korrektur-Option

## Dateisystem-Struktur

```
/Werkstatt-Dokumente/
├── Kunden/
│   ├── [KundenName]/
│   │   ├── Fahrzeuge/
│   │   │   ├── [Kennzeichen]/
│   │   │   │   ├── [Jahr]/
│   │   │   │   │   ├── Rechnungen/
│   │   │   │   │   │   ├── Rechnung_2024-03-15_RE12345.pdf
│   │   │   │   │   ├── Aufträge/
│   │   │   │   │   │   ├── Auftrag_2024-03-15_AR12345.pdf
│   │   │   │   │   └── Garantien/
│   │   │   │   │       ├── Garantie_2024-03-15_GA12345.pdf
│   │   │   │   └── ...
│   │   └── ...
│   └── ...
├── Nicht_zugeordnet/
│   ├── [Dokumente ohne erkennbaren Kunden]/
│   └── ...
└── Backups/
    ├── Täglich/
    │   ├── backup_2024-03-15.zip
    │   └── ...
    └── Manuell/
        ├── backup_2024-03-15_14-30-vor_Änderung.zip
        └── ...
```

### Benennungskonventionen
- Kundenordner: Exakter Name (Sonderzeichen ersetzt: ä→ae, ö→oe, ü→ue, ß→ss, /→_)
- Fahrzeugordner: Kennzeichen (ohne Leerzeichen, z.B. "M-AB123")
- Dateiname: `[Dokumenttyp]_[Jahr-MM-TT]_[Nummer].pdf`
- Beispiel: `Rechnung_2024-03-15_RE12345.pdf`

### Ordnererstellung
- Automatisch beim ersten Dokument für Kunde/Fahrzeug/Jahr/Dokumenttyp
- Prüfung auf Duplikate vor Speicherung
- Verschieben bei manueller Kunden/Fahrzeug-Zuordnung

## Backup-System

### Tägliche automatische Backups
- Zeitpunkt: Konfigurierbar (Standard: Mitternacht)
- Speicherort: `/Backups/Täglich/`
- Inhalt: Vollständige SQLite-Datenbank (`werkstatt.db`) + `/Kunden/` Ordner
- Format: `backup_YYYY-MM-DD.zip`
- Aufbewahrung: 30 Tage (ältere Backups werden automatisch gelöscht)
- Prüfsummen-Verifizierung nach jedem Backup
- Statusanzeige: "Letztes Backup: [Datum] - Erfolgreich"

### Manuelle Backups
- Auslösbar über Hauptmenü oder F10
- Speicherort: `/Backups/Manuell/`
- Format: `backup_YYYY-MM-DD_HH-MM-Uhrzeit_Beschreibung.zip`
- Beschreibung kann vom Benutzer eingegeben werden
- Aufbewahrung: Unbegrenzt (manuelle Löschung möglich)
- Fortschrittsanzeige bei großen Backups

### Restore-Funktion
- Wählt Backup aus Liste
- Zeigt Vorschau: Datum, Größe, Anzahl Dokumente
- Bestätigung erforderlich: "Dies überschreibt alle aktuellen Daten. Fortfahren?"
- Automatisches Backup des aktuellen Zustands vor Restore
- Nach Restore: Anwendung neustart erforderlich
- Rollback möglich (Restore des vorherigen Backups)

### Backup-Fehlerbehandlung
- Speicherplatz voll: Warnung mit Möglichkeit, alte Backups zu löschen
- Netzwerkfehler: Wiederholungsversuche mit Benachrichtigung
- Beschädigte Backups: Warnung vor Restore, Möglichkeit zur Reparatur

## Error-Handling und Fehlertoleranz

### Fehlerkategorien und Behandlungsstrategien

**Netzwerkfehler:**
- Exponential Backoff bei temporären Fehlern (1s, 2s, 4s, 8s, 16s)
- Benachrichtigung: "Verbindung zum Netzwerk verloren. Wiederhole..."
- Maximal 5 Wiederholungsversuche, danach Benutzer benachrichtigen

**Datenbank-Locks:**
- SQLite WAL-Mode aktivieren
- Timeout: 30 Sekunden
- Retry-Logic mit exponentiellem Backoff
- Queue-System für gleichzeitige Schreibvorgänge

**OCR-Fehler:**
- OCR fehlgeschlagen: Manuelles Ausfüllen der Formulare
- Konfidenz zu niedrig: Benutzer benachrichtigen, manuelle Bestätigung
- Status-Indikator: "OCR läuft..." mit Fortschrittsbalken

**Scanner-Probleme:**
- Scanner nicht verfügbar: Fallback zu Drag & Drop
- Scanner-Ausfall: Fehlermeldung mit Anleitung zum Neustart
- Qualität zu schlecht: Warnung, erneuter Scan möglich

**Validierungsfehler:**
- Eingabefelder: Rot markieren, Fokus auf fehlerhaftes Feld
- Beschreibung: "Ungültiges Format. Erwartet: [Beschreibung]"
- Speichern erst nach Korrektur aller Fehler möglich

### Protokollierung
- Alle Fehler werden in Protokoll-Tabelle geschrieben
- Technik-Fehler: Stacktrace für Fehlersuche
- Benutzer-Fehler: Kurze Beschreibung ohne Stacktrace
- Export von Protokollen möglich

### Wiederherstellung
- Bei schweren Fehlern: "Letztes erfolgreiches Backup wiederherstellen?"
- Automatisches Backup vor kritischen Aktionen
- Rollback bei fehlgeschlagenen Transaktionen

## Validierungs-Logik

### Pflichtfelder und Validierungen

**Kunden:**
- Name: Pflichtfeld, min 2 Zeichen, max 100 Zeichen
- Telefon: Optional, Format `+49 [0-9]{3,}` oder `0[1-9][0-9]*`
- E-Mail: Optional, Standard-E-Mail-Regex
- Adresse: Optional, max 200 Zeichen

**Fahrzeuge:**
- Kunden-ID: Pflichtfeld, muss existieren
- Kennzeichen: Pflichtfeld, Regex `^[A-Z]{1,3}-[A-Z]{1,2} [0-9]{1,4}$`
- Marke: Optional, max 50 Zeichen
- Modell: Optional, max 50 Zeichen
- Baujahr: Optional, Bereich 1900-aktuelles Jahr+1

**Dokumente:**
- Kunden-ID: Optional (für "Nicht zugeordnet")
- Fahrzeug-ID: Optional
- Dokument-Typ: Pflichtfeld (auftrag/rechnung/garantie/sonstiges)
- Nummer: Pflichtfeld, max 50 Zeichen, alphanumerisch
- Datum: Pflichtfeld, kein zukünftiges Datum
- Betrag: Optional, Dezimalzahl, max 10 Stellen

### Benutzeroberfläche-Validierung
- Echtzeit-Validierung bei Eingabe
- Visuelles Feedback (rot für Fehler, grün für gültig)
- Submit-Button deaktiviert bei unvollständigen Formularen
- Tooltip mit Fehlerbeschreibung bei Hover

## Sicherheitskonzept

### Benutzerrollen
- **Besitzer**: Vollzugriff auf alle Funktionen
- **Mitarbeiter**: Eingeschränkter Zugriff

### Berechtigungs-Matrix

| Funktion | Besitzer | Mitarbeiter |
|----------|----------|-------------|
| Dokumente hochladen | ✓ | ✓ |
| Dokumente löschen | ✓ | ✗ |
| Dokument-Metadaten bearbeiten | ✓ | ✓ |
| Dokumente verschieben | ✓ | ✗ |
| Kunden anlegen/bearbeiten | ✓ | ✗ |
| Fahrzeuge zuordnen | ✓ | ✓ |
| Backup erstellen | ✓ | ✗ |
| Backup restore | ✓ | ✗ |
| Benutzer verwalten | ✓ | ✗ |
| Einstellungen ändern | ✓ | ✗ |
| Protokoll anzeigen | ✓ | ✗ |
| OCR-Training | ✓ | ✗ |

### Authentifizierung
- Benutzername + Passwort bei Programmstart
- Passwörter gehasht mit bcrypt
- Sitzung bis zum Programmende
- Automatischer Logout bei 30 Minuten Inaktivität (konfigurierbar)

### Audit-Trail
- Alle wichtigen Aktionen werden protokolliert
- Login, Logout, Upload, Bearbeitung, Löschung
- Protokoll kann von Besitzer eingesehen werden
- Export von Protokollen möglich

## Scanner-Integration

### Scanner-Auswahl
- Automatische Erkennung verfügbarer Scanner (WIA-Interface)
- Dropdown-Menü bei mehreren Scannern
- Standard-Scanner speichern (in `einstellungen`-Tabelle)
- Scanner-Konfiguration pro Benutzer möglich

### Scan-Einstellungen
- Auflösung: 150/300/600 DPI (Standard: 300 DPI)
- Farbmodus: Schwarz-Weiß, Graustufen, Farbe (Standard: Graustufen)
- Dateiformat: PDF (Standard), optional JPG/TIFF
- Einseitig oder doppelseitig (bei Scanner-Unterstützung)
- Mehrere Seiten zu einem PDF zusammenfassen
- Scann-Einstellungen werden pro Benutzer gespeichert

### Scan-Ablauf
1. Benutzer klickt "Dokument scannen"
2. WIA-Scanner-Interface öffnet sich
3. Benutzer platziert Dokument, bestätigt Scan
4. Vorschau des gescannten Bildes wird angezeigt
5. Nach jedem Scan: "Weitere Seite scannen?" Ja/Nein
6. Bei "Nein": Alle Seiten zu PDF zusammenfassen
7. Direkt Upload zum Upload-Bildschirm mit OCR-Analyse

### Scanner-Fehlerbehandlung
- Scanner nicht verfügbar: Fehlermeldung mit Fallback zu Drag & Drop
- Scanner-Ausfall: "Scanner reagiert nicht. Bitte prüfen Sie die Verbindung."
- Qualitätsprobleme: Warnung "Scanqualität ist schlecht. Erneut scannen?"
- Scan abgebrochen: Rückkehr zum Upload-Bildschirm ohne Speicherung

### Alternative Eingabe: Drag & Drop
- Unterstützt PDF- und Bilddateien
- Mehrere Dateien gleichzeitig möglich
- Automatische Erkennung wie bei gescannten Dokumenten
- Dateien werden temporär gespeichert, bei Abbruch gelöscht

## Technologien und Bibliotheken

### Kern
- Python 3.12+
- PyQt6 (Benutzeroberfläche)
- sqlite3 (Datenbank, WAL-Mode aktiviert)

### Dokumentenverarbeitung
- pdfplumber (PDF-Text-Extraktion, Seiten-Zählung)
- pytesseract (OCR)
- Pillow (Bildverarbeitung)
- pypdf2 (PDF-Manipulation, optional)

### Asynchrone Verarbeitung
- asyncio (für parallele OCR-Verarbeitung)
- threading (Queue-System für gleichzeitige Zugriffe)

### Scanner-Integration
- pywin32 (WIA-Scanner, Windows-spezifisch)

### Backup
- zipfile (ZIP-Archive)
- shutil (Dateioperationen)
- hashlib (Prüfsummen-Verifizierung)

### Sicherheit
- bcrypt (Passwort-Hashing)
- hashlib (Datenintegrität)

### Netzwerk und Concurrency
- filelock (File-Locking für SQLite auf Netzwerk)
- concurrent.futures (Thread-Pool für parallele Aufgaben)

### Verpackung
- PyInstaller (.exe-Erstellung)
- nuitka (Alternative zu PyInstaller, besser für Performance)

### SQLite-Konfiguration
- WAL-Mode aktiviert: `PRAGMA journal_mode=WAL`
- Timeout: 30 Sekunden
- Synchro-Mode: NORMAL (Balance zwischen Performance und Sicherheit)

## Nächste Schritte

Design überarbeitet basierend auf Spec-Review-Fehlerbehebung:

**Behobene Probleme:**
- SQLite-WAL-Mode für gleichzeitige Zugriffe spezifiziert
- Umfassendes Error-Handling hinzugefügt
- Dateisystem-Struktur konsistent gemacht
- OCR-Training und Lernen spezifiziert
- Suchfunktionalität mit FTS5 und Indizes detailliert
- PDF-Seiten-Erkennung hinzugefügt
- Validierungs-Logik definiert
- Performance-Anforderungen spezifiziert
- Audit-Trail verpflichtend gemacht
- Scanner-Fehlerbehandlung spezifiziert

**Nächster Schritt:** Zweiter Spec-Review, dann Benutzer-Review, danach Implementierungsplan mit `writing-plans` Skill.
