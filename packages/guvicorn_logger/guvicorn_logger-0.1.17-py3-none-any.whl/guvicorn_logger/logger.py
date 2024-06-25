import logging
import os
from logging import config


class Logger:
    """
    fmt: formatter default -> "(%(asctime)s) (%(correlation_id)s) (%(pid)s) | %(levelprefix)s %(message)s"
    use_colors: by default is true
    correlation_id: to use the lib asgi-correlation-id

    """

    # TODO
    # path_file_log:
    #    You can specify a path where the logs will be saved in the
    #    file: log.log!
    #    Enter only the path, as the file names are standard.

    def __init__(
        self,
        fmt: str = None,
        use_colors: bool = True,  # TODO path_file_log: str = None
        correlation_id: bool = False,
    ) -> None:
        self._use_colors = use_colors
        self._path_file_log = None  # path_file_log
        self._correlation_id = correlation_id
        if correlation_id:
            DEFAULT_FORMAT = "(%(asctime)s) (%(correlation_id)s) (%(pid)s) | %(levelprefix)s %(message)s"
        else:
            DEFAULT_FORMAT = "(%(asctime)s) (%(pid)s) | %(levelprefix)s %(message)s"
        self._formatter = fmt or DEFAULT_FORMAT

    def _check_file_path(self):
        self._path_file_log = os.path.normpath(f"{self._path_file_log}")
        if not os.path.exists(self._path_file_log):
            try:
                os.mkdir(self._path_file_log)
            except PermissionError:
                raise PermissionError("The directory does not exist and is not allowed to create.")
            except Exception as err:
                print(err.with_traceback(None))

    def get_config(self):
        formatter_file = {
            "default_file": {
                "()": "guvicorn_logger.core.DefaultFormatter",
                "fmt": self._formatter,
                "use_colors": False,
            },
            "access_file": {
                "()": "guvicorn_logger.core.AccessFormatter",
                "fmt": self._formatter,
                "use_colors": False,
            },
        }

        handlers_file = {
            "console_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "default_file",
                "filename": f"{self._path_file_log}/log.log",
                "maxBytes": 1024,
                "backupCount": 3,
            },
            "access_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "access_file",
                "filename": f"{self._path_file_log}/log.log",
                "maxBytes": 1024,
                "backupCount": 3,
            },
        }

        config = {
            "version": 1,
            "disable_existing_loggers": False,
            "filters": {
                "correlation_id": {
                    "()": "asgi_correlation_id.CorrelationIdFilter",
                    "uuid_length": 8,
                },
            },
            "formatters": {
                "default": {
                    "()": "guvicorn_logger.core.DefaultFormatter",
                    "fmt": self._formatter,
                    "use_colors": self._use_colors,
                },
                "access": {
                    "()": "guvicorn_logger.core.AccessFormatter",
                    "fmt": self._formatter,
                    "use_colors": self._use_colors,
                },
            },
            "handlers": {
                "console": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "filters": ["correlation_id"],
                },
                "access": {
                    "formatter": "access",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                    "filters": ["correlation_id"],
                },
            },
            "root": {"handlers": ["console"], "level": "INFO"},
            "loggers": {
                "gunicorn": {"propagate": True},
                "gunicorn.info": {"propagate": True},
                "gunicorn.access": {
                    "level": "INFO",
                    "handlers": ["access"],
                    "propagate": False,
                    "qualname": "gunicorn.access",
                },
                "gunicorn.error": {"propagate": True},
                "uvicorn": {"propagate": True},
                "uvicorn.access": {
                    "level": "DEBUG",
                    "handlers": ["access"],
                    "propagate": False,
                    "qualname": "uvicorn.access",
                },
                "uvicorn.error": {"propagate": True},
            },
        }
        if self._path_file_log:
            self._check_file_path()
            config["handlers"].update(handlers_file)
            config["formatters"].update(formatter_file)
            config["root"]["handlers"].append("console_file")
            for key in config["loggers"]:
                if key in ("gunicorn.access", "uvicorn.access"):
                    config["loggers"][key]["handlers"].append("access_file")
                elif "handlers" in config["loggers"][key]:
                    config["loggers"][key]["handlers"].append("console_file")
                else:
                    config["loggers"][key].update({"handlers": ["console_file"]})

        return config

    def configure(self) -> logging:
        log_config = self.get_config()
        config.dictConfig(log_config)

        return logging
