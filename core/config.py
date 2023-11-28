import os
from configparser import ConfigParser

env = os.getenv("ENV", ".config")


def get_db_config():
    if env == ".config":
        config = ConfigParser()
        config.read(".config")
        config = config["database"]
    else:
        config = {
            "MONGO_CONNECTION_URL": os.getenv("MONGO_CONNECTION_URL", "mongodb://localhost:27017/demo_python"),
        }
    return config
