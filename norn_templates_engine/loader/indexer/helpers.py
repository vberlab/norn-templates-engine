"""
    Helpers functions for indexer
"""
from norn_templates_engine.loader.indexer import errors

def validate_list_of_str(value, name: str) -> (bool, tuple[Exception], str):
    """
        Validate value.
        Return validate result, tuple with errors and valid items
    """
    status = False
    valid = list()
    validation_errors = list()
    if not isinstance(value, (list, tuple)):
        validation_errors.append(
            errors.TemplatesIndexInvalidType(
                name=name,
                actual=type(value),
                expected=(list, tuple)
            )
        )
    else:
        for item in value:
            if not isinstance(item, str):
                validation_errors.append(
                    errors.TemplatesIndexInvalidType(
                        name=f"{name} item",
                        actual=type(value),
                        expected=str
                    )
                )
            else:
                valid.append(item)
    if not validation_errors:
        status = True
    return status, validation_errors

def validate_dict(value, name: str, expect_key: type, expect_val: type) -> (bool, tuple[Exception], dict[str, str]):
    """
        Validate dict values types
    :param value: dictionary
    :param name: name of variable in indexer or other
    :param expect_key: key type
    :param expect_val: val type
    """
    status = False
    valid = dict()
    validation_errors = list()
    if not isinstance(value, dict):
        validation_errors.append(
            errors.TemplatesIndexInvalidType(
                name=name,
                actual=type(value),
                expected=dict
            )
        )
    else:
        for k, v in value.items():
            if isinstance(k, expect_key):
                if isinstance(v, expect_val):
                    valid[k] = v
                else:
                    validation_errors.append(
                        errors.TemplatesIndexInvalidType(
                            name=f"{name} {k} value",
                            actual=type(v),
                            expected=expect_val
                        )
                    )
            else:
                validation_errors.append(
                    errors.TemplatesIndexInvalidType(
                        name=f"{name} key",
                        actual=type(k),
                        expected=expect_key
                    )
                )
    if not validation_errors:
        status = True
    return status, validation_errors