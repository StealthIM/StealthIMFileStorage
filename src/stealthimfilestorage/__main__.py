import asyncio
import uvloop
import argparse
from . import config
from . import server
from . import bind_server
from . import storage


def main():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    parser = argparse.ArgumentParser(description="A simple example script.")
    parser.add_argument('--config', type=str,
                        help='Config file path', default="config.toml")
    args = parser.parse_args()
    config.load_cfg(args.config)
    server.init()
    storage.get_usage()
    uvloop.run(bind_server.run())


if __name__ == "__main__":
    main()
