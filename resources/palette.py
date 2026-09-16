from PySide6.QtCore import QSettings
from PySide6.QtGui import QColor, QPalette

from resources.themes.catppuccin_mocha import CATPPUCCIN_MOCHA
from resources.themes.dark import DARK
from resources.themes.dracula import DRACULA
from resources.themes.gruvbox_dark import GRUVBOX_DARK
from resources.themes.light import LIGHT
from resources.themes.nord import NORD
from resources.themes.solarized_light import SOLARIZED_LIGHT

THEMES: dict[str, dict[str, str]] = {
    "Catppuccin Mocha": CATPPUCCIN_MOCHA,
    "Dracula": DRACULA,
    "Nord": NORD,
    "Solarized Light": SOLARIZED_LIGHT,
    "Gruvbox Dark": GRUVBOX_DARK,
    "Light": LIGHT,
    "Dark": DARK,
}


def get_theme_name() -> str:
    settings = QSettings("Apex", "ApexFinance")
    return str(settings.value("theme_name", "catppuccin_mocha"))


def set_theme_name(name: str) -> None:
    settings = QSettings("Apex", "ApexFinance")
    settings.setValue("theme_name", name)


THEME: dict[str, str] = THEMES.get(get_theme_name(), CATPPUCCIN_MOCHA)


def build_qpalette(theme: dict[str, str]) -> QPalette:
    p: QPalette = QPalette()
    p.setColor(QPalette.ColorRole.Window, QColor(theme["background"]))
    p.setColor(QPalette.ColorRole.Base, QColor(theme["header"]))
    p.setColor(QPalette.ColorRole.WindowText, QColor(theme["text"]))
    p.setColor(QPalette.ColorRole.Text, QColor(theme["text"]))
    p.setColor(QPalette.ColorRole.Button, QColor(theme["header"]))
    p.setColor(QPalette.ColorRole.ButtonText, QColor(theme["text"]))
    p.setColor(QPalette.ColorRole.Highlight, QColor(theme["accent"]))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor(theme["background"]))
    p.setColor(QPalette.ColorRole.PlaceholderText, QColor(theme["muted"]))
    return p
