"""
    Classes for render errors
"""

class RenderError(Exception):
    """
        Base class for rendering template errors
    """
    code: str = "RENDER_ERROR"

class RenderFailed(RenderError):
    code = "RENDER_FAILED"

class NormalizeFailed(RenderError):
    code = "NORMALIZE_FAILED"