"""
    Manifest rules for index build
"""
from typing import Sequence

class RepoManifest:
    def __init__(self, manifest_text: str) -> None:
        self._template_roots = None
        self._fragments_roots = None
        self._include_parts = None
        self._allowed_extensions = None
        self.manifest_text = manifest_text

    def _extract_templates_roots(self) -> None:
        raise NotImplementedError

    def _extract_fragments_roots(self) -> None:
        raise NotImplementedError

    def _extract_allowed_extensions(self) -> None:
        raise NotImplementedError

    def _extract_include_parts(self) -> None:
        raise NotImplementedError

    @property
    def template_roots(self) -> Sequence[str]:
        return self._template_roots

    @property
    def fragments_roots(self) -> Sequence[str]:
        return self._fragments_roots

    @property
    def include_parts(self) -> Sequence[str]:
        return self._include_parts

    @property
    def allowed_extensions(self) -> Sequence[str]:
        return self._allowed_extensions