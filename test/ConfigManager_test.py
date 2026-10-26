"""! @test
Usecases and edge cases for the functionality of the src.ConfigManager.ConfMgr
singleton class; which provides handling and access to fallback, and user
user defined config at both default and custom locations.

@var DEFAULT_CONFIG_PATHS
     the list of paths used by the application to search for config files
@var NON_DEFAULT_CONFIG_PATHS
     a list of non standard config paths meant to emulate what a user might
     pass on the command line, should they wish
@var MINIMAL_CONFIG
     a very minimal config defining just one language and one project within
     that language
"""
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

NON_DEFAULT_CONFIG_PATHS: list[str] = [
    (expanduser("~/some/path/to/progenrtr.conf")),
    (expanduser("~/another/path/to/config.ini")),
    ("/opt/some/config"),
    ("/var/other/conf.ig"),
    ("myConfig.txt")
]

MINIMAL_CONFIG: str = """
    [ProGenrtr]
    languages = test_language

    [project.test_language]
    test_project: testProject
"""


@pytest.fixture
def testSetup(fs: FakeFilesystem) -> Iterator[FakeFilesystem]:
    """!
    Test Fixture to do setup common to all tests; currently this:
    - resets the ConfMgr singleton to ensure repeatibility
    - passes through the fs fixture

    @param fs is a reference to a fake file system (pyfakefs fixture)
    @see
        - [pyfakefs docs](https://pytest-pyfakefs.readthedocs.io/en/stable/)
    """
    yield fs
    ConfMgr.reset()


def test_minimal_fallback_is_successfully_parsed(
        testSetup: Iterator[FakeFilesystem]) -> None:
    """!@START_SCENARIO
    a minimal fallback.ini in its default location is parsed without issues
    @GIVEN{fallback.ini exists at templates/fallback.ini}
    @WHEN{The config is parsed}
    @THEN{config is parsed}
    @AND_T{no exceptions occur}
    @END_SCENARIO

    @param testSetup fixture responsible for fake filesystem and Config setup
    @see
        - @ref testSetup
    """
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
    """! @START_SCENARIO
    The user is notified of a nonexistant fallback.ini
    @GIVEN{There is no fallback.ini in an expected place}
    @AND_G{`--config <configfile>` is not passed on the command line}
    @WHEN{The config is parsed}
    @THEN{The user is notified of this fact}
    @AND_T{Execution is returned to system with an error code}
    @END_SCENARIO

    @param testSetup fixture responsible for fake filesystem and Config setup
    @param capfd fixture for capturing stdout stderr etc
    """
    testSetup.create_file("/not/fallback/path", contents=MINIMAL_FALLBACK_INI)
    args = {"--config": None}
    with pytest.raises(SystemExit) as e:
        ConfMgr().parse(args)
    out, err = capfd.readouterr()
    assert "not available" and "fallback.ini" in out
    assert e.value.code > 0


def test_user_is_notified_of_invalid_fallback_ini(
        testSetup: Iterator[FakeFilesystem],
        capfd: CaptureFixture[str]) -> None:
    """! @START_SCENARIO
    a fallback config must contain (at a minimum) a `[META]` section containing
    a `cfgPaths` key which should contain at least one path or else user
    defined config is essentially disabled....which would be dumb
    @GIVEN{a `<project_root>/templates/fallback.ini` exists}
    @WHEN{There is **NO** `[META]` section}
    @OR_W{There is an **EMPTY** `[META]` section}
    @OR_W{There is a `[META]` section **BUT** the `cfgPaths` key is empty}
    @THEN{The user should be informed in some way}
    @END_SCENARIO
    """
    # NO [META] SECTION
    invalid_config_NO_META = ""
    testSetup.create_file(FALLBACK_PATH, contents=invalid_config_NO_META)
    args = {"--config": None}
    with pytest.raises(SystemExit) as ke:
        ConfMgr().parse(args)
    out, err = capfd.readouterr()
    assert "META" and FALLBACK_PATH in out
    assert ke.value.code > 0

    # EMPTY [META] SECTION i.e. no cfgpaths property
    invalid_config_EMPTY_META = "[META]"
    testSetup.get_object(FALLBACK_PATH).set_contents(invalid_config_EMPTY_META)
    args = {"--config": None}
    with pytest.raises(SystemExit) as ae:
        ConfMgr().parse(args)
    out, err = capfd.readouterr()
    assert "META" and FALLBACK_PATH in out
    assert ae.value.code > 0

    # EMPTY CONFIGPATHS PROPERTY
#    invalid_config_EMPTY_CFPATHS = ""


