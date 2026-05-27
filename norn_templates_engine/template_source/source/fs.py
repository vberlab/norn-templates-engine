"""
    Filesystem source implementation
"""

from pathlib import PurePosixPath, Path
from typing import Iterable

from norn_templates_engine.template_source.source.base import TemplateSource
from norn_templates_engine.template_source.errors import TemplateSourceError


class FsSource(TemplateSource):

    def __init__(self, root: str = ".") -> None:
        if Path(root).exists():
            super().__init__(root)
        else:
            raise TemplateSourceError(f"Path [{root}] passed as root does not exist")

    def exists(self, path: str) -> bool:
        _path = Path(self.root, path)
        return _path.exists()

    def read_text(self, path: str) -> str:
        if not self.exists(path):
            raise TemplateSourceError(
                f"Path [{path}] does not exist.")
        if not self.is_file(path):
            raise TemplateSourceError(f"Path [{path}] is not a file")
        _path = Path(self.root, path)
        try:
            # TODO: encoding ?
            with open(_path, 'r', encoding="utf-8") as _file:
                return _file.read()
        except OSError as err:
            raise TemplateSourceError(f"Cannot read file: [{_path}]") from err

    def iter_files(self, root: str = ".", max_depth: int = 0) -> Iterable[PurePosixPath]:
        """
            Iterate over files in a directory. 
            Use max_depth = -1 for infinite subdirectory depth
        """
        if not self.exists(root) or not self.is_dir(root):
            raise TemplateSourceError(
                f"Path [{root}] is not a directory or does not exist")
        _max_depth = -1 if max_depth < -1 else max_depth
        for _current in Path(self.root, root).iterdir():
            _str_current = str(_current)
            if self.is_dir(_str_current) and (_max_depth > 0 or _max_depth == -1):
                yield from self.iter_files(_str_current, _max_depth-1)
            elif self.is_file(_current):
                yield PurePosixPath(_current)

    def is_dir(self, path: str) -> bool:
        _path = Path(self.root, path)
        if not self.exists(_path):
            raise TemplateSourceError(f"Path [{_path}] does not exist.")
        return _path.is_dir()

    def is_file(self, path: str) -> bool:
        _path = Path(self.root, path)
        if not self.exists(_path):
            raise TemplateSourceError(f"Path [{_path}] does not exist.")
        return _path.is_file()

