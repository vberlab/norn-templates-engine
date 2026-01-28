"""
    Base dataclass for templates index
"""
from dataclasses import dataclass, field
from norn_templates_engine.loader.indexer import errors
from norn_templates_engine.loader.indexer import helpers

@dataclass(frozen=True)
class TemplatesIndex:
    _templates: list[str]  # templates list as full path from root
    _template_service_types: list[str]  # Template service type e.g nginx, haproxy, iptables etc
    _include_parts: list[str]  # Include parts by service type
    _templates_content: dict[str, str]  # Templates content files dictionary
    _templates_policy: dict[str, str]  # Templates policy files dictionary
    _templates_by_service_index: dict[str, list[str]]
    _include_parts_by_service_index: dict[str, list[str]]
    _root: str = None  # Template repository root

    @property
    def templates(self):
        return self._templates

    def _validate_templates(self):
        return helpers.validate_list_of_str(self.templates, "templates")
    @property
    def templates_service_types(self):
        return self._template_service_types
    def _validate_template_service_types(self, value):
        return helpers.validate_list_of_str(self.templates_service_types, "templates service types")
    @property
    def include_parts(self):
        return self._include_parts
    def _validate_include_parts(self, value):
        return helpers.validate_list_of_str(self.include_parts, "include parts")
    @property
    def templates_content(self):
        return self._templates_content
    def _validate_templates_content(self):
        return helpers.validate_dict(
            self.templates_content,
            "templates content",
            str,
            str
        )
    @property
    def templates_policy(self):
        return self._templates_policy
    def _validate_templates_policy(self):
        return helpers.validate_dict(
            self.templates_policy,
            "templates policy",
            str,
            str
        )
    @property
    def template_by_service_index(self):
        return self._templates_by_service_index
    def _validate_templates_by_service_index(self):
        status, validation_errors = helpers.validate_dict(
            self.template_by_service_index,
            "templates_by_service_index",
            str,
            list
        )
        if not status:
            return status, validation_errors
        validation_errors = list(validation_errors)
        for key, val in self.template_by_service_index.items():
            status, _errors = helpers.validate_list_of_str(val)
            if not status:
                validation_errors += _errors
        if validation_errors:
            status = False
        return status, validation_errors

    @property
    def include_parts_by_service_index(self):
        return self._include_parts_by_service_index

    def _validate_include_parts_by_service_index(self):
        status, validation_errors = helpers.validate_dict(
            self.include_parts_by_service_index,
            "include parts by service index",
            str,
            list
        )
        if not status:
            return status, validation_errors
        validation_errors = list(validation_errors)
        for key, val in self.include_parts_by_service_index.items():
            status, _errors = helpers.validate_list_of_str(val)
            if not status:
                validation_errors += _errors
        if validation_errors:
            status = False
        return status, validation_errors

    @property
    def root(self):
        return self._root

    def __post_init__(self):
        # Validate Index fields
        _errors = list()
        _validate_order = [
            self._validate_template_service_types,
            self._validate_templates,
            self._validate_templates_content,
            self._validate_templates_policy,
            self._validate_include_parts,
            self._validate_templates_by_service_index,
            self._validate_include_parts_by_service_index
        ]
        for validate_method in _validate_order:
            _, validation_errors = validate_method()
            _errors += validation_errors

        if _errors:
            raise errors.TemplateIndexValidationError(errors=_errors)
        
