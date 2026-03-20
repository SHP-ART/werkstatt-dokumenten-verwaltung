# Werkstatt-Dokumenten-Verwaltung - Design-Dokument

**Datum:** 2026-03-20
**Status:** Design genehmigt

## Zusammenfassung

Eine Desktop-Anwendung für kleine Werkstätten (2-5 Mitarbeiter) zum automatisierten Sichern, Archivieren und Dokumentieren von gescannten Werkstatt-Aufträgen, Rechnungen, Garantien und anderen wichtigen Dokumenten. Das System erkennt automatisch Kunden, Fahrzeuge und Dokumenttypen und organisiert Dokumente in einer klaren Ordnerstruktur.

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
- nummer
- datum
- betrag
- dateipfad
- dateiname
- status (automatisch_erkannt/manuell_bestätigt)
- erstellt_am
- aktualisiert_am

**schluesselwoerter**
- id (PK)
- dokument_id (FK)
- wort
- position
- konfidenz_score (0-100)

**protokoll** (optional)
- id (PK)
- benutzer_id (FK)
- aktion
- details
- zeitpunkt

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

### OCR
- Bibliothek: pytesseract (Tesseract OCR)
- Sprachen: Deutsch + Englisch
- Qualitätsschwellen: Konfidenz > 60%

### Mustererkennung
- **Kunden**: Regex-Pattern, lernt aus bisherigen Dokumenten
- **Fahrzeuge**: Kennzeichen-Regex, Verknüpfung mit Datenbank
- **Dokument-Typ**: Schlüsselwörter + Bayes-Klassifikator

### Konfidenz-System
- <50%: Manuelle Überprüfung erforderlich
- 50-80%: Vorschlag anzeigen, Bestätigung erfordern
- >80%: Automatische Übernahme

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
│   │   │   │   └── ...
│   │   └── ...
│   └── ...
├── Nicht_zugeordnet/
└── Backups/
    ├── Täglich/
    └── Manuell/
```

### Benennungskonventionen
- Kundenordner: Exakter Name (Sonderzeichen ersetzt)
- Fahrzeugordner: Kennzeichen (ohne Leerzeichen)
- Dateiname: `[Dokumenttyp]_[Datum]_[Nummer].pdf`

## Backup-System

### Tägliche automatische Backups
- Zeitpunkt: Konfigurierbar (Standard: Mitternacht)
- Speicherort: `/Backups/Täglich/`
- Inhalt: Vollständige Datenbank + `/Kunden/` Ordner
- Format: `backup_YYYY-MM-DD.zip`
- Aufbewahrung: 30 Tage

### Manuelle Backups
- Auslösbar über Hauptmenü oder F10
- Speicherort: `/Backups/Manuell/`
- Format: `backup_YYYY-MM-DD_HH-MM_Uhrzeit_Beschreibung.zip`
- Aufbewahrung: Unbegrenzt

### Restore-Funktion
- Wählt Backup aus Liste
- Zeigt Vorschau: Datum, Größe, Anzahl Dokumente
- Bestätigung erforderlich
- Automatisches Backup vor Restore

## Sicherheitskonzept

### Benutzerrollen
- **Besitzer**: Vollzugriff
- **Mitarbeiter**: Eingeschränkter Zugriff

### Berechtigungen
Mitarbeiter können: Dokumente hochladen, bearbeiten, Fahrzeuge zuordnen
Besitzer hat zusätzlich: Löschen, Backup, Benutzerverwaltung, Einstellungen

### Authentifizierung
- Benutzername + Passwort bei Programmstart
- Passwörter gehasht mit bcrypt
- Sitzung bis zum Programmende

## Scanner-Integration

### Scanner-Auswahl
- Automatische Erkennung verfügbarer Scanner
- Dropdown-Menü bei mehreren Scannern
- Standard-Scanner speichern

### Scan-Einstellungen
- Auflösung: 150/300/600 DPI
- Farbmodus: Schwarz-Weiß, Graustufen, Farbe
- Dateiformat: PDF (Standard)
- Einseitig oder doppelseitig
- Mehrere Seiten zu einem PDF

### Scan-Ablauf
- Benutzer klickt "Dokument scannen"
- Vorschau-Dialog
- Nach jedem Scan: "Weitere Seite scannen?"
- Bei "Nein": Direkt Upload zum Upload-Bildschirm

## Technologien und Bibliotheken

### Kern
- Python 3.12+
- PyQt6 (Benutzeroberfläche)
- sqlite3 (Datenbank)

### Dokumentenverarbeitung
- pdfplumber (PDF-Text-Extraktion)
- pytesseract (OCR)
- Pillow (Bildverarbeitung)
- pypdf2 (PDF-Manipulation, optional)

### Scanner-Integration
- pywin32 (WIA-Scanner, Windows-spezifisch)

### Backup
- zipfile (ZIP-Archive)
- shutil (Dateioperationen)

### Sicherheit
- bcrypt (Passwort-Hashing)

### Verpackung
- PyInstaller (.exe-Erstellung)

## Nächste Schritte

Design ist genehmigt. Nächster Schritt ist die Erstellung eines detaillierten Implementierungsplans mit dem `writing-plans` Skill.
