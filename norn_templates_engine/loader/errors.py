"""
    Errors for templates loaders
"""
from norn_templates_engine.errors import NornError

class LoaderError(NornError):
    """
        Base class for template loaders error
    """
    PREFIX = "LOADER"
    code = "LOADER_ERROR"

class TemplateNotCachedError(LoaderError):
    code = "TEMPLATE_NOT_CACHED"

class TemplateNotFoundError(LoaderError):
    code = "TEMPLATE_NOT_FOUND"

class TemplateContentIsNotFile(LoaderError):
    code = "TEMPLATE_CONTENT_IS_NOT_FILE"

class TemplateMissingContentFile(LoaderError):
    code = "TEMPLATE_MISSING_CONTENT_FILE"

class TemplateCacheError(LoaderError):
    """
        Base class for template cache errors
    """
    PREFIX = "CACHE"
    code = "TEMPLATE_CACHE_ERROR"

class TemplateCachheExists(TemplateCacheError):
    code = "TEMPLATE_CACHE_EXISTS"

class TemplateCacheTtlInvalidType(TemplateCacheError):
    code = "CACHE_OBJECT_TTL_VALUE_INVALID_TYPE"

class TemplateCacheObjectInvalidType(TemplateCacheError):
    code = "CACHE_OBJECT_INVALID_TYPE"

class TemplateCacheUpdateObjectError(TemplateCacheError):
    code = "CACHE_OBJECT_UPDATE_ERROR"

class TemplateCacheAddObjectError(TemplateCacheError):
    code = "CACHE_OBJECT_ADD_ERROR"