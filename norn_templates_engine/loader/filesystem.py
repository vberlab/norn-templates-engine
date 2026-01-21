"""
    Template loader from file system functions and classes
"""
from pathlib import Path
from norn_templates_engine.loader.base import TemplateLoader
from norn_templates_engine.loader.base import TemplatePack
from norn_templates_engine.loader.base import TemplateRepoIndexBuilder
from norn_templates_engine.loader.base import TemplateRepoCache
from norn_templates_engine.loader import errors

class TemplateFsRepoIndexBuilder(TemplateRepoIndexBuilder):
    """
        Template repository indexer from filesystem
    """
    def __init__(self, root: str):
        self._root = root
        super().__init__()
        self.root_paths = Path(self.root)
        self.raw_index = {item.name: {"path_obj": item} for item in self.root_paths.iterdir() if item.is_dir()}
        self._errors = {template: list() for template in self.raw_index.keys()}


    def index_content(self):
        """
            Search and index template content file in templates repository
        """
        for name, data in self.raw_index.items():
            path_object = data["path_object"]
            for item in path_object.iterdir():
                if item.name.split(".")[-1] == "content":
                    if item.is_file():
                        self.raw_index[name].update({"content": item.name})
                        break
                    else:
                        self._errors[name].append(errors.TemplateContentIsNotFile())
            else:
                self._errors[name].append(errors.TemplateMissingContentFile())
        return {name: data["content"] for name, data in self.raw_index.items()}

    def index_includes(self):
        """
            Index includes parts of templates
        """
        for name, data in self.raw_index.items():
            if self.errors[name]: continue
            path_object = data["path_object"]
            if "includes" not in [item.name for item in path_object.iterdir()]:
                self.raw_index[name].update({"includes": None})
                continue
            else:
                self.raw_index[name].update({
                    "includes": [item.name for item in Path(f"{path_object.absolute()}/includes").iterdir() if item.is_file()]
                })
        return {name: data["includes"] for name, data in self.raw_index.items()}

    def index_names(self):
        """
            Index template names without errors
        """
        return (item for item in self.raw_index.keys() if not self.errors[item])



class TemplatesFilesystemLoader(TemplateLoader):
    """
        Class for loading template from local filesystem
    :param templates_repo_root: root path to templates repository
    :param index_save_path: path to file where templates index will be saved
    :param lazy: if True loads template on request, else loads all templates on init
    """
    def __init__(self, templates_repo_root: str, index_save_path: str, lazy: bool = False):
        self._templates_repo_root = templates_repo_root
        super().__init__(index_save_path=index_save_path, lazy=lazy)
        self._index = self._create_index()
        if not self.lazy:
            self._load()

    @property
    def templates_repo_root(self):
        return self._templates_repo_root

    def _create_index(self):
        """
            Create index file from template repository
        """
        return TemplateFsRepoIndexBuilder(root=self.templates_repo_root).build_index()

    def _lazy_load(self, template_name: str) -> TemplatePack:
        """
            Load passed template from filesystem
        """
        if not self.index.exists(template_name):
            raise errors.TemplateNotFoundError(f"Template {template_name} does not exists in index")
        _name = template_name
        _path = self.index.template_content[_name]
        _content = None
        _includes = dict()
        try:
            with open(_path, "r") as _fd:
                _content = _fd.read()
        except Exception as _err:
            raise errors.LoaderError(f"Loader unhandled error occurred when read {template_name} content") from _err
        try:
            for include in self.index.template_includes[_name]:
                with open(include, "r") as _fd:
                    _includes[include] = _fd.read()
        except Exception as _err:
            raise errors.LoaderError(f"Loader unhandled error occurred when read include path {include} of {template_name}") from _err
        return TemplatePack(
            name=_name,
            path=_path,
            content=_content,
            includes=_includes
        )

    def _load(self):
        """
            Load all templates from filesystem and save to cache
        """
        for template in self.index.template_names:
            try:
                self.cache.add(new_template=self._lazy_load(template_name=template))
            except Exception as _err:
                raise errors.LoaderError(f"Loading {template} error") from _err
        return




