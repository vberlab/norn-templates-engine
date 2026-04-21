"""
    Render errors
"""
from norn_templates_engine.errors import NornTemplateError

class RenderError(NornTemplateError):
    pass

class ContextProcessorError(RenderError):
    pass

class FragmentCheckError(RenderError):
    pass
