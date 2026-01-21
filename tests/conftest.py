import pytest
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class TestConfig:
    project_name: str = "norn-templates-engine"
    test_fs_templates_repo: str = "templates_repo_example"

def search_project_abs_root() -> Path:
    """
        Determinate project root(search setup.py file)
    """
    path = Path("./").absolute()
    while path.name != TestConfig.project_name:
        path = path.absolute().parent
    return path

@pytest.fixture()
def project_abs_root() -> Path:
    return search_project_abs_root()

@pytest.fixture()
def template_repo_abs_path() -> Path:
    """
        Return templates_repo_example absolute path
    """
    return search_project_abs_root().joinpath(TestConfig.test_fs_templates_repo)
