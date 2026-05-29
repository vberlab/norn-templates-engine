import py
import shutil
import pytest

from pathlib import Path, PurePosixPath

from norn_templates_engine.template_source.source.fs import FsSource
from norn_templates_engine.template_source.errors import TemplateSourceError


TEST_FS_TEMPLATE_SOURCE_DIR = "fs_template_source"
WITH_CONTENT = "with_content"
DIR_1 = "dir_1"
DIR_2 = "dir_2"
DIR_3 = "dir_3"
FILE_0 = "file_0"
FILE_1 = "file_1"
WRONG_PATH = "wrong_path"
FILE_WITH_CONTENT = PurePosixPath(WITH_CONTENT)

FLAT = [
    PurePosixPath(FILE_WITH_CONTENT),
]

FILES_LEVEL_1 = [
    PurePosixPath(DIR_1, FILE_0),
    PurePosixPath(DIR_1, FILE_1),
]

FILES_LEVEL_2 = [
    PurePosixPath(DIR_1, DIR_2, FILE_0),
    PurePosixPath(DIR_1, DIR_2, FILE_1),
]

FILES_LEVEL_3 = [
    PurePosixPath(DIR_1, DIR_2, DIR_3, FILE_0),
    PurePosixPath(DIR_1, DIR_2, DIR_3, FILE_1),
]

SUBDIRS = FILES_LEVEL_1 + FILES_LEVEL_2 + FILES_LEVEL_3

ALL_FILES = SUBDIRS + FLAT


def raise_os_error(*args, **kwargs):
    raise OSError("Forced OSError")


@pytest.fixture(scope="session")
def fs_template_dir(tmpdir_factory: pytest.TempdirFactory):
    root_dir: py.path.LocalPath = tmpdir_factory.mktemp(
        TEST_FS_TEMPLATE_SOURCE_DIR)
    for _file in SUBDIRS:
        root_dir.ensure(str(_file))
    root_dir.join(FILE_WITH_CONTENT).write(FILE_WITH_CONTENT)
    yield root_dir
    shutil.rmtree(str(root_dir))


@pytest.fixture
def source(fs_template_dir) -> FsSource:
    return FsSource(str(fs_template_dir))

# .init
def test_fs_source_init():
    with pytest.raises(TemplateSourceError):
        FsSource(WRONG_PATH)


# .exists
def test_existing_file(source: FsSource):
    assert source.exists(str(FILE_WITH_CONTENT))


def test_non_existing_file(source: FsSource):
    assert not source.exists(str(WRONG_PATH))


# .is_dir
def test_failing_dir_type_check(source: FsSource):
    assert not source.is_dir(str(FILE_WITH_CONTENT))


def test_successful_dir_type_check(source: FsSource):
    assert source.is_dir(str(DIR_1))


def test_non_existing_dir_type_check_raises_error(source: FsSource):
    with pytest.raises(TemplateSourceError):
        source.is_dir(str(WRONG_PATH))


# .is_file
def test_failing_file_type_check(source: FsSource):
    assert not source.is_file(str(DIR_1))


def test_successful_file_type_check(source: FsSource):
    assert source.is_file(str(FILE_WITH_CONTENT))


def test_non_existing_file_type_check_raises_error(source: FsSource):
    with pytest.raises(TemplateSourceError):
        source.is_file(str(WRONG_PATH))


# .read_text
def test_non_existing_file_reading_raises_error(source: FsSource):
    with pytest.raises(TemplateSourceError):
        source.read_text(str(WRONG_PATH))


def test_trying_to_read_not_a_file_raises_error(source: FsSource):
    with pytest.raises(TemplateSourceError):
        source.read_text(str(DIR_1))


def test_failed_file_reading_raises_custom_error(source: FsSource, monkeypatch):
    monkeypatch.setitem(__builtins__, "open", raise_os_error)
    with pytest.raises(TemplateSourceError):
        source.read_text(str(WITH_CONTENT))


def test_read_file(source: FsSource):
    assert source.read_text(str(WITH_CONTENT)) == WITH_CONTENT


# .iter_files
def test_non_existing_path_iteration_raises_error(source: FsSource):
    with pytest.raises(TemplateSourceError):
        list(source.iter_files(str(WRONG_PATH)))


def test_iterating_not_a_directory_raises_error(source: FsSource):
    with pytest.raises(TemplateSourceError):
        list(source.iter_files(str(WITH_CONTENT)))


def test_iter_files_from_root_max_depth_0(source: FsSource, fs_template_dir: py.path.LocalPath):
    files = list(source.iter_files(max_depth=0))
    assert len(files) == len(FLAT)
    for file in FLAT:
        assert PurePosixPath(file) in files


def test_iter_files_from_root_max_depth_1(source: FsSource, fs_template_dir: py.path.LocalPath):
    files = list(source.iter_files(max_depth=1))
    assert len(files) == len(FLAT + FILES_LEVEL_1)
    for file in FLAT + FILES_LEVEL_1:
        assert PurePosixPath(file) in files


def test_iter_files_from_root_max_depth_infinite(source: FsSource, fs_template_dir: py.path.LocalPath):
    files = list(source.iter_files(max_depth=-1))
    assert len(files) == len(ALL_FILES)
    for file in ALL_FILES:
        assert PurePosixPath(file) in files


def test_iter_files_from_root_max_depth_too_small(source: FsSource, fs_template_dir: py.path.LocalPath):
    files = list(source.iter_files(max_depth=-5))
    assert len(files) == len(ALL_FILES)
    for file in ALL_FILES:
        assert PurePosixPath(file) in files


def test_iter_files_from_root_max_depth_too_big(source: FsSource, fs_template_dir: py.path.LocalPath):
    files = list(source.iter_files(max_depth=5))
    assert len(files) == len(ALL_FILES)
    for file in ALL_FILES:
        assert PurePosixPath(file) in files


def test_iter_files_from_subdirectory_max_depth_0(source: FsSource, fs_template_dir: py.path.LocalPath):
    files = list(source.iter_files(DIR_1))
    assert len(files) == len(FILES_LEVEL_1)
    for file in FILES_LEVEL_1:
        assert PurePosixPath(file) in files


def test_iter_files_from_subdirectory_max_depth_1(source: FsSource, fs_template_dir: py.path.LocalPath):
    files = list(source.iter_files(DIR_1, max_depth=1))
    assert len(files) == len(FILES_LEVEL_1 + FILES_LEVEL_2)
    for file in FILES_LEVEL_1 + FILES_LEVEL_2:
        assert PurePosixPath(file) in files


def test_iter_files_from_subdirectory_max_depth_infinite(source: FsSource, fs_template_dir: py.path.LocalPath):
    files = list(source.iter_files(DIR_1, max_depth=-1))
    assert len(files) == len(SUBDIRS)
    for file in SUBDIRS:
        assert PurePosixPath(file) in files


def test_iter_files_from_subdirectory_max_depth_too_small(source: FsSource, fs_template_dir: py.path.LocalPath):
    files = list(source.iter_files(DIR_1, max_depth=-5))
    assert len(files) == len(SUBDIRS)
    for file in SUBDIRS:
        assert PurePosixPath(file) in files


def test_iter_files_from_subdirectory_max_depth_too_big(source: FsSource, fs_template_dir: py.path.LocalPath):
    files = list(source.iter_files(DIR_1, max_depth=5))
    assert len(files) == len(SUBDIRS)
    for file in SUBDIRS:
        assert PurePosixPath(file) in files
