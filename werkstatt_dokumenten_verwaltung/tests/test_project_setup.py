import pytest
from pathlib import Path
from config import Config

def test_config_paths_exist():
    """Test, ob Config-Pfade korrekt gesetzt sind"""
    assert isinstance(Config.BASE_DIR, Path)
    assert Config.DATABASE_PATH == Config.BASE_DIR / "data" / "werkstatt.db"

def test_ensure_directories():
    """Test Verzeichniserstellung"""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp_dir:
        # Temporäres BASE_DIR setzen
        original_base = Config.BASE_DIR
        Config.BASE_DIR = Path(tmp_dir)

        Config.ensure_directories()

        # Prüfe, ob Verzeichnisse erstellt wurden
        assert (Config.DATABASE_PATH.parent).exists()
        assert Config.DOCUMENTS_PATH.exists()
        assert Config.BACKUP_PATH.exists()
        assert (Config.BACKUP_PATH / "Täglich").exists()
        assert (Config.BACKUP_PATH / "Manuell").exists()

        # Reset
        Config.BASE_DIR = original_base
