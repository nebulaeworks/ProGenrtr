from configparser import ConfigParser
from Config import getConfig, conf2obj, ConfigStruct
from os.path import expanduser
from pathlib import Path


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

    __fallbackPath = "templates/fallback.ini"

    def __new__(cls):
        """!
        singleton mechanism, make sure that member variables are defined here as
        they will be overwritten in __init__ as it gets called everytime a 'new'
        object is created.
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(ConfMgr, cls).__new__(cls)
            cls.instance.projects = ConfigStruct()
            cls.instance.args = ConfigStruct()
        return cls.instance

    def parse(self, args: dict):
        """!
        parse the config file at the path provided or if none is provided then
        use the fallback config.
        @param confPath the path to the config file to parse.
        @return none, sets internal projects state
        """
        self.args = ConfigStruct(**args) # decoupling or untestable?
        if self.args["--config"] is None:
            print("WARNING: expected config not found using fallback!!")
            self.__conf = conf2obj(getConfig(ConfMgr.__fallbackPath), "META")
            self.__conf = self.__getConfFromList(
                    self.__conf.cfgpaths.split(",")
            )
            if self.__conf is None:
                self.__parseConfFileSections(ConfMgr.__fallbackPath)
        else:
            self.__parseConfFileSections(confPath)

    def __getConfFromList(self, paths: list[str]) -> ConfigStruct:
        """!
        parses and returns the first config found in the list provided.
        @param paths, list of strings representing the possible places that
               that config files could exist at.
        @returns none. just parses the first config file found. 
        """
        for path in paths:
            if self.__configPathExists(path):
                self.__parseConfFileSections(path)

    def __configPathExists(self, path: str) -> bool:
        """!
        checks that the provided path corresponds to a real path to a real file
        @param path string representation of a path to an ini style config
        @returns bool true iff path exists else false.
        """
        if Path(expanduser(path)).is_file():
            return True
        else:
            return False

    def __parseConfFileSections(self, path: str) -> None:
        """!
        This needs to parse all sections: language section defines which other
        sections exist.

        need to decide how to represent generable projects, probably as
        cloneable URLs.

        @param path, string representing the path of the config file to use.
        @returns none
        """
        config = getConfig(path)

        # Extract the languages
        langs = conf2obj(config, section="ProGenrtr").languages.split(',')
        langs = [s.strip() for s in langs]  # Clean newline characters

        # Create a dictionary to hold ConfigStructs
        projects = {}

        for lang in langs:
            if f"project.{lang}" in config:
                projects[lang] = conf2obj(config, section=f"project.{lang}")

        self.projects = ConfigStruct(**projects)