@pytest.mark.parametrize("expected_path", DEFAULT_CONFIG_PATHS)
def test_minimal_config_is_parsed_from_default_locations(
        testSetup: Iterator[FakeFilesystem],
        expected_path: str) -> None:
    """! @START_SCENARIO
    there are a set of @ref DEFAULT_CONFIG_PATHS "default locations" that the
    application uses to look for configs (in the absence of command line args
    specifying a custom config location) we want to test that config files are
    found and parsed when in any of these locations.
    @GIVEN{a valid `<project_root>/templates/fallback.ini` exists}
    @AND_G{An @ref MINIMAL_CONFIG "minimal config" file exists at one of the
           @ref DEFAULT_CONFIG_PATHS "default locations"}
    @AND_G{The config defines a language and a project for that language}
    @AND_G{`--config <configfile>` is not passed on the command line}
    @WHEN{The config is parsed}VV
    @THEN{the project definition is accessible as:
          `ConfMgr().projects.<language_name>.<project_name>`}
    @END_SCENARIO
    """

    testSetup.create_file(FALLBACK_PATH, contents=MINIMAL_FALLBACK_INI)
    testSetup.create_file(expected_path, contents=MINIMAL_CONFIG)
    args = {"--config": None}
    ConfMgr().parse(args)

    expectedProjectName = "testProject"
    assert ConfMgr().projects.test_language.test_project == expectedProjectName


@pytest.mark.parametrize("expected_path", NON_DEFAULT_CONFIG_PATHS)
def test_minimal_config_is_parsed_from_custom_locations(
        testSetup: Iterator[FakeFilesystem],
        expected_path: str) -> None:
    """! @START_SCENARIO
    The user should be able to manually specify a config file location should
    they so choose.
    @GIVEN{A valid `<project_root>/templates/fallback.ini` exists}
    @AND_G{`--config <configfile>` **is** passed on the command line specifying
           a path to a config file}
    @AND_G{An @ref MINIMAL_CONFIG "minimal config" file exists at the
           @ref NON_DEFAULT_CONFIG_PATHS "custom location" specified above}
    @AND_G{The config defines a language and a project for that language}
    @WHEN{The config is parsed}VV
    @THEN{the project definition is accessible as:
          `ConfMgr().projects.<language_name>.<project_name>`}
    @END_SCENARIO
    """
    testSetup.create_file(FALLBACK_PATH, contents=MINIMAL_FALLBACK_INI)
    testSetup.create_file(expected_path, contents=MINIMAL_CONFIG)
    args = {"--config": expected_path}
    ConfMgr().parse(args)

    expectedProjectName = "testProject"
    assert ConfMgr().projects.test_language.test_project == expectedProjectName


@pytest.mark.xfail(reason="not implemented yet")
def test_single_language_zero_projects(testSetup):
    """! @START_SCENARIO
    @GIVEN{ }
    @WHEN{ }
    @THEN{ }
    @END_SCENARIO
    """
    pytest.skip("not implemented yet")


@pytest.mark.xfail(reason="not implemented yet")
def test_language_can_have_single_project(testSetup):
    """! @START_SCENARIO
    @GIVEN{ }
    @WHEN{ }
    @THEN{ }
    @END_SCENARIO
    """
    pytest.skip("not implemented yet")


@pytest.mark.xfail(reason="not implemented yet")
def test_language_can_have_multiple_projects(testSetup):
    """! @START_SCENARIO
    @GIVEN{ }
    @WHEN{ }
    @THEN{ }
    @END_SCENARIO
    """
    pytest.skip("not implemented yet")


@pytest.mark.xfail(reason="not implemented yet")
def test_multiple_languages_zero_projects(testSetup):
    """! @START_SCENARIO
    @GIVEN{ }
    @WHEN{ }
    @THEN{ }
    @END_SCENARIO
    """
    pytest.skip("not implemented yet")


@pytest.mark.xfail(reason="not implemented yet")
def test_mutliple_languages_single_project(testSetup):
    """! @START_SCENARIO
    @GIVEN{ }
    @WHEN{ }
    @THEN{ }
    @END_SCENARIO
    """
    pytest.skip("not implemented yet")


@pytest.mark.xfail(reason="not implemented yet")
def test_multiple_language_multiple_projects(testSetup):
    """! @START_SCENARIO
    @GIVEN{ }
    @WHEN{ }
    @THEN{ }
    @END_SCENARIO
    """
    pytest.skip("not implemented yet")


@pytest.mark.xfail(reason="not implemented yet")
def test_zero_languages(testSetup):
    """! @START_SCENARIO
    @GIVEN{ }
    @WHEN{ }
    @THEN{ }
    @END_SCENARIO
    """
    pytest.skip("not implemented yet")
