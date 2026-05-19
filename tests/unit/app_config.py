"""
    Unit test for ConfigLoader
"""
from pathlib import Path
import pytest
from norn_templates_engine.config import AppConfig
from norn_templates_engine.config.loader import ConfigLoader
from norn_templates_engine.config import errors

TEST_CONFIG_DIR = Path(__file__).parent / "data/app_config"
VALID_CONFIG = TEST_CONFIG_DIR / "valid.yaml"
INVALID_YAML_CONFIG = TEST_CONFIG_DIR / "invalid.yaml"
EMPTY_CONFIG = TEST_CONFIG_DIR / "empty.yaml"

@pytest.fixture
def loader() -> ConfigLoader:
    return ConfigLoader()

def test_load_returns_app_config(loader: ConfigLoader):
    config = loader.load(path=VALID_CONFIG)
    assert isinstance(config, AppConfig)

def test_load_accepts_str_path(loader: ConfigLoader):
    str_path = str(VALID_CONFIG)
    config = loader.load(path=str_path)
    assert isinstance(config, AppConfig)

def test_load_raises_config_not_found_for_missing_file(loader: ConfigLoader):
    missing_config_path = TEST_CONFIG_DIR / "missing.yaml"
    with pytest.raises(errors.ConfigNotFoundError):
        loader.load(path=missing_config_path)

def test_load_raises_config_parse_error_for_invalid_yaml(loader: ConfigLoader):
    with pytest.raises(errors.ConfigParseError):
        loader.load(INVALID_YAML_CONFIG)

def test_load_raises_config_empty_for_empty_yaml(loader: ConfigLoader):
    with pytest.raises(errors.ConfigEmpty):
        loader.load(EMPTY_CONFIG)


