"""
    Test filesystem index builder
"""
from norn_templates_engine.loader.filesystem import TemplateFsRepoIndexBuilder

def test_fs_index_builder_builds_index(template_repo_abs_path):
    b = TemplateFsRepoIndexBuilder(root=template_repo_abs_path)
    index = b.build_index()
    # assert
    assert "nginx/common_site" in index.template_names
    assert "nginx" in index.template_service_types
