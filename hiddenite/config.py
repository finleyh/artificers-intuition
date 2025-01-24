import os
import configparser

CONFIG_PATH = os.path.expanduser("~/.hiddenite/config.ini")


def create_default_config():
    """Create a default configuration file if it doesn't exist"""
    if os.path.exists(CONFIG_PATH):
        print(f"Configuration file already exists at '{CONFIG_PATH}'")
        return

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    config=configparser.ConfigParser()

    config["PostgreSQL"]={
        "dbname":"mwcp_data",
        "user":"your_user",
        "password":"your_password",
        "host":"127.0.0.1",
        "port":"5432"
    }

    config["API"]={
        "url":"http://127.0.0.1:8040/run_parser?recursive=true&output=json"
    }

    with open(CONFIG_PATH, "w") as config_file:
        config.write(config_file)
    print(f"Default configuration created at '{CONFIG_PATH}'")

def load_config():
    """Load the configuration file."""
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file not found at '{CONFIG_PATH}'")

    config=configparser.ConfigParser()
    config.read(CONFIG_PATH)

    db_config={
        "dbname":config["PostgreSQL"]["dbname"],
        "user":config["PostgreSQL"]["user"],
        "password":config["PostgreSQL"]["password"],
        "host":config["PostgreSQL"]["host"],
        "port":config["PostgreSQL"]["port"],
    }

    api_url = config["API"]["url"]

    return db_config, api_url
