"""
    Build and runtime index errors
"""
from norn_templates_engine.loader.errors import LoaderError

class TemplatesIndexError(LoaderError):
    """
        Base templates index error
    """
    PREFIX = "INDEX"
    code = "INDEX_ERROR"

class TemplatesIndexInvalidType(TemplatesIndexError):
    """
        Index field value has invalid type
    """
    MESSAGE_TEMPLATE = "{name} value has invalid type {actual}, expected {expected}"
    code = "INDEX_FILED_VALUE_INVALID_TYPE"

    def __init__(self, *, name: str, actual: type, expected: type|tuple[type,...]):
        msg = self.MESSAGE_TEMPLATE.format(
            name=name,
            actual=actual,
            expected=expected
        )
        super().__init__(msg)

class TemplateIndexValidationError(TemplatesIndexError):
    """
        If index validation has errors
    """
    code = "INDEX_VALIDATION_ERROR"
    def __init__(self, errors: list|tuple, *args):
        self.collected_errors = errors
        super().__init__(args)

class TemplatesIndexBuildError(TemplatesIndexError):
    """
        Base template index build process error
    """
    PREFIX = "BUILD"
    code = "INDEX_BUILD_ERROR"

class TemplateIndexBuildFileNotFound(TemplatesIndexError):
    """
        Passed file not found when build process run
    """
    code = "INDEX_BUILD_FILE_NOT_FOUND"