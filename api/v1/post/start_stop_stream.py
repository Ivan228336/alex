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

# import httpx
# import logging
# from fastapi import APIRouter, HTTPException
#
# # Настройка логирования
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# logger = logging.getLogger(__name__)
#
# router = APIRouter()
# VMIX_URL = "http://127.0.0.1:8088/api/"
#
# @router.post("/vmix/stream/start/{court_id}")
# async def start_stream(court_id: int):
#     """Запустить трансляцию для корта court_id (1..4)"""
#
#     if court_id < 1 or court_id > 4:
#         logger.warning(f"Некорректный court_id: {court_id}. Допустимы значения 1..4")
#         raise HTTPException(status_code=400, detail="court_id должен быть от 1 до 4")
#
#     stream_index = court_id - 1
#     logger.info(f"Получен запрос на СТАРТ стрима для court_id={court_id} -> stream_index={stream_index}")
#
#     try:
#         async with httpx.AsyncClient() as client:
#             params = {"Function": "StartStreaming", "Value": str(stream_index)}
#             logger.info(f"Отправка GET-запроса к vMix: {VMIX_URL} с параметрами {params}")
#             resp = await client.get(VMIX_URL, params=params)
#
#         # Логируем ответ
#         logger.info(f"vMix ответил статусом {resp.status_code}")
#         if resp.status_code != 200:
#             # Пытаемся прочитать тело ответа для диагностики
#             try:
#                 response_text = resp.text
#             except:
#                 response_text = "<не удалось прочитать тело>"
#             logger.error(f"vMix вернул ошибку. Тело ответа: {response_text}")
#             raise HTTPException(status_code=resp.status_code, detail=f"vMix вернул ошибку: {response_text}")
#
#         logger.info(f"Команда StartStreaming для стрима {stream_index} выполнена успешно")
#         return {"status": "ok", "vmix_response": resp.status_code}
#
#     except httpx.ConnectError as e:
#         logger.error(f"Не удалось подключиться к vMix по адресу {VMIX_URL}: {e}")
#         raise HTTPException(status_code=503, detail="Не удалось подключиться к vMix (порт 8088)")
#     except Exception as e:
#         logger.exception(f"Неожиданная ошибка при выполнении start_stream: {e}")
#         raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")
#
# @router.post("/vmix/stream/stop/{court_id}")
# async def stop_stream(court_id: int):
#     """Остановить трансляцию для корта court_id (1..4)"""
#
#
#     if court_id < 1 or court_id > 4:
#         logger.warning(f"Некорректный court_id: {court_id}. Допустимы значения 1..4")
#         raise HTTPException(status_code=400, detail="court_id должен быть от 1 до 4")
#
#     stream_index = court_id - 1
#     logger.info(f"Получен запрос на СТОП стрима для court_id={court_id} -> stream_index={stream_index}")
#
#     try:
#         async with httpx.AsyncClient() as client:
#             params = {"Function": "StopStreaming", "Value": str(stream_index)}
#             logger.info(f"Отправка GET-запроса к vMix: {VMIX_URL} с параметрами {params}")
#             resp = await client.get(VMIX_URL, params=params)
#
#         logger.info(f"vMix ответил статусом {resp.status_code}")
#         if resp.status_code != 200:
#             try:
#                 response_text = resp.text
#             except:
#                 response_text = "<не удалось прочитать тело>"
#             logger.error(f"vMix вернул ошибку. Тело ответа: {response_text}")
#             raise HTTPException(status_code=resp.status_code, detail=f"vMix вернул ошибку: {response_text}")
#
#         logger.info(f"Команда StopStreaming для стрима {stream_index} выполнена успешно")
#         return {"status": "ok", "vmix_response": resp.status_code}
#
#     except httpx.ConnectError as e:
#         logger.error(f"Не удалось подключиться к vMix по адресу {VMIX_URL}: {e}")
#         raise HTTPException(status_code=503, detail="Не удалось подключиться к vMix (порт 8088)")
#     except Exception as e:
#         logger.exception(f"Неожиданная ошибка при выполнении stop_stream: {e}")
#         raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {str(e)}")

