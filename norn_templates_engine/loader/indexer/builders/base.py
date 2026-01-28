"""
    Base class for index builders
"""
from abc import ABC, abstractmethod
from norn_templates_engine.loader.indexer.index import TemplatesIndex

class BaseIndexBuilder(ABC):
    """
        Abstract class for building template repo index
    """

    def __init__(self, root: str = None):
        self._root = root

    @property
    def root(self) -> str or None:
        """
            templates repository root path
        """
        return self._root
    @abstractmethod
    def fetch_templates(self) -> list[str]:
        """
            Fetch index templates field
        """
        pass

    @abstractmethod
    def fetch_templates_service_types(self) -> list[str]:
        """
            Fetch index templates_service_types field
        """
        pass

    @abstractmethod
    def fetch_include_parts(self) -> list[str]:
        """
            Fetch index include_parts field
        """
        pass

    @abstractmethod
    def fetch_templates_content(self) -> dict[str, str]:
        """
            Fetch index templates_content field
        """
        pass

    @abstractmethod
    def fetch_templates_policy(self) -> dict[str, str]:
        """
            Fetch index templates_policy field
        """
        pass

    @abstractmethod
    def build_templates_by_service_index(self) -> dict[str, list[str]]:
        """
            Build templates by service index
        """
        pass

    @abstractmethod
    def build_include_parts_by_service_index(self) -> dict[str, list[str]]:
        """
            Build include parts by service index
        """
        pass

    def build_index(self):
        """
            Build index object
        """
        self._index = TemplatesIndex(
            self.fetch_templates(),
            self.fetch_templates_service_types(),
            self.fetch_include_parts(),
            self.fetch_templates_content(),
            self.fetch_templates_policy(),
            self.build_templates_by_service_index(),
            self.build_include_parts_by_service_index(),
            self.root
        )

    @property
    def index(self):
        return self._index