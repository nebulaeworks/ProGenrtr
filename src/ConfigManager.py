from Config import getConfig, conf2obj, ConfigStruct
from utils import PROJECT_ROOT
from os.path import expanduser
from pathlib import Path
import sys


class ConfMgr(object):
    """!
    Singleton class responsble for parsing and making available config items to
    the rest of the application.

    This class only provides one public method, parse(), which can be used to
    parse an explicitly specified config file path or it can be called with
    default arguments in which case it will search a pre-defined list of
    locations for an expected filename, if it doesnt find any matching files
    it will use the fallback config.
    """

    __fallbackPath = f"{PROJECT_ROOT}/templates/fallback.ini"

    def __new__(cls):
        """!
        singleton mechanism, make sure that member variables are defined here
        as they will be overwritten in __init__ as it gets called everytime a
        'new' object is created.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfMgr, cls).__new__(cls)
            cls.instance.projects = ConfigStruct()
            cls.instance.args = ConfigStruct()
        return cls.instance

    @classmethod
    def reset(cls):
        """!
        de-initialises the ConfigManager
        """
        if hasattr(cls, "instance"):
            del ConfMgr.instance

    def parse(self, args: dict):
        """!
        parse the config file at the path provided or if none is provided then
        use the fallback config.
        @param args the dictionary of command line arguments
        @return none, sets internal projects state
        """
        self.__exitIfFallbackConfigDoesNotExists()

        self.args = ConfigStruct(**args)  # decoupling or untestable?

        if self.args["--config"] is None:
            cfgPaths = self.__getConfigLocationList()
            self.projects = self.__getConfFromList(cfgPaths)

            if self.projects is None:
                print("WARNING: expected config not found using fallback!!")
                self.projects = self.__parseConfFileSections(ConfMgr.__fallbackPath)
        else:
            self.__parseConfFileSections(self.args["--config"])

    def __getConfigLocationList(self) -> list[str]:
        """!
        parse the `[META]` section of the fallback config to retrieve the
        default locations at which config is expected to exist.

        @return List[str] where each entry is a filesystem path
        """
        meta = conf2obj(getConfig(ConfMgr.__fallbackPath), "META")
        return meta.cfgpaths.replace("\n", "").split(",")

    def __getConfFromList(self, paths: list[str]) -> ConfigStruct | None:
        """!
        parses and returns the first config found in the list provided.
        @param paths, list of strings representing the possible places that
               that config files could exist at.
        @returns none. just parses the first config file found.
        """
        for location in paths:
            path = expanduser(location)
            if self.__configPathExists(path):
                try:
                    return self.__parseConfFileSections(path)
                except Exception as e:
                    sys.exit(e)
        return None

    def __configPathExists(self, path: str) -> bool:
        """!
        checks that the provided path corresponds to a real path to a real file
        @param path string representation of a path to an ini style config
        @returns bool true iff path exists else false.
        """
        if Path(path).is_file():
            return True
        else:
            return False

    def __parseConfFileSections(self, path: str) -> ConfigStruct:
        """!
        This needs to parse all sections: language section defines which other
        sections exist.

        need to decide how to represent generable projects, probably as
        cloneable URLs.

        @param path, string representing the path of the config file to use.
        @returns none
        """
        try:
            config = getConfig(path)
        except FileNotFoundError as fe:
            print(f"ERROR: {str(fe)}")
            sys.exit(1)

        # Extract the languages
        langs = conf2obj(config, section="ProGenrtr").languages.split(',')
        langs = [s.strip() for s in langs]  # Clean newline characters
        # Create a dictionary to hold ConfigStructs
        projects = dict()

        for lang in langs:
            if f"project.{lang}" in config:
                projects[lang] = conf2obj(config, section=f"project.{lang}")

        return ConfigStruct(**projects)

    def __exitIfFallbackConfigDoesNotExists(self) -> None:
        """!
        check for the existance of the fallback.ini config file, if its missing
        exit with an appropriate status code
        """
        if Path(self.__fallbackPath).exists() is False:
            print(
                f"ERROR: necessary file '{self.__fallbackPath}' not available"
            )
            sys.exit(1)
