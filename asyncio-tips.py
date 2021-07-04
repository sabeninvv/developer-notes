from os.path import isfile
from typing import NoReturn
import base64
import hashlib
import hmac
import asyncio
import aiofiles
from aiohttp import ClientSession
from aiohttp.client import _RequestContextManager


def sig_hash_msg(*, secret_message: str, secret_key: str = "private-key", digestmod=hashlib.sha256) -> str:
    """
    Кодирование сообщения, используя односторонние хэш-функции типа sha2
    :param secret_message: Сообщение для хэширования
    :param secret_key: Ключ для хэширования
    :param digestmod: Алгоритм хэширования
    :return: Кодированная строка.
    """
    secret_message, secret_key = bytes(secret_message, "UTF-8"), bytes(secret_key, "UTF-8")
    digester = hmac.new(key=secret_key, msg=secret_message, digestmod=digestmod)
    signature = digester.digest()
    signature = base64.urlsafe_b64encode(signature)
    return str(signature, "UTF-8")


async def save_file(*, content: bytes, path2file: str) -> NoReturn:
    """
    Асинхронное сохранение файла
    :param content:
    :param path2file:
    """
    async with aiofiles.open(path2file, mode="wb") as stream:
        await stream.write(content)


def get_media_type(*, response: _RequestContextManager, default_content_type: str = "mp4") -> str:
    """
    Распарсить медиа тип файла
    :param response: _RequestContextManager
    :return: медиа тип файла
    """
    try:
        return response.content_type.split("/")[-1]
    except:
        return default_content_type


async def download_bytes(*, url: str) -> str:
    """
    Создать сессию, отправить GET запрос, проверить на статус НЕ 400.
    Получить тип скачиваемого объекта (.json, .mp4, .jpg, etc).
    Создать хэш из url по которому хранится  файл.
    Сохранить объект как ХЭШ.ТИП

    Если объект находится в хранилище типа s3, то уточните, если ли время жизни у ссылок на файлы.
    Если есть, то имеет смысл использовать хэширование
    :param url: ссылка по которому хранится  файл
    :return: путь до файла
    """
    async with ClientSession() as session:
        async with session.get(url=url) as resp:
            resp.raise_for_status()
            bytes_data = await resp.read()
            media_type = get_media_type(response=resp)
            file_name = sig_hash_msg(secret_message=url)
            path2file = f"{file_name}.{media_type}"
            if not isfile(path2file):
                await save_file(content=bytes_data, path2file=path2file)
            return path2file


async def run_gather():
    url = "https://ya.ru"
    tasks = (asyncio.create_task(coro=download_bytes(url=url)) for _ in range(10))
    return await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    answer = loop.run_until_complete(run_gather())
