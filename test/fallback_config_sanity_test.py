from configparser import ConfigParser
from os.path import exists
from pathlib import Path

import pytest

fallbackConf = "templates/fallback.ini"
configPathSection = "META"


class TestFallbackConfig():
    """!
    @test Validate the actual fallback config used by the application.
    @todo make this representitive as it these tests are based on an older
          version of the config files
    @bug many of these tests pass when they probably shouldnt
    """

    def test_fallback_config_exists(self):
        """! @START_SCENARIO
        A real fallback.ini config MUST exist at the @ref fallbackConf
        "fallbackConf path"
        @GIVEN{ }
        @WHEN{ }
        @THEN{ }
        @END_SCENARIO
        """
        assert Path(fallbackConf).is_file()

    def test_fallback_has_meta_config_paths_section(self):
        """! @START_SCENARIO
        the fallback config must contain a section called META_CONFIG_PATHS
        @GIVEN{ }
        @WHEN{ }
        @THEN{ }
        @END_SCENARIO
        """
        fallback = ConfigParser()
        fallback.read(fallbackConf)
        assert fallback.has_section(configPathSection)

    def test_fallback_config_paths_not_empty(self):
        """! @START_SCENARIO
        The META_CONFIG_PATHS section is not empty
        @GIVEN{ }
        @WHEN{ }
        @THEN{ }
        @END_SCENARIO
        """
        fallback = ConfigParser()
        fallback.read(fallbackConf)
        assert len(fallback.items(configPathSection)) > 0
