"""
    Render main wrapper
"""
from typing import Mapping, Sequence, Optional

class RenderRequest:
    """
        Render input data
    """
    def __init__(
            self,
            template: str,
            context: Mapping[str, object],
            fragments: Optional[Sequence[str]] = None
    ) -> None:
        self.template = template
        self.context = context
        self.fragments = fragments

class RenderResult:
    """
        Render output data
    """
    def __init__(self, content: str) -> None:
        self.content = content

class Render:
    """
        Render pipeline class
    """
    def __init__(
            self,
            context_processor,
            fragment_checker,
            loader,
            template_engine,

    ) -> None:
        self._context_processor = context_processor
        self._fragment_checker = fragment_checker
        self._loader = loader
        self._template_engine = template_engine

    def render(self, request: RenderRequest) -> RenderResult:
        """
            Pipeline method for rendering template
        """
        pass