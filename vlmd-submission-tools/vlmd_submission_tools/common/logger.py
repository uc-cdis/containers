"""Module for custom logging. Adapted from Nils Homer's
work (https://github.com/nh13).
@author: Kyle Hernandez <kmhernan@uchicago.edu>
"""
import logging
import sys


class Logger(object):
    """Provides methods to obtain loggers."""

    RootLogger = logging.getLogger("vlmd_submission_tools")
    LoggerFormat = "[%(levelname)s] [%(asctime)s] [%(name)s] - %(message)s"

    @classmethod
    def setup_root_logger(cls) -> None:
        """Sets up the root logger and should only be called once."""
        for handle in Logger.RootLogger.handlers:
            Logger.RootLogger.removeHandler(handle)
            Logger.RootLogger.setLevel(level=Logger.LoggerLevel)

        handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(Logger.LoggerFormat, datefmt="%Y%m%d %H:%M:%S")
        handler.setFormatter(formatter)
        Logger.RootLogger.addHandler(handler)

    LoggerLevel = logging.INFO

    @classmethod
    def get_logger(cls, name: str, stream=None) -> logging.Logger:
        """Gets a logger with the given name.  If a ``stream`` is not
        provided, the logger will be a child of the root logger, otherwise, a
        new logger is created using the given ``stream``."""
        if not stream:
            logger = Logger.RootLogger.getChild(name)
        else:
            logger = logging.getLogger(name)
            handler = logging.StreamHandler(stream)
            formatter = logging.Formatter(Logger.LoggerFormat)
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger


Logger.setup_root_logger()
