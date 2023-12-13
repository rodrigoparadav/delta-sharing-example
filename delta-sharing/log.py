import logging
import os
import warnings
from functools import wraps
from pythonjsonlogger import jsonlogger
from threading import Lock

TEXT = "text"
JSON = "json"
MAX_AMOUNT_OF_CHR = 200
formaters = {
    TEXT: logging.Formatter(
        os.environ.get(
            "STD_LOG_FORMAT", "[%(asctime)s] %(module)s - %(levelname)s - %(msg)s"
        )
    ),
    JSON: jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(name)s %(funcName)s %(msg)s"
    ),
}


class Log:
    """Data Platform thread-safe centralized logger.

    Custom logger that acts as a singleton resource by using the "data_platform" logger name.
    The logger is able to send messages to the following handlers:
      - StreamHandler (stderr).
    """

    __instance = None
    _lock = Lock()

    _logger = None

    def __new__(cls, name=None, level=None, type=None, *args, **kwargs):
        with cls._lock:
            if cls.__instance is None:
                cls.__instance = super().__new__(cls)
                cls._name = name or __name__
                cls._level = level or os.environ.get("LOG_LEVEL", "INFO")
                cls._type = type or os.environ.get("LOG_TYPE", JSON)
                cls._init_logger()

        return cls.__instance

    @classmethod
    def _init_logger(cls):
        """Initializes the Data Platform logger and corresponding handlers using environment variables settings."""
        cls._logger = logging.getLogger(cls._name)

        logger_level = os.environ.get("LOG_LEVEL", "INFO")
        Log._logger.setLevel(logger_level)

        # StreamHandler (stderr).
        std_handler = logging.StreamHandler()
        cls._logger.setLevel(cls._level)
        if str(cls._type).lower() not in formaters.keys():
            type = TEXT
        fmt = formaters.get(cls._type)
        std_handler.setFormatter(fmt)
        cls._logger.addHandler(std_handler)

    @classmethod
    def get_instance(cls) -> logging.Logger:
        return cls._logger

    @classmethod
    def log(cls) -> logging.Logger:
        warnings.warn(
            "log() is deprecated, use get_instance() instead", DeprecationWarning
        )
        return cls._logger