# import asyncio
# import httpx
# import logging
# import xml.etree.ElementTree as ET
# from fastapi import APIRouter, HTTPException
#
# # Настройка логирования
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# logger = logging.getLogger(__name__)
#
# router = APIRouter()
# VMIX_URL = "http://127.0.0.1:8088/api/"
# HTTP_TIMEOUT = 5.0  # Таймаут для запросов к vMix
#
#
# # ---------- Вспомогательные функции ----------
#
# def parse_vmix_xml(xml_text: str) -> dict:
#     """Парсит XML-ответ vMix. Учитывает реальную структуру атрибутов channel1, channel2 и т.д."""
#     try:
#         root = ET.fromstring(xml_text)
#     except ET.ParseError as e:
#         logger.error(f"Ошибка парсинга XML: {e}")
#         return {"streaming": False, "error": "Невалидный XML от vMix", "streams": {}}
#
#     streaming_elem = root.find(".//streaming")
#     general_streaming = streaming_elem is not None and streaming_elem.text == "True"
#
#     error_elem = root.find(".//streamingerror")
#     general_error = error_elem.text if error_elem is not None and error_elem.text else None
#
#     # Парсим статусы по каналам (vMix использует атрибуты channel1, channel2, channel3)
#     streams_status = {}
#     if streaming_elem is not None:
#         # Проверяем, отдаёт ли vMix атрибуты channel (обычно отдаёт)
#         if streaming_elem.get("channel1") is not None:
#             for i in range(4):  # Индексы 0..3 (соответствуют channel1..4)
#                 ch_val = streaming_elem.get(f"channel{i + 1}", "False")
#                 streams_status[i] = (ch_val.lower() == "true")
#         else:
#             # Фолбек, если версия vMix старая и не отдает каналы
#             for i in range(4):
#                 streams_status[i] = general_streaming
#
#     return {
#         "streaming": general_streaming,
#         "error": general_error,
#         "streams": streams_status  # Словарь вида {0: False, 1: True, ...}
#     }
#
#
# async def get_vmix_state() -> dict:
#     """Запрашивает XML статус у vMix."""
#     async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
#         try:
#             resp = await client.get(VMIX_URL)
#             resp.raise_for_status()
#             return parse_vmix_xml(resp.text)
#         except Exception as e:
#             logger.exception(f"Ошибка при запросе состояния vMix: {e}")
#             raise HTTPException(status_code=503, detail="vMix недоступен (проверьте, запущен ли он)")
#
#
# async def send_vmix_command(function: str, value: str = ""):
#     """Отправляет команду во vMix."""
#     async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
#         params = {"Function": function, "Value": value}
#         try:
#             resp = await client.get(VMIX_URL, params=params)
#             resp.raise_for_status()
#             logger.info(f"Команда {function}({value}) успешно отправлена в vMix")
#         except Exception as e:
#             logger.error(f"Ошибка отправки команды {function}: {e}")
#             raise HTTPException(status_code=500, detail="Ошибка выполнения команды во vMix")
#
#
# # ---------- Эндпоинты ----------
#
# @router.post("/vmix/stream/start/{court_id}")
# async def start_stream(court_id: int):
#     if court_id < 1 or court_id > 4:
#         raise HTTPException(status_code=400, detail="court_id должен быть от 1 до 4")
#
#     stream_index = court_id - 1
#     logger.info(f"Запуск стрима: court_id={court_id} (в vMix это channel{stream_index + 1})")
#
#     # 1. Отправляем команду
#     await send_vmix_command("StartStreaming", str(stream_index))
#
#     # 2. Ждем, пока vMix свяжется с VK/YouTube и обновит XML
#     await asyncio.sleep(1.5)
#
#     # 3. Запрашиваем состояние
#     state = await get_vmix_state()
#     is_active = state["streams"].get(stream_index, False)
#
#     # 4. Прозрачный анализ результатов
#     if state["error"]:
#         # Если vMix вернул конкретную ошибку (например, неверный ключ VK)
#         logger.error(f"Ошибка vMix при запуске стрима {stream_index}: {state['error']}")
#         raise HTTPException(status_code=500, detail=f"Ошибка трансляции: {state['error']}")
#
#     if not is_active:
#         # Если ошибки нет, но статус False (обычно это значит, что стрим банально не настроен)
#         logger.error(f"Стрим {stream_index} не запустился. Вероятно, не настроен URL или ключ потока.")
#         raise HTTPException(status_code=500, detail="Стрим не запустился (проверьте настройки стрима во vMix)")
#
#     logger.info(f"Стрим {stream_index} успешно запущен!")
#     return {"status": "ok", "streaming": True, "error": None}
#
#
# @router.post("/vmix/stream/stop/{court_id}")
# async def stop_stream(court_id: int):
#     if court_id < 1 or court_id > 4:
#         raise HTTPException(status_code=400, detail="court_id должен быть от 1 до 4")
#
#     stream_index = court_id - 1
#     logger.info(f"Остановка стрима: court_id={court_id}")
#
#     await send_vmix_command("StopStreaming", str(stream_index))
#
#     await asyncio.sleep(0.5)
#     state = await get_vmix_state()
#     is_active = state["streams"].get(stream_index, False)
#
#     return {"status": "ok", "streaming": is_active, "error": state["error"]}
#
#
# @router.get("/vmix/stream/status/{court_id}")
# async def get_stream_status(court_id: int):
#     if court_id < 1 or court_id > 4:
#         raise HTTPException(status_code=400, detail="court_id должен быть от 1 до 4")
#
#     stream_index = court_id - 1
#     state = await get_vmix_state()
#
#     is_active = state["streams"].get(stream_index, False)
#
#     return {
#         "streaming": is_active,
#         "error": state["error"]
#     }

