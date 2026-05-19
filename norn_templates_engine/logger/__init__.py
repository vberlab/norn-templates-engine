"""
    App logging configuration
"""
import logging
from norn_templates_engine.logger import errors
from norn_templates_engine.config import AppConfig

class LoggerConfigurator:

    @staticmethod
    def _resolve_level(level: str) -> int:
        """
            Resolve str option to logging level constant
        """
        levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
        }
        if level not in levels.keys():
            raise errors.LoggerError(
                f"Unsupported logging level [{level}]"
            )
        return levels[level]

    @staticmethod
    def build(config: AppConfig) -> None:
        """
            Configure global python logging system
            call this method on app startup
        """
        logging.basicConfig(
            level=LoggerConfigurator._resolve_level(config.logging.level),
            format=config.logging.format
        )
        