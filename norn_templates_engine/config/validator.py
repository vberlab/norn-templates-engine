from typing import Hashable
from norn_templates_engine.config import errors

class ConfigurationValidator:

    def _has_key(self,key: Hashable, data: dict) -> bool:
        if not isinstance(data, dict):
            return False
        if data.get(key) is not None:
            return True
        return False

    def validate(self, data: dict, schema: dict):
        # Check required options
        for k, v in schema.items():
            if self._has_key("required", v):
                if not self._has_key(k, data):
                    raise errors.ConfigValidationError(f"Missing required field [{k}]")
        # Check types
        for k, v in schema.items():
            if not data.get(k):
                continue
            if not isinstance(data[k], v["type"]):
                raise errors.ConfigValidationError(f"Option [{k}] has invalid type [{type(data[k])}], a [{v['type']}] required")
            if isinstance(data[k], dict):
                self.validate(data=data[k], schema=schema[k])
        # Check dependency required
        for k, v in schema.items():
            if isinstance(v, dict):
                if self._has_key("dependency", v):
                    for dependency in v["dependency"]:
                        if dependency in data.keys():
                            break
                    else:
                        raise errors.ConfigValidationError(f"Missing dependency option for option [{k}]")
        return
