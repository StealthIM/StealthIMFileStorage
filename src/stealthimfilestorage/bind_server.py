import grpclib
import grpclib.server
from . import config
# from .proto import filestorage_pb2
from .proto import filestorage_grpc
import types
from typing import Any, Coroutine, Callable
from . import config
import time


class Service():
    __mapping__ = filestorage_grpc.StealthIMFileStorageBase.__mapping__


def serve(func: Callable[[Any], Coroutine[Any, Any, Any]]) -> Callable[[Any, grpclib.server.Stream[Any, Any]], Coroutine[Any, Any, Any]]:
    def convert_ns(ns: int) -> str:
        if ns < 1000:
            return f"{ns} ns"
        elif ns < 1000000:
            us = ns / 1000
            return f"{us:.2f} us"
        elif ns < 1000000000:
            ms = ns / 1000000
            return f"{ms:.2f} ms"
        else:
            s = ns / 1000000000
            return f"{s:.2f} s"

    async def warpper(self: Any, stream: grpclib.server.Stream[Any, Any]):
        request = await stream.recv_message()
        if config.Enable_Log:
            t1 = time.time_ns()
            ret = await func(request)
            delta_t = time.time_ns()-t1
            print(f'[GRPC]Call {func.__name__} ({convert_ns(delta_t)})')
        else:
            ret = await func(request)
        await stream.send_message(ret)
    setattr(Service, func.__name__, types.MethodType(warpper, Service))
    return warpper


async def run() -> None:
    server = grpclib.server.Server([Service()])
    print(
        f'[GRPC]Started server at {config.configs["server"]["host"]}:{config.configs["server"]["port"]}')
    await server.start(host=config.configs["server"]["host"], port=config.configs["server"]["port"])
    await server.wait_closed()
