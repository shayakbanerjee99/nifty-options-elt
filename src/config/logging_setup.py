import logging.config
from pathlib import Path

import yaml

BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent.parent
LOGGER_CONFIG_FILE = BASE_DIR / "logging.yaml"


def setup_logging() -> None:
    with open(LOGGER_CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)

    for handler in config.get("handlers", {}).values():
        if "filename" in handler:
            log_path = PROJECT_ROOT / handler["filename"]
            log_path.parent.mkdir(parents=True, exist_ok=True)
            handler["filename"] = str(log_path)

    logging.config.dictConfig(config)