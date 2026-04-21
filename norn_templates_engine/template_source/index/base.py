"""
    Template repository indexer
"""
from abc import ABC, abstractmethod
from pathlib import PurePosixPath
from typing import Iterable, Mapping

from norn_templates_engine.template_source.source.base import TemplateSource
from norn_templates_engine.template_source.index import errors


class TemplateHandle:
    """
        Link to template entrypoint
    """

    def __init__(self, path: PurePosixPath) -> None:
        self.path = path


class FragmentHandle:
    """
        Link to template fragment
    """

    def __init__(self, path: PurePosixPath, template: str) -> None:
        self.path = path
        self.template = template


class RepositoryIndex:
    """
        Template repository index(immutable)
    """

    def __init__(self, templates: Mapping[str, TemplateHandle], fragments: Mapping[str, FragmentHandle]) -> None:
        self._templates = templates
        self._fragments = fragments

    @property
    def templates(self) -> Iterable[str]:
        return self._templates.keys()

    def get_template(self, name: str) -> TemplateHandle:
        if name not in self._templates.keys():
            raise errors.TemplateNotInIndexError(f"Template {name} not found in index")
        return self._templates[name]

    def get_fragment(self, name: str):
        if name not in self._fragments.keys():
            raise errors.FragmentNotInIndexError(f"Fragment {name} not found in index")

class RepositoryIndexer:
    """
        Build repository index from TemplateSource
    """
    def build(self, source: TemplateSource) -> RepositoryIndex:
        # TODO: 3) Implement index building
        pass
