"""
    Class and functions for Template Pack object
"""
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Template:
    name: str                   # Template object name
    content: str                # Data from .content file
    policy: str                 # Data from .policy file

@dataclass(frozen=True)
class IncludePart:
    name: str                   # Name of include part
    data: str                   # Data from include file

@dataclass(frozen=True)
class TemplatePack:
    template: Template          # Template object
    include: list[IncludePart]  # Include part objects list