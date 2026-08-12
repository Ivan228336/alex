from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.v1.get.get_score import router as score_router
from api.v1.get.health import router as health_router
from api.v1.post.post_score import router as update_router
from api.v1.get.get_score_html import router as html_router
from api.v1.post.start_stop_stream import router as start_stop_router
from uvicorn import run
import multiprocessing
from pathlib import Path
from PIL import Image
import sys
import asyncio


def get_base_dir():
    """Возвращает базовую папку для чтения ресурсов (статики)."""
    if getattr(sys, 'frozen', False):
        # Запуск из .exe
        return Path(sys._MEIPASS)
    else:
        # Обычный запуск
        return Path(__file__).parent

def get_data_dir():
    """Возвращает папку для записи данных (media, json)."""
    if getattr(sys, 'frozen', False):
        # Рядом с .exe
        return Path(sys.executable).parent
    else:
        return Path(__file__).parent

proj_dir = get_base_dir()        # для чтения статики
data_dir = get_data_dir()        # для записи медиа

media_dir = data_dir / "media"
media_dir.mkdir(exist_ok=True)
json_path = data_dir / "data.json"

app = FastAPI(title="API для тенниса",
              version="1.0.0")


app.include_router(score_router)
app.include_router(update_router)
app.include_router(health_router)
app.include_router(html_router)
app.include_router(start_stop_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # В продакшене лучше указать конкретные адреса
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    # image = Image.open(proj_dir / "static" / "score_empty.png")
    # path = media_dir / "tennis_score.png"
    # image.save(path, format="PNG")
    # image.close()
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    for file in media_dir.glob('tennis_score*'):
        file.unlink()
        print(f"Удален файл: {file.name}")
    multiprocessing.freeze_support()
    run(app, host="0.0.0.0", port=8000)