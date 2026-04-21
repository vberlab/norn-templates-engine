"""
    Template Indexer errors
"""
from norn_templates_engine.template_source.errors import TemplateSourceError

class TemplateIndexerError(TemplateSourceError):
    pass

class TemplateNotInIndexError(TemplateIndexerError):
    pass

class FragmentNotInIndexError(TemplateIndexerError):
    pass