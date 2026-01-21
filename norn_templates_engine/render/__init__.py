"""
    Basic classes for rendering
"""
from typing import Protocol, Any, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum

class Engine(str, Enum):
    NGINX = "nginx"

@dataclass(frozen=True)
class TemplateRenderResult:
    complite_text: str
    normalize_text: str

class TemplateRender(Protocol):
    """
        Pure render interface
    """
    engine: Engine
    def render(self, tpack: TemplatePack, tcontext: Mapping[str, Any]) -> TemplateRenderResult:
        pass