import asyncio
import httpx
import logging
import xml.etree.ElementTree as ET
from fastapi import APIRouter, HTTPException

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

router = APIRouter()
VMIX_URL = "http://127.0.0.1:8088/api/"
HTTP_TIMEOUT = 5.0


def parse_vmix_xml(xml_text: str) -> dict:
    """Парсит XML-ответ vMix с поддержкой мультистриминга и общего статуса."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        logger.error(f"Ошибка парсинга XML: {e}")
        return {"streaming": False, "error": "Невалидный XML от vMix", "streams": {}}

    streaming_elem = root.find(".//streaming")
    general_streaming = streaming_elem is not None and streaming_elem.text.lower() == "true"

    error_elem = root.find(".//streamingerror")
    general_error = error_elem.text if error_elem is not None and error_elem.text else None

    streams_status = {}
    if streaming_elem is not None:
        # Проверяем, есть ли отдельные каналы в XML от vMix
        has_channels = any(streaming_elem.get(f"channel{i + 1}") is not None for i in range(4))

        if has_channels:
            for i in range(4):
                ch_val = streaming_elem.get(f"channel{i + 1}", "False")
                streams_status[i] = (ch_val.lower() == "true")
        else:
            # Если мультистриминг в vMix не настроен, все корты используют общий статус
            for i in range(4):
                streams_status[i] = general_streaming

    return {
        "streaming": general_streaming,
        "error": general_error,
        "streams": streams_status
    }


async def get_vmix_state() -> dict:
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        try:
            resp = await client.get(VMIX_URL)
            resp.raise_for_status()
            return parse_vmix_xml(resp.text)
        except Exception as e:
            logger.exception(f"Ошибка при запросе состояния vMix: {e}")
            raise HTTPException(status_code=503, detail="vMix недоступен (проверьте, запущен ли он)")


async def send_vmix_command(function: str, value: str = ""):
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        params = {"Function": function, "Value": value}
        try:
            resp = await client.get(VMIX_URL, params=params)
            resp.raise_for_status()
            logger.info(f"Команда {function}({value}) успешно отправлена в vMix")
        except Exception as e:
            logger.error(f"Ошибка отправки команды {function}: {e}")
            raise HTTPException(status_code=502, detail="Ошибка выполнения команды во vMix")


@router.post("/vmix/stream/start/{court_id}")
async def start_stream(court_id: int):
    if court_id < 1 or court_id > 4:
        raise HTTPException(status_code=400, detail="court_id должен быть от 1 до 4")

    stream_index = court_id - 1
    logger.info(f"Запуск стрима: court_id={court_id}")

    await send_vmix_command("StartStreaming", str(stream_index))
    await asyncio.sleep(2.5)

    state = await get_vmix_state()
    is_active = state["streams"].get(stream_index, False)

    if state["error"]:
        logger.error(f"Ошибка vMix: {state['error']}")
        raise HTTPException(status_code=400, detail=f"Ошибка трансляции: {state['error']}")

    if not is_active:
        logger.error(f"Стрим {stream_index} не запустился (нет потока или не настроен ключ).")
        # Возвращаем 400 Bad Request вместо 500 Internal Server Error
        raise HTTPException(status_code=400,
                            detail="Стрим не запустился. Проверьте настройки URL во vMix.")

    return {"status": "ok", "streaming": True, "error": None}


@router.post("/vmix/stream/stop/{court_id}")
async def stop_stream(court_id: int):
    if court_id < 1 or court_id > 4:
        raise HTTPException(status_code=400, detail="court_id должен быть от 1 до 4")

    stream_index = court_id - 1
    logger.info(f"Остановка стрима: court_id={court_id}")

    await send_vmix_command("StopStreaming", str(stream_index))
    await asyncio.sleep(2.0)

    state = await get_vmix_state()
    is_active = state["streams"].get(stream_index, False)

    return {"status": "ok", "streaming": is_active, "error": state["error"]}


@router.get("/vmix/stream/status/{court_id}")
async def get_stream_status(court_id: int):
    if court_id < 1 or court_id > 4:
        raise HTTPException(status_code=400, detail="court_id должен быть от 1 до 4")

    stream_index = court_id - 1
    state = await get_vmix_state()
    is_active = state["streams"].get(stream_index, False)

    return {
        "streaming": is_active,
        "error": state["error"]
    }