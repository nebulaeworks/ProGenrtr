import configparser
from pathlib import Path
from typing import Any


class DataStruct:
    """!
    data object to access config in a sane manner, essentially a dictionary
    that allows access to its keys as data members.
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def get(self, attr: str, default: Any = None) -> Any:
        try:
            return getattr(self, attr)
        except AttributeError:
            return default

    def __getitem__(self, attr: str) -> Any:
        return self.__dict__[attr]

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()


def getConfig(path: str) -> dict:
    """!
    read the config file and return the object as parsed by ConfigParser.
    @param path is the path to the ini style config file
    @returns parsed config object
    """
    if not Path(path).exists():
        raise FileNotFoundError(f"config file not found at '{path}'")
    data = configparser.ConfigParser()
    data._interpolation = configparser.ExtendedInterpolation()
    data.read(path)
    return data


def makeDataStruct(data: dict, attribute: str = None):
    """!
    create a ConfigStruct from a parsed config object, either for the file as
    a whole or for a specific section of the config file.
    @param data the dictionary containing the parsed config
    @param section the section you wish to convert (optional)
    @returns ConfigStruct containg the parsed config values.
    """
    if attribute is None:
        return DataStruct(**data)
    else:
        return DataStruct(**data[attribute])
