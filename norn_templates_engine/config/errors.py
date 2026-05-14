"""
    Configuration errors
"""
from norn_templates_engine.errors import NornTemplateError

class ConfigError(NornTemplateError):
    pass

class ConfigNotFoundError(ConfigError):
    pass

class ConfigParseError(ConfigError):
    pass

class ConfigLoaderError(ConfigError):
    pass

class ConfigEmpty(ConfigError):
    pass

class ConfigValidationError(ConfigError):
    pass
