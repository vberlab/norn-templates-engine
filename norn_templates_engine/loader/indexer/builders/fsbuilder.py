"""
    Classes and functions for build index from local filesystem
"""
import re
from pathlib import Path
from norn_templates_engine.loader.indexer import errors
from norn_templates_engine.loader.indexer.index import TemplatesIndex
from norn_templates_engine.loader.indexer.builders.base import BaseIndexBuilder


class FileSystemIndexBuilder(BaseIndexBuilder):
    """
        Build templates repository index
        from local filesystem
    """

    def __init__(self, root: str):
        super().__init__(root)

    @staticmethod
    def search_file(file_name: str, path: Path) -> tuple[str, str]:
        """
            Search file in passed path
        """
        _files = [(item.name, item.absolute().as_posix()) for item in path.iterdir() if item.is_file()]
        for _name, _abs in _files:
            if re.match(file_name, _name) is not None:
                absolute_path = _abs
                break
        else:
            raise errors.TemplateIndexBuildFileNotFound(f"{file_name} not found in {path.absolute().as_posix()}")
        return file_name, absolute_path

    def _search_policy(self, path: Path) -> tuple[str, str]:
        """
            Search policy file
        """
        return self.search_file(file_name=r"*.policy", path=path)

    def _search_content(self, path: Path) -> tuple[str, str]:
        """
            Search content file
        """
        return self.search_file(file_name=r"*.content", path=path)
    @staticmethod
    def search_dir(dir_name: str, path: Path) -> tuple[str, str]:
        """
            Search directory in passed path
        """
        _dirs = [(item.name, item.absolute().as_posix() for item in path.iterdir() if item.is_dir())]
        for _name, _abs in _dirs:
            if re.match(dir_name, _name) is not None:
                absolute_path = _abs
                break
        else:
            raise errors.TemplateIndexBuildFileNotFound(f"{dir_name} not found in {path.absolute().as_posix()}")
        return dir_name, absolute_path

    def _search_include(self, path: Path) -> tuple[str, str]:
        """
            Search include path folder
        """
        return self.search_dir(dir_name="include", path=path)

    @staticmethod
    def fetch_files(path: Path, mask: str = None) -> tuple[tuple[str, str], ...]:
        """
            Fetch files from path.
            Filter by mask if present
        """
        files = [(item.name, item.absolute().as_posix()) for item in path.iterdir() if item.is_file()]
        if mask is not None:
            files = [item for item in files if re.match(mask, item[0]) is not None]
        return tuple(files)

    @staticmethod
    def fetch_dirs(path: Path, mask: str = None) -> tuple[tuple[str, str], ...]:
        """
            Fetch dirs from path.
            Filter by mask if present
        """
        dirs = [(item.name, item.absolute().as_posix()) for item in path.iterdir() if item.is_dir()]
        if mask is not None:
            dirs = [item for item in dirs if re.match(mask, item[0]) is not None]
        return tuple(dirs)

    def _fetch_raw_index_template(self, template_name: str, path: Path) -> (dict, tuple):
        """
            Wrapper method for indexing template folder.
            Search includes, content and policy files
        """
        # Search content file
        content = None
        try:
            content = self._search_content(path=path)
        except errors.TemplateIndexBuildFileNotFound as e:
            raise errors.TemplateIndexBuildFileNotFound(
                f"Invalid template {template_name}, missing content file"
            ) from e
        except Exception as e:
            raise errors.TemplatesIndexBuildError(
                f"Unhandled error occurred when search template {template_name} content file") from e
        # Search policy file
        policy = None
        try:
            policy = self._search_policy(path=path)
        except errors.TemplateIndexBuildFileNotFound as e:
            pass
            #TODO: Log missing policy error, when logging will be ready
        except Exception as e:
            raise errors.TemplatesIndexBuildError(
                f"Unhandled error occurred when search template {template_name} content file"
            ) from e
        includes = None
        try:
            includes = self._search_include(path=path)
        except errors.TemplateIndexBuildFileNotFound:
            pass
        except Exception as e:
            raise errors.TemplatesIndexBuildError(
                f"Unhandled error occurred when search include parts forlder for template {template_name}"
            ) from e
        return {
            template_name: {
                "content": content,
                "policy": policy,
                "include": includes
            }
        }

    def _fetch_raw_index_service(self, service_name: str, path: Path) -> dict:
        """
            Wrapper method for indexing service folder
            Search includes, templates, policy for service
        """
        service_index = {
            "templates": dict(),
            "include": list(),
            "policy": None
        }
        _template_dirs = self.fetch_dirs(path=path, mask=r'^(?!\s*include\s*$).+')  # Fetch all dirs except include
        _include_dir = self._search_include(path=path)
        try:
            service_index[service_name]["policy"] = self._search_policy()
        except errors.TemplateIndexBuildFileNotFound as e:
            raise errors.TemplateIndexBuildFileNotFound(
                f"Missing policy file for service {service_name}, service must have a policy"
            ) from e

        for _name, _path in _template_dirs:
            service_index["templates"].update(self._fetch_raw_index_template(_name, Path(_path)))
        _, _include_path = _include_dir
        service_index["include"] = [path for _, path in self.fetch_files(Path(_include_path))]
        return {
            service_name: service_index
        }

    def _build_raw_index(self):
        """
            Build raw index of template repository
        """
        self.raw_index = dict()
        for _srv ,_path_object in self.fetch_dirs(path=(Path(self.root)/"templates")):
            self.raw_index.update(
                self._fetch_raw_index_service(_srv, Path(_path_object))
            )

    def fetch_templates_service_types(self) -> list[str]:
        """
            Fetch service types from raw index
        """
        return list(self.raw_index.keys())

    def fetch_templates(self) -> list[str]:
        """
            Fetch templates from raw index
        """
        templates = list()
        for srv_index in self.raw_index.values():
            templates += list(srv_index["templates"].keys())
        return templates

    def build_templates_by_service_index(self) -> dict[str, list[str]]:
        templates_by_service = dict()
        for srv, index in self.raw_index.items():
            templates = list(index["templates"].keys())
            templates_by_service.update(
                {srv: templates}
            )
        return templates_by_service

    def fetch_include_parts(self) -> list[str]:
        """
            Fetch include part from raw index
        """
        include_parts = list()
        for srv_index in self.raw_index.values():
            if srv_index["include"]:
                include_parts += srv_index["include"]
            for tmpl_index in srv_index["templates"].values():
                if tmpl_index["include"]:
                    include_parts += tmpl_index["include"]
        return include_parts

    def build_include_parts_by_service_index(self) -> dict[str, list[str]]:
        include_parts_by_service = dict()
        for srv, index in self.raw_index.items():
            include_parts_by_service[srv] = list()
            if index["include"]:
                include_parts_by_service[srv] += index["include"]
            for tmpl_index in index["templates"].values():
                if tmpl_index["include"]:
                    include_parts_by_service[srv] += tmpl_index["include"]
        return include_parts_by_service

    def fetch_templates_content(self) -> dict[str, str]:
        """
            Fetch template content from raw index
        """
        templates_content = dict()
        for srv_index in self.raw_index.values():
            for name, values in srv_index["templates"].items():
                templates_content.update({name: values["content"]})
        return templates_content

    def fetch_templates_policy(self) -> dict[str, str]:
        """
            Fetch template policy from raw index.
            If policy file missing set service policy
        """
        templates_policy = dict()
        for srv_index in self.raw_index.values():
            srv_policy = srv_index["policy"]
            for name, values in srv_index["templates"].items():
                policy = values.get("policy")
                if policy is None:
                    policy = srv_policy
                templates_policy.update({name: policy})
        return templates_policy
