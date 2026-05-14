"""
    Configuration loader class
"""
import yaml
from pathlib import Path
from norn_templates_engine.config import AppConfig
from norn_templates_engine.config import errors

class ConfigLoader:

    def load(self, path: str | Path) -> AppConfig:
        pass

    def _check_config_path(self, path: Path) -> None:
        """
            Check config file avail by passed path or raise error
        """
        if not path.exists():
            raise errors.ConfigNotFoundError(f"Configuration file {path} does not exists")
        if not path.is_file():
            raise errors.ConfigNotFoundError(f"Path of configuration file {path} is not a file")
        return

    def _read_yaml(self,path: Path):
        """
            Read yaml data from configuration file
        """
        try:
            with path.open("r", encoding="utf-8") as _fd_:
                data = yaml.safe_load(_fd_)
        except yaml.YAMLError as err:
            raise errors.ConfigParseError(f"Invalid YAML config: {path}") from err
        except OSError as err:
            raise errors.ConfigLoaderError(f"Cannot read configuration file: {path}") from err
        if data is None:
            raise errors.ConfigEmpty(f"Empty config file. Some options must declared explicity.")
        if not isinstance(data, dict):
            raise errors.ConfigValidationError(f"Invalid data type {type(data.__name__)}, must be mapping object")
        return data

    def _validate(self, data):
        """
            Validate configuration data
        """
