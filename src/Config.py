import configparser
from pathlib import Path
from typing import Any


class DataStruct:
    """!
    data object; essentially takes a dictionary-like object and provides access
    to its entries as first class data members, whilst retaining dictionary
    style access.

    @par Examples
    @code{.py}
    # create a dictionary to create a DataStruct from
    var: dict = {"stuff": "and", "some": "things"}
    # create a DataStruct by unpacking the dictionary into the constructor
    data: DataStruct = DataStruct(**var)

    # member access
    print(data.stuff)  # prints 'and'
    print(data.some)   # prints 'things'

    # dictionary access
    print(data["stuff"])       # prints 'and'
    print(data["some"])        # prints 'things'
    print(data["twistybits"])  # KeyError

    # defaulted access
    print(data.get("stuff"))       # prints 'and'
    print(data.get("some"))        # prints 'stuff'
    print(data.get("turnips"))     # prints 'None'
    print(data.get("turnips", 42)) # prints '42'
    @endcode
    """

    def __init__(self, **kwargs):
        """!
        constructs a DataStruct from a dict or dict like object (remember to
        unpack it with `**` operator); Alternatively a series of named params
        can be directly used (although utility for this seems limited).

        @param kwargs a series of named parameters
        @throws TypeError if the data provided (or attribute specified) is or
                contains a type would create an invalid member or data not a
                dict-like object
        @throws AttributeError if somehow you have managed to override the
                internal `__dict__` member with something that is not not a
                dict..... dumbass

        @par Examples
        @code{.py}
        var: dict = {"stuff": "and", "some": "things"}
        data: DataStruct = DataStruct(**var)
        @endcode
        """
        self.__dict__.update(kwargs)

    def get(self, attr: str, default: Any = None) -> Any:
        """!
        provides defaulted access to the members. i.e. if the attribute does not
        exist then return will default to `None` unless an explicit default
        value is provided

        @param attr the attribute name as a string
        @param default the value to return if the attribute does not exist
               is None if no explicit value is provided
        @returns Any value type that is stored by the specified attribute or
                 default value.

        @par Examples
        @code
        var: dict = {"stuff": "and", "some": "things"}
        data: DataStruct = DataStruct(**var)

        print(data.get("stuff"))       # prints 'and'
        print(data.get("some"))        # prints 'stuff'
        print(data.get("turnips"))     # prints 'None'
        print(data.get("turnips", 42)) # prints '42'
        @endcode
        """
        try:
            return getattr(self, attr)
        except AttributeError:
            return default

    def __getitem__(self, attr: str) -> Any:
        """!
        provides dictionary style access to the members. i.e. using normal
        square bracket indexing.

        @param attr the attribute name as a string
        @returns Any value applicable to the attribute requested
        @throws KeyError if the attribute does not exist

        @par Examples
        @code
        var: dict = {"stuff": "and", "some": "things"}
        data: DataStruct = DataStruct(**var)

        print(data["stuff"])       # prints 'and'
        print(data["some"])        # prints 'stuff'
        print(data["turnips"])     # KeyError: 'turnips'
        @endcode
        """
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
    create a DataStruct from a dictionary-like object; this also allows you to
    create a DataStruct from a dictionary-like object nested inside another
    dictionary-like object by providing a value to the `attribute` named param.

    @param data the dictionary containing the parsed config
    @param attribute a nested dict-like object within the data you are passing
           in.
    @return DataStruct containing the dict-like entry keys as data members and
            entry values as the data member values
    @throws TypeError if the data provided (or attribute specified) is or
            contains a type would create an invalid member or data not a
            dict-like object
    @throws AttributeError if somehow you have managed to override the
            internal `__dict__` member with something that is not not a dict
            ..... dumbass

    @par Examples
    @code{.py}
    @endcode
    """
    if attribute is None:
        return DataStruct(**data)
    else:
        return DataStruct(**data[attribute])
