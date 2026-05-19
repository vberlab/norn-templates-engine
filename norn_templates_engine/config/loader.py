"""
    Configuration loader class
"""
import yaml
from pathlib import Path
from norn_templates_engine.config import AppConfig, ConfigModel
from norn_templates_engine.config import errors
from norn_templates_engine.config.validator import ConfigurationValidator
from norn_templates_engine.config.schema import APP_CONFIG_SCHEMA

class ConfigLoader:

    def load(self, path: str | Path) -> AppConfig:
        _path = path
        if isinstance(path, str):
            _path = Path(path)
        self._check_config_path(path=_path)
        _data = self._read_yaml(path=_path)
        self._validate(data=_data)
        return self._build_config(data=_data)

    @staticmethod
    def _check_config_path(path: Path) -> None:
        """
            Check config file avail by passed path or raise error
        """
        if not path.exists():
            raise errors.ConfigNotFoundError(f"Configuration file [{path}] does not exists")
        if not path.is_file():
            raise errors.ConfigNotFoundError(f"Path of configuration file [{path}] is not a file")
        return

    @staticmethod
    def _read_yaml(path: Path) -> dict:
        """
            Read yaml data from configuration file
        """
        try:
            with path.open("r", encoding="utf-8") as _fd_:
                data = yaml.safe_load(_fd_)
        except yaml.YAMLError as err:
            raise errors.ConfigParseError(f"Invalid YAML config: [{path}]") from err
        except OSError as err:
            raise errors.ConfigLoaderError(f"Cannot read configuration file: [{path}]") from err
        if data is None:
            raise errors.ConfigEmpty(f"Empty config file. Some options must declared explicity.")
        if not isinstance(data, dict):
            raise errors.ConfigValidationError(f"Invalid data type [{type(data).__name__}], must be mapping object")
        return data

    @staticmethod
    def _validate(data: dict):
        """
            Validate configuration data
        """
        return ConfigurationValidator().validate(data=data, schema=APP_CONFIG_SCHEMA)

    @staticmethod
    def _build_config(data: dict):
        """
            Build AppConfig class
        """
        return AppConfig(
            api=ConfigModel.Api(**data.get("api")),
            template_source=ConfigModel.TemplateSource(data.get("template_source")),
            template_fs_source=ConfigModel.TemplateFsSource(**data.get("template_fs_source")),
            template_git_source=ConfigModel.TemplateGitSource(**data.get("template_git_source")),
            template_local_cache_dir=ConfigModel.TemplateLocalCacheDir(data.get("template_local_cache_dir")),
            template_engine=ConfigModel.TemplateEngine(**data.get("template_engine")),
            context_policy=ConfigModel.ContextPolicy(**data.get("context_policy")),
            logging=ConfigModel.Logging(**data.get("logging"))
        )
