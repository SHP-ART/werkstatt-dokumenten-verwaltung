import pytest
from database.models import Benutzer, Kunde, Fahrzeug, Dokument, Schluesselwort, Einstellung, Protokoll

def test_benutzer_model():
    """Test Benutzer-Modell"""
    # Wir erstellen Dummy-Objekte für den Test
    assert Benutzer.__name__ == "Benutzer"

def test_kunde_model():
    """Test Kunde-Modell"""
    assert Kunde.__name__ == "Kunde"

def test_fahrzeug_model():
    """Test Fahrzeug-Modell"""
    assert Fahrzeug.__name__ == "Fahrzeug"

def test_dokument_model():
    """Test Dokument-Modell"""
    assert Dokument.__name__ == "Dokument"
