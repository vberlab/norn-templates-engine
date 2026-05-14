from typing import Mapping, Hashable
from norn_templates_engine.config import schema
from norn_templates_engine.config import errors

class ConfigurationValidator:
    schema: schema.APP_CONFIG_SCHEMA

    def _has_key(self,key: Hashable, data: Mapping) -> bool:
        if data.get(key) is not None:
            return True
        return False

    def validate(self, data: Mapping):
        # Check required options
        for k, v in self.schema.items():
            if v["required"]:
                if not self._has_key(k, data):
                    raise errors.ConfigValidationError(f"Missing required field {k}")
        # Check types
        for k, v in self.schema.items():
            if not data[k]:
                continue
            if not isinstance(data[k], v["type"]):
                raise errors.ConfigValidationError(f"Option {k} has invalid type {type(data[k])}, a {v['type']} required")
            if isinstance(data[k], dict):
                self.validate(data=data[k])
        return
