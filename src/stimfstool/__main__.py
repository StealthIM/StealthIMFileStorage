from grpclib.client import Channel
from .proto import filestorage_pb2, filestorage_grpc
import argparse
import asyncio

parser = argparse.ArgumentParser(description='计算两个数字的和')

parser.add_argument('cmd', type=str, help='命令')
parser.add_argument('--server', type=str, help='服务器地址',
                    default="127.0.0.1:50052", required=False)

args = parser.parse_args()

server: str = args.server


async def reload():
    channel = Channel(server.split(":")[0], int(server.split(":")[1]))
    stub = filestorage_grpc.StealthIMFileStorageStub(channel)
    request = filestorage_pb2.ReloadRequest()
    response = await stub.Reload(request)
    print(repr(response))
    channel.close()


async def usage():
    channel = Channel(server.split(":")[0], int(server.split(":")[1]))
    stub = filestorage_grpc.StealthIMFileStorageStub(channel)
    request = filestorage_pb2.GetUsageRequest()
    response = await stub.GetUsage(request)
    print(str(response.usage)+"/"+str(response.total))
    channel.close()

if (args.cmd == "reload"):
    asyncio.run(reload())
elif (args.cmd == "usage"):
    asyncio.run(usage())
