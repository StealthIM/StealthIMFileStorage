import hashlib
import aiofiles
import aiofiles.os
import os
from . import config

usage: int = 0


async def save(bytes: bytes) -> None:
    global usage
    usage += 1
    try:
        hashstr = hashlib.sha256(bytes).hexdigest()
        hash_head = hashstr[:2]
        await aiofiles.os.makedirs(f"{config.Storage_Dir}{os.sep}{hash_head}", exist_ok=True)
        assert await aiofiles.os.path.exists(f"{config.Storage_Dir}{os.sep}{hash_head}{os.sep}{hashstr}") is False
        async with aiofiles.open(f"{config.Storage_Dir}{os.sep}{hash_head}{os.sep}{hashstr}", "wb") as f:
            await f.write(bytes)
    except AssertionError:
        usage -= 1
    except Exception as e:
        usage -= 1
        raise e


async def get(hashstr: str) -> bytes:
    global usage
    hash_head = hashstr[:2]
    async with aiofiles.open(f"{config.Storage_Dir}{os.sep}{hash_head}{os.sep}{hashstr}",  "rb") as f:
        return await f.read()


async def delete(hashstr: str) -> None:
    global usage
    usage -= 1
    hash_head = hashstr[:2]
    try:
        await aiofiles.os.remove(f"{config.Storage_Dir}{os.sep}{hash_head}{os.sep}{hashstr}")
    except Exception:
        usage += 1


def get_usage():
    global usage
    usage = 0
    usage_tmp = 0
    usage_tmp = sum(len(os.listdir(f"{config.Storage_Dir}{os.sep}{i}"))
                    for i in os.listdir(str(config.Storage_Dir)))
    usage = usage_tmp
