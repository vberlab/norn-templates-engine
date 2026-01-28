"""
    App common errors classes
"""
from dataclasses import dataclass

@dataclass(frozen=True)
class ErrorConfig:
    PREFIX_SEPARATOR: str = "_"

class NornError(Exception):
    """
        Base App error
    """
    PREFIX = "NORN"
    code = "NORN_TEMPLATE_ENGINE_ERROR"

    @classmethod
    def full_traceback_prefix(cls) -> str:
        """
            Show full traceback code
        """
        _parts = list()
        for base in reversed(cls.__mro__):
            if hasattr(base, "PREFIX"):
                _parts.append(base.PREFIX)
        return ErrorConfig.PREFIX_SEPARATOR.join(_parts)