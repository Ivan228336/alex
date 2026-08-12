import asyncio
import os
from utils.render import FrameBuffer



async def generate_frames(path):
    try:
        while True:
            if not os.path.exists(path):
                await asyncio.sleep(1)
                continue

            with open(path, "rb") as file:
                frame_bytes = file.read()

            yield (b'--frame\r\n'
                   b'Content-Type: image/png\r\n\r\n' + frame_bytes + b'\r\n')

            await asyncio.sleep(0.5)
    except (asyncio.CancelledError, OSError, ConnectionResetError):
        # Это предотвратит падение всего сервера при закрытии вкладки клиентом
        print("Соединение закрыто клиентом или сетью")
        return  # Мягко завершаем генератор

async def frame_generator(court_id: int):
    pass