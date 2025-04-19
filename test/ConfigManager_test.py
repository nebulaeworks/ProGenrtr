import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from os.path import expanduser
from _pytest.capture import CaptureFixture
from typing import Iterator

from ConfigManager import ConfMgr
from test.testUtils import FALLBACK_PATH, MINIMAL_FALLBACK_INI


DEFAULT_CONFIG_PATHS: list[str] = [
    (expanduser("~/.progenrtr.conf")),
    (expanduser("~/.config/progenrtr/progenrtr.conf")),
    ("/etc/progenrtr.conf")
]

MINIMAL_CONFIG: str = """
    [ProGenrtr]
    languages = test_language

    [project.test_language]
    test_project: testProject
"""


@pytest.fixture
def testSetup(fs: FakeFilesystem) -> Iterator[FakeFilesystem]:
    yield fs
    ConfMgr.reset()
def test_minimal_fallback_is_successfully_parsed(
        testSetup: Iterator[FakeFilesystem]) -> None:
    testSetup.create_file(FALLBACK_PATH, contents=MINIMAL_FALLBACK_INI)
    args = {"--config": None}
    try:
        ConfMgr().parse(args)
        assert ConfMgr().projects.test_lang.test_proj == "test"
    except Exception as e:
        pytest.fail(e)


def test_user_is_notified_of_nonexistant_fallback_ini(
        testSetup: Iterator[FakeFilesystem],
        capfd: CaptureFixture[str]) -> None:
    testSetup.create_file("/not/fallback/path", contents=MINIMAL_FALLBACK_INI)
    args = {"--config": None}
    with pytest.raises(SystemExit) as e:
        ConfMgr().parse(args)
    out, err = capfd.readouterr()
    assert "not available" and "fallback.ini" in out
    assert e.value.code > 0


@pytest.mark.parametrize("expected_path", DEFAULT_CONFIG_PATHS)
def test_minimal_config_is_parsed_from_default_locations(
        testSetup: Iterator[FakeFilesystem],
        expected_path: str) -> None:

    testSetup.create_file(FALLBACK_PATH, contents=MINIMAL_FALLBACK_INI)
    testSetup.create_file(expected_path, contents=MINIMAL_CONFIG)
    args = {"--config": None}
    ConfMgr().parse(args)

    expectedProjectName = "testProject"
    assert ConfMgr().projects.test_language.test_project == expectedProjectName
