import aiofiles
import aiofiles.os
import os
import asyncio
import shutil
from . import config

usage: int = 0


async def save(bytes: bytes, hashstr: str, block_id: int) -> None:
    global usage
    usage += 1
    try:
        hash_head = hashstr[:2]
        await aiofiles.os.makedirs(f"{config.Storage_Dir}{os.sep}{hash_head}", exist_ok=True)
        assert await aiofiles.os.path.exists(f"{config.Storage_Dir}{os.sep}{hash_head}{os.sep}{hashstr}{os.sep}{block_id}") is False
        async with aiofiles.open(f"{config.Storage_Dir}{os.sep}{hash_head}{os.sep}{hashstr}{os.sep}{block_id}", "wb") as f:
            await f.write(bytes)
    except AssertionError:
        usage -= 1
    except Exception as e:
        usage -= 1
        raise e


async def get(hashstr: str, block_id: int) -> bytes:
    global usage
    hash_head = hashstr[:2]
    async with aiofiles.open(f"{config.Storage_Dir}{os.sep}{hash_head}{os.sep}{hashstr}{os.sep}{block_id}",  "rb") as f:
        return await f.read()


async def delete(hashstr: str) -> None:
    global usage
    usage -= 1
    hash_head = hashstr[:2]
    try:
        await asyncio.to_thread(lambda: shutil.rmtree(f"{config.Storage_Dir}{os.sep}{hash_head}{os.sep}{hashstr}"))
    except Exception:
        usage += 1


def get_usage():
    global usage
    usage = 0
    usage_tmp = 0
    usage_tmp = sum(len(os.listdir(f"{config.Storage_Dir}{os.sep}{i}"))
                    for i in os.listdir(str(config.Storage_Dir)))
    usage = usage_tmp
