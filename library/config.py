# library/config.py
import os

class Config:
    __data = {}

    @staticmethod
    def load():
        if Config.__data:
            return 

        files = ["config/database.txt", "config/base.txt"]
        for path in files:
            if os.path.exists(path):
                with open(path, "r") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            key, value = line.split("=", 1)
                            Config.__data[key.strip()] = value.strip()
            else:
                print(f"\033[33mWarning: file not found: {path}\033[0m")

    @staticmethod
    def get(key, default=None):
        Config.load()
        return Config.__data.get(key, default)

    @staticmethod
    def all():
        Config.load()
        return Config.__data.copy()
