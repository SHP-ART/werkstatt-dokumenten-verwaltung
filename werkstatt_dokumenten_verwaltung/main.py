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
