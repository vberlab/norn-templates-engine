"""
    Templates loader
"""
from abc import ABC, abstractmethod
from pathlib import PurePosixPath
from typing import Optional, Iterable, Mapping, Sequence

from norn_templates_engine.template_source.index.base import RepositoryIndexer
from norn_templates_engine.template_source.index.base import RepositoryIndex
from norn_templates_engine.template_source.index.base import TemplateHandle
from norn_templates_engine.template_source.index.base import FragmentHandle
from norn_templates_engine.template_source.source.base import TemplateSource


class LoadedTemplate:
    """
        Loaded template object and fragments(optional)
    """

    def __init__(
            self,
            entrypoint: PurePosixPath,
            templates_map: Mapping[str, str],
            selected_fragments: Mapping[str, str],
    ) -> None:
        """
            Loaded:
            - template endtrypoint
            - user defined fragments
            - include parts
            - context
        """
        self.entrypoint = entrypoint
        self.templates_map = templates_map
        self.selected_fragents = selected_fragments


class TemplateLoader:
    """
        Load entrypoint and permit user defined fragments
        to in-memory snapshot
    """

    def load(
            self,
            template_name: str,
            fragment_name: Sequence[str] | None = None
    ) -> LoadedTemplate:
        pass
