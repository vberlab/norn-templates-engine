"""
    Base template source ABC class
"""
from abc import ABC, abstractmethod
from pathlib import PurePosixPath
from typing import Iterable

class TemplateSource(ABC):
    """
        Abstract template source(git, fs, etc...)
        Read-only
    """
    def __init__(self, root: str = ".") -> None:
        self.root = PurePosixPath(root)

    @abstractmethod
    def exists(self, path: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def read_text(self, path: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def iter_files(self, root: str = ".") -> Iterable[PurePosixPath]:
        raise NotImplementedError

    @abstractmethod
    def is_dir(self, path: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_file(self, path: str) -> bool:
        raise NotImplementedError
