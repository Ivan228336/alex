# import httpx
# from fastapi import APIRouter, HTTPException
#
# router = APIRouter()
#
# VMIX_URL = "http://127.0.0.1:8088/api/"
#
# @router.post("/vmix/stream/start/{court_id}")
# async def start_stream(court_id: int):
#     """Запустить трансляцию для корта court_id (1..4)"""
#     if 0 > court_id > 4:
#         return
#     try:
#         # vMix нумерует стримы с 0
#         stream_index = court_id - 1
#         async with httpx.AsyncClient() as client:
#             resp = await client.get(
#                 VMIX_URL,
#                 params={
#                     "Function": "StartStreaming",
#                     "Value": str(stream_index)   # указываем какой стрим
#                 }
#             )
#         if resp.status_code != 200:
#             raise HTTPException(status_code=resp.status_code, detail="vMix вернул ошибку")
#         return {"status": "ok", "vmix_response": resp.status_code}
#     except httpx.ConnectError:
#         raise HTTPException(status_code=503, detail="Не удалось подключиться к vMix (порт 8088)")
#
# @router.post("/vmix/stream/stop/{court_id}")
# async def stop_stream(court_id: int):
#     """Остановить трансляцию для корта court_id (1..4)"""
#     try:
#         stream_index = court_id - 1
#         async with httpx.AsyncClient() as client:
#             resp = await client.get(
#                 VMIX_URL,
#                 params={
#                     "Function": "StopStreaming",
#                     "Value": str(stream_index)
#                 }
#             )
#         if resp.status_code != 200:
#             raise HTTPException(status_code=resp.status_code, detail="vMix вернул ошибку")
#         return {"status": "ok", "vmix_response": resp.status_code}
#     except httpx.ConnectError:
#         raise HTTPException(status_code=503, detail="Не удалось подключиться к vMix (порт 8088)")

import httpx
import logging
from fastapi import APIRouter, HTTPException

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

router = APIRouter()
VMIX_URL = "http://127.0.0.1:8088/api/"

@router.post("/vmix/stream/start/{court_id}")
async def start_stream(court_id: int):
    """Запустить трансляцию для корта court_id (1..4)"""

    if court_id < 1 or court_id > 4:
        logger.warning(f"Некорректный court_id: {court_id}. Допустимы значения 1..4")
        raise HTTPException(status_code=400, detail="court_id должен быть от 1 до 4")

    stream_index = court_id - 1
    logger.info(f"Получен запрос на СТАРТ стрима для court_id={court_id} -> stream_index={stream_index}")

    try:
        async with httpx.AsyncClient() as client:
            params = {"Function": "StartStreaming", "Value": str(stream_index)}
            logger.info(f"Отправка GET-запроса к vMix: {VMIX_URL} с параметрами {params}")
            resp = await client.get(VMIX_URL, params=params)

        # Логируем ответ
        logger.info(f"vMix ответил статусом {resp.status_code}")
        if resp.status_code != 200:
            # Пытаемся прочитать тело ответа для диагностики
            try:
                response_text = resp.text
            except:
                response_text = "<не удалось прочитать тело>"
            logger.error(f"vMix вернул ошибку. Тело ответа: {response_text}")
            raise HTTPException(status_code=resp.status_code, detail=f"vMix вернул ошибку: {response_text}")

        logger.info(f"Команда StartStreaming для стрима {stream_index} выполнена успешно")
        return {"status": "ok", "vmix_response": resp.status_code}

    except httpx.ConnectError as e:
        logger.error(f"Не удалось подключиться к vMix по адресу {VMIX_URL}: {e}")
        raise HTTPException(status_code=503, detail="Не удалось подключиться к vMix (порт 8088)")
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при выполнении start_stream: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")

@router.post("/vmix/stream/stop/{court_id}")
async def stop_stream(court_id: int):
    """Остановить трансляцию для корта court_id (1..4)"""


    if court_id < 1 or court_id > 4:
        logger.warning(f"Некорректный court_id: {court_id}. Допустимы значения 1..4")
        raise HTTPException(status_code=400, detail="court_id должен быть от 1 до 4")

    stream_index = court_id - 1
    logger.info(f"Получен запрос на СТОП стрима для court_id={court_id} -> stream_index={stream_index}")

    try:
        async with httpx.AsyncClient() as client:
            params = {"Function": "StopStreaming", "Value": str(stream_index)}
            logger.info(f"Отправка GET-запроса к vMix: {VMIX_URL} с параметрами {params}")
            resp = await client.get(VMIX_URL, params=params)

        logger.info(f"vMix ответил статусом {resp.status_code}")
        if resp.status_code != 200:
            try:
                response_text = resp.text
            except:
                response_text = "<не удалось прочитать тело>"
            logger.error(f"vMix вернул ошибку. Тело ответа: {response_text}")
            raise HTTPException(status_code=resp.status_code, detail=f"vMix вернул ошибку: {response_text}")

        logger.info(f"Команда StopStreaming для стрима {stream_index} выполнена успешно")
        return {"status": "ok", "vmix_response": resp.status_code}

    except httpx.ConnectError as e:
        logger.error(f"Не удалось подключиться к vMix по адресу {VMIX_URL}: {e}")
        raise HTTPException(status_code=503, detail="Не удалось подключиться к vMix (порт 8088)")
    except Exception as e:
        logger.exception(f"Неожиданная ошибка при выполнении stop_stream: {e}")
        raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")