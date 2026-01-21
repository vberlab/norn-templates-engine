import pytest
from norn_templates_engine.loader.filesystem import TemplatesFilesystemLoader
from norn_templates_engine.loader import errors


def test_fs_loader_loads_template_pack(template_repo_abs_path):
    loader = TemplatesFilesystemLoader(templates_repo_root=template_repo_abs_path, lazy=True)
    pack = loader.get_template("common_site")

    assert pack.name == "common_site"
    assert pack.content is not None and len(pack.content) > 0
    assert isinstance(pack.includes, dict)
    assert len(pack.includes) >= 1


def test_fs_loader_missing_template_raises(template_repo_abs_path):
    loader = TemplatesFilesystemLoader(templates_repo_root=template_repo_abs_path, lazy=True)
    with pytest.raises(errors.TemplateNotFoundError):
        loader.get_template("no_such_template")
