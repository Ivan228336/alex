from pathlib import Path
import sys


proj_dir = Path(__file__).parent

def get_base_dir():
    """Возвращает базовую папку для чтения ресурсов (статики)."""
    if getattr(sys, 'frozen', False):
        # Запуск из .exe
        return Path(sys._MEIPASS)
    else:
        # Обычный запуск
        return Path(__file__).parent

def get_data_dir():
    """Папка для записи данных (media, json) — рядом с exe или в корне проекта."""
    if getattr(sys, 'frozen', False):
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent