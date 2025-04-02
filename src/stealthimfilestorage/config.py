import tomllib
import os
import asyncio

configs = None

Storage_Dir = "./storage"
Max_Block = 0
Enable_Log = False

last_config_path = ""


def load_cfg(cfg_path: str = "config.toml"):
    global last_config_path
    last_config_path = cfg_path
    try:
        with open(cfg_path, "rb") as f:
            global configs
            configs = tomllib.load(f)
    except FileNotFoundError:
        print("Config file not found, creating a new one...")
        with open(os.path.dirname(__file__)+os.sep+"config.sample.toml", "r") as f:
            cfg = f.read()
        with open(cfg_path, "w") as f:
            f.write(cfg)
        os._exit(1)
    global Storage_Dir, Max_Block, Enable_Log
    Storage_Dir = configs["file"]["path"]
    Max_Block = configs["usage"]["total"]
    Enable_Log = configs["server"]["log"]


async def reload_cfg():
    global last_config_path
    await asyncio.to_thread(lambda: load_cfg(last_config_path))
    print("[CONF]Config Reloaded")
