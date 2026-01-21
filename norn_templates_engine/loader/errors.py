"""
    Errors for templates loaders
"""

class LoaderError(Exception):
    """
        Base class for template loaders error
    """
    code = "LOADER_ERROR"

class TemplateNotCachedError(LoaderError):
    code = "TEMPLATE_NOT_CACHED"

class TemplateNotFoundError(LoaderError):
    code = "TEMPLATE_NOT_FOUND"

class TemplateContentIsNotFile(LoaderError):
    code = "TEMPLATE_CONTENT_IS_NOT_FILE"

class TemplateMissingContentFile(LoaderError):
    code = "TEMPLATE_MISSING_CONTENT_FILE"

class TemplateCachheExists(LoaderError):
    code = "TEMPLATE_CACHE_EXISTS"