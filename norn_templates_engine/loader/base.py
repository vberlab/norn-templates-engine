"""
    Basic classes for loading templates
"""
import yaml
from dataclasses import dataclass, field, asdict
from abc import ABC, abstractmethod
from typing import Mapping
from norn_templates_engine.loader import errors

@dataclass(frozen=True, kw_only=True)
class TemplatesRepoIndex:
    root: str
    template_names: tuple[str] = field(default_factory=list)
    template_content: dict[str, str] = field(default_factory=dict)
    template_includes: dict[str, list[str]] = field(default_factory=dict)

    def exists(self, template_name: str) -> bool:
        """
            Check if template exists.
        """
        return template_name in self.template_names

    def content_path(self, template_name: str, full_path: bool = False) -> str:
        """
            Return template content file path
        :param full_path: return full fs path if True, else return path regarding repo root
        """
        if not self.exists(template_name):
            raise errors.TemplateNotFoundError(f"Template {template_name} does not exists")
        path = f"{template_name}/{self.template_content[template_name]}"
        if full_path:
            path = f"{self.root}/{path}"
        return path

    def includes_path(self, template_name: str, full_path: bool = False) -> tuple or None:
        """
            Return template includes parts files path.
            If template has no includes, return None
        :param full_path: return full fs path if True, else return path regarding repo root
        """
        if not self.exists(template_name):
            raise errors.TemplateNotFoundError(f"Template {template_name} does not exists")
        if not self.template_includes[template_name]:
            return
        paths = (f"{template_name}/includes/{include_part}"for include_part in self.template_includes[template_name])
        if full_path:
            paths = (f"{self.root}/{include_item_path}" for include_item_path in paths )
        return paths

    def to_dict(self):
        return asdict(self)

class TemplateRepoIndexBuilder(ABC):
    """
        Abstract template repo index builder class
    """
    _root: str
    _errors: dict

    @property
    def root(self):
        return self._root

    @property
    def errors(self):
        return self._errors

    @abstractmethod
    def index_names(self):
        """
            Search and index templates names
        """
        pass

    @abstractmethod
    def index_content(self):
        """
            Index content paths
        """
        pass

    @abstractmethod
    def index_includes(self):
        """
            Search and index includes parts
        """
        pass

    def build_index(self) -> TemplatesRepoIndex:
        """
            Create index class object
        """
        return TemplatesRepoIndex(
            root=self.root,
            template_names=self.index_names(),
            template_content=self.index_content(),
            template_includes=self.index_includes()
        )

@dataclass(frozen=True)
class TemplatePack:
    """
        Self-contained template set.
    """
    name: str           # template name. e.g "example.conf.j2"
    path: str           # template path e.g "/templates/example.conf"
    content: str        # template text file content
    includes: Mapping[str, str]     # template file includes parts, relpath -> file content

@dataclass
class TemplateRepoCache:
    template_packs: dict = field(default_factory=dict)
    template_names: list = field(default_factory=list)

    def add(self, new_template: TemplatePack):
        """
            Add template to cache
        """
        if new_template.name in self.template_names:
            raise errors.TemplateCachheExists(f"{new_template.name} existing in cache")
        self.template_names.append(new_template.name)
        self.template_packs[new_template.name] = new_template

    def update(self, new_template: TemplatePack):
        """
            Update template record in cache
        """
        if new_template.name not in self.template_names:
            self.add(new_template=new_template)
        self.template_packs[new_template.name] = new_template

    def clear(self):
        """
            Clear cache
        """
        self.template_names = list()
        self.template_packs = dict()

class TemplateLoader(ABC):
    """
        Abstract template loader class.
        :param index_save_path: Path for template index save
        :param lazy: if True loads template on request, else loads all templates on init
    """
    _index: TemplatesRepoIndex

    def __init__(self, index_save_path: str, lazy: bool = False):
        self._index_save_path = index_save_path
        self._cache = TemplateRepoCache()
        self._lazy = lazy
        self._index = self._create_index()
        self._dump_index()

    @property
    def index_save_path(self):
        return self._index_save_path

    @property
    def lazy(self):
        return self._lazy

    @property
    def cache(self):
        return self._cache

    def cache_clear(self):
        """
            Clear self._cache
        """
        self._cache.clear()

    @abstractmethod
    def _load(self):
        """
            Load all templates and save to cache
        """
        pass

    @abstractmethod
    def _lazy_load(self, template_name: str) -> TemplatePack:
        """
            Load passed template
        save them to self._cache and return pack
        """
        pass

    def _load_from_cache(self, template_name: str) -> TemplatePack:
        """
            Load template from cache
        """
        if template_name not in self._cache.template_names:
            raise errors.TemplateNotCachedError(f"Template {template_name} not cached")
        else:
            return self.cache.template_packs[template_name]

    def get_template(self, template_name: str) -> TemplatePack:
        """
            Return template pack from cache or load them
        """
        try:
            template = self._load_from_cache(template_name)
        except errors.TemplateNotCachedError:
            template = self._lazy_load(template_name)
        except Exception as _err:
            raise errors.LoaderError(f"Loader unhandled error occurred, when getting template {template_name}") from _err
        return template

    @abstractmethod
    def exists(self, template_name: str) -> bool:
        """
            Check existing passed template in index.
        """

    @abstractmethod
    def _create_index(self) -> TemplatesRepoIndex:
        """
            Create index file from template repository
        """
        pass

    @property
    def index(self) -> TemplatesRepoIndex:
        """
            Templates index
        """
        return self._index

    def _dump_index(self) -> None:
        """
            Dump templates index database to path
        """
        try:
            with open(self._index_save_path, "w") as _fd:
                yaml.safe_dump(self.index.to_dict())
        except Exception as _err:
            raise errors.LoaderError(f"Loader unhandled error occurred, when dump templates repo index") from _err
        return