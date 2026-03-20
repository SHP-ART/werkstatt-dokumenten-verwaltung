from datetime import datetime
from typing import Optional
import logging

# Dummy-Module für vereinfachte Installation
from dummy_modules import declarative_base_func, Column, relationship, ForeignKey, Integer, String, DateTime, Float, Boolean

logger = logging.getLogger(__name__)

Base = declarative_base_func()

class Benutzer(Base):
    """Benutzer-Tabelle"""
    __tablename__ = "benutzer"

    id = Column(Integer, primary_key=True)
    benutzername = Column(String(50), unique=True, nullable=False)
    passwort_hash = Column(String(255), nullable=False)
    rolle = Column(String(20), nullable=False)  # 'besitzer' oder 'mitarbeiter'
    erstellt_am = Column(DateTime, default=datetime.utcnow)
    zuletzt_geloggt = Column(DateTime)

    def __repr__(self):
        return f"<Benutzer(id={self.id}, benutzername='{self.benutzername}', rolle='{self.rolle}')>"

class Kunde(Base):
    """Kunden-Tabelle"""
    __tablename__ = "kunden"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    adresse = Column(String(200))
    telefon = Column(String(20))
    email = Column(String(100))
    erstellt_am = Column(DateTime, default=datetime.utcnow)

    # Beziehungen
    fahrzeuge = relationship("Fahrzeug", back_populates="kunde")

    def __repr__(self):
        return f"<Kunde(id={self.id}, name='{self.name}')>"

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

    # Beziehungen
    kunde = relationship("Kunde", back_populates="fahrzeuge")
    dokumente = relationship("Dokument", back_populates="fahrzeug")

    def __repr__(self):
        return f"<Fahrzeug(id={self.id}, kennzeichen='{self.kennzeichen}')>"

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
    aktualisiert_am = Column(DateTime, default=datetime.utcnow)

    # Beziehungen
    kunde = relationship("Kunde", foreign_keys=[kunden_id])
    fahrzeug = relationship("Fahrzeug", back_populates="dokumente")
    schluesselwoerter = relationship("Schluesselwort", back_populates="dokument")

    def __repr__(self):
        return f"<Dokument(id={self.id}, typ='{self.dokument_typ}', nummer='{self.nummer}')>"

class Schluesselwort(Base):
    """Schlüsselwörter-Tabelle"""
    __tablename__ = "schluesselwoerter"

    id = Column(Integer, primary_key=True)
    dokument_id = Column(Integer, ForeignKey("dokumente.id"), nullable=False)
    wort = Column(String(100), nullable=False)
    position = Column(Integer)  # Position im Dokument
    konfidenz_score = Column(Integer)  # 0-100

    # Beziehungen
    dokument = relationship("Dokument", back_populates="schluesselwoerter")

    def __repr__(self):
        return f"<Schluesselwort(id={self.id}, wort='{self.wort}', konfidenz={self.konfidenz_score})>"

class Einstellung(Base):
    """Einstellungen-Tabelle"""
    __tablename__ = "einstellungen"

    id = Column(Integer, primary_key=True)
    benutzer_id = Column(Integer, ForeignKey("benutzer.id"), nullable=False)
    schluessel = Column(String(100), nullable=False)
    wert = Column(String(500))
    aktualisiert_am = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Einstellung(id={self.id}, schluessel='{self.schluessel}')>"

class Protokoll(Base):
    """Protokoll-Tabelle"""
    __tablename__ = "protokoll"

    id = Column(Integer, primary_key=True)
    benutzer_id = Column(Integer, ForeignKey("benutzer.id"), nullable=True)
    aktion = Column(String(50), nullable=False)
    details = Column(String(500))
    zeitpunkt = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Protokoll(id={self.id}, aktion='{self.aktion}')>"
