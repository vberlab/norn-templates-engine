"""
    Test filesystem index builder
"""
from pathlib import Path
from norn_templates_engine.loader.indexer.builders.fsbuilder import FileSystemIndexBuilder

def test_fs_index_builder_builds_index(template_repo_abs_path):
    b = FileSystemIndexBuilder(root=template_repo_abs_path)
    b.build_index()
    index = b.index
    # assert
    for path in index.templates:
        assert Path(path).exists()
    for path in index.include_parts:
        assert Path(path).exists()
    assert isinstance(index.template_by_service_index, dict)
    assert isinstance(index.include_parts_by_service_index, dict)

