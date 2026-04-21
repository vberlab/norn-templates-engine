"""
    Context processor functions
"""
from typing import Mapping

class ContextPolicy:
    """
        Context validation rules
    """
    def __init__(self, policy: Mapping[str, object]) -> None:
        self.policy = policy

    def apply_defaults(self, context: Mapping[str, object]) -> Mapping[str, object]:
        pass


    def validate(self, context: Mapping[str, object]) -> None:
        pass

class ContextProcessor:
    """
        Check passed context for policy allowed
    """
    def process(self, context: Mapping[str, object], policy: ContextPolicy) -> dict[str, object]:
        """
            Return normalize context
        """
        pass
    