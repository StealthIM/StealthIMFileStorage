from . import bind_server as serv
from .proto import filestorage_pb2
from . import config
from . import storage
from . import errorcode
from typing import Any
import asyncio


def init() -> None:
    pass


@serv.serve
async def Ping(_: Any) -> filestorage_pb2.Pong:
    return filestorage_pb2.Pong()


@serv.serve
async def GetFile(data: filestorage_pb2.GetFileRequest) -> filestorage_pb2.GetFileResponse:
    try:
        dt = await storage.get(data.hash, data.block)
        return filestorage_pb2.GetFileResponse(result=filestorage_pb2.Result(code=errorcode.SUCCESS, msg=""), block_data=dt)
    except Exception as e:
        return filestorage_pb2.GetFileResponse(result=filestorage_pb2.Result(code=errorcode.SERVER_INTERNAL_COMPONENT_ERROR, msg=str(e)), block_data=b"")


@serv.serve
async def SaveFile(data: filestorage_pb2.SaveFileRequest) -> filestorage_pb2.SaveFileResponse:
    try:
        await storage.save(data.block_data, data.hash, data.block)
        return filestorage_pb2.SaveFileResponse(result=filestorage_pb2.Result(code=errorcode.SUCCESS, msg=""))
    except Exception as e:
        return filestorage_pb2.SaveFileResponse(result=filestorage_pb2.Result(code=errorcode.SERVER_INTERNAL_COMPONENT_ERROR, msg=str(e)))


@serv.serve
async def RemoveBlock(data: filestorage_pb2.RemoveBlockRequest) -> filestorage_pb2.RemoveBlockResponse:
    asyncio.create_task(storage.delete(data.block_hash))
    return filestorage_pb2.RemoveBlockResponse(result=filestorage_pb2.Result(code=errorcode.SUCCESS, msg=""))


@serv.serve
async def GetUsage(data: filestorage_pb2.GetUsageRequest) -> filestorage_pb2.GetUsageResponse:
    return filestorage_pb2.GetUsageResponse(result=filestorage_pb2.Result(code=errorcode.SUCCESS, msg=""), usage=storage.usage, total=config.Max_Block)


@serv.serve
async def Reload(data: filestorage_pb2.ReloadRequest) -> filestorage_pb2.ReloadResponse:
    asyncio.create_task(config.reload_cfg())
    return filestorage_pb2.ReloadResponse(result=filestorage_pb2.Result(code=errorcode.SUCCESS, msg=""))
