"""! @test
tests of the src.Config.DataStruct class along with its helper
functions: src.Config.getConfig() and src.Config.makeDataStruct(). Together these
provide low level (relatively speaking) handling of ini formatted config files.
"""
import pytest
from typing import Any
from copy import deepcopy
from Config import DataStruct, getConfig, makeDataStruct


class testClass:
    """!
    only exists as an example of a user defined data type for testing purposes.
    """

    def __init__(self):
        self.varStr: str = "aye"
        self.varEmptyStr: str = ""
        self.varFloat: float = 3.14159
        self.varInt: int = 42
        self.varBoolT: bool = True
        self.varBoolF: bool = False
        self.varNone: None = None
        self.varList: list = [self.varStr, self.varEmptyStr, self.varFloat,
                              self.varInt, self.varBoolT, self.varBoolF,
                              self.varNone]
        self.varDict: dict = {"str": self.varStr, "emptyStr": self.varEmptyStr,
                              "float": self.varFloat, "int": self.varInt,
                              "boolT": self.varBoolT, "boolF": self.varBoolF,
                              "none": self.varNone, "subdict": {"a": "b"}}
        self.varTuple: tuple = (self.varStr, self.varEmptyStr, self.varFloat,
                                self.varInt, self.varBoolT, self.varBoolF,
                                self.varNone)
        self.varSet: set = set({self.varStr, self.varEmptyStr, self.varFloat,
                                self.varInt, self.varBoolT, self.varBoolF,
                                self.varNone})

    def functionCall(self, param: Any) -> Any:
        return param


def test_DataStuct_dict_init_handles_standard_primitives() -> None:
    """! @START_SCENARIO
    normal instanciation of a DataStruct object requires a dictionary to be
    passed in as kwargs (see todo for @ref src.Config.DataStruct.__init__()
    "DataStruct constructor") and results in a DataStruct object that
    contains all the entries of that dictionary as member properties. Test that
    this works for all common primitive types.
    @GIVEN{A dictionary containing any of the following types: str, int, float
           bool, None}
    @WHEN{A DataStruct is constructed from this dictionary}
    @THEN{The dictionary entries are converted to properties of the
          DataStruct object, where the entry key is the property name and the
          entry value is the property value}
    @END_SCENARIO
    """
    # deepcopy may be unnecessary but this way we dont have to keep track of
    # which vars are which type so if it changes in the future it wont break
    # because of value/reference semantics
    expectedA = deepcopy(testClass().varStr)
    expectedB = deepcopy(testClass().varEmptyStr)
    expectedC = deepcopy(testClass().varFloat)
    expectedD = deepcopy(testClass().varInt)
    expectedE = deepcopy(testClass().varBoolT)
    expectedF = deepcopy(testClass().varBoolF)
    expectedG = deepcopy(testClass().varNone)

    testDict: dict = {
        "A": expectedA,
        "B": expectedB,
        "C": expectedC,
        "D": expectedD,
        "E": expectedE,
        "F": expectedF,
        "G": expectedG
    }
    actual: DataStruct = DataStruct(**testDict)
    assert actual.A == expectedA
    assert actual.B == expectedB
    assert actual.C == expectedC
    assert actual.D == expectedD
    assert actual.E == expectedE
    assert actual.F == expectedF
    assert actual.G == expectedG


def test_DataStruct_dict_init_handles_standard_collections() -> None:
    """! @START_SCENARIO
    Same as test_DataStuct_dict_init_handles_standard_primitives except for
    standard python collections. Makes sure that these collections become
    direct members and that normal operations on those collections act normally
    @GIVEN{A dictionary containing any of the following types: list, dict,
           tuple, set}
    @WHEN{A DataStruct is constructed from this dictionary}
    @THEN{The collection dictionary entries are converted to properties of the
          DataStruct object, where the entry key is the property name and the
          entry value is the actual collection}
    @AND_T{the collections are still usable as such}
    @END_SCENARIO
    """
    expectedH = deepcopy(testClass().varList)
    expectedI = deepcopy(testClass().varDict)
    expectedJ = deepcopy(testClass().varTuple)
    expectedK = deepcopy(testClass().varSet)
    testDict: dict = {
        "H": expectedH,
        "I": expectedI,
        "J": expectedJ,
        "K": expectedK,
    }
    actual: DataStruct = DataStruct(**testDict)

    # List tests
    assert actual.H == expectedH
    assert type(actual.H) is list
    assert len(actual.H) == len(expectedH)

    # dict tests
    assert actual.I == expectedI
    assert type(actual.I) is dict
    assert len(actual.I) == len(expectedI)

    # tuple tests
    assert actual.J == expectedJ
    assert type(actual.J) is tuple
    assert len(actual.J) == len(expectedJ)

    # set tests
    assert actual.K == expectedK
    assert type(actual.K) is set
    assert len(actual.K) == len(expectedK)


def test_DataStruct_dict_init_handles_custom_types() -> None:
    """! @START_SCENARIO
    Same as test_DataStuct_dict_init_handles_standard_primitives except for
    user defined types; Makes sure that these types can have their properties
    accessed and functions called.
    @GIVEN{A dictionary containing a user defined type}
    @WHEN{A DataStruct is constructed from this dictionary}
    @THEN{The user defined type is accessible as a direct member of the
          DataStruct}
    @AND_T{properties and functions of the userdefined type are accessible
           callable(respectively)}
    @END_SCENARIO
    """
    expectedL: testClass = testClass()
    testDict: dict = {
        "L": expectedL
    }
    actual: DataStruct = DataStruct(**testDict)
    assert actual.L == expectedL
    assert type(actual.L) is testClass
    assert type(actual.L.varInt) is int
    assert actual.L.varInt is deepcopy(testClass().varInt)
    assert actual.L.functionCall("poop") == "poop"


def test_DataStruct_good_dictionary_access() -> None:
    """! @START_SCENARIO
    ensure that dictionary access in a datastruct mirrors the member access
    @GIVEN{A dictionary (non empty) initialised DataStruct}
    @WHEN{The DataStruct is accessed using square brackets notation}
    @THEN{The returned value is the same type and value of the original dict}
    @END_SCENARIO
    """
    actual: DataStruct = DataStruct(**testClass().varDict)
    expectedInt: int = deepcopy(testClass().varInt)
    expectedStr: str = deepcopy(testClass().varStr)

    assert type(actual['int']) is type(expectedInt)
    assert actual['int'] == expectedInt
    assert type(actual['str']) is type(expectedStr)
    assert actual['str'] == expectedStr


def test_DataStruct_bad_dictionary_access() -> None:
    """! @START_SCENARIO
    ensure that dictionary access in a DataStruct throws appropriately when
    presented with bad inputs
    @GIVEN{A dictionary (non empty) initialised DataStruct}
    @WHEN{The DataStruct is accessed using square brackets notation}
    @AND_W{The entry being accessed does not exist in the original dictionary}
    @THEN{A `KeyError` is thrown}
    @END_SCENARIO
    """
    actual: DataStruct = DataStruct(**testClass().varDict)

    with pytest.raises(KeyError):
        actual['nonExistantNonsense']


def test_DataStruct_good_defaulted_access() -> None:
    """! @START_SCENARIO
    ensure that access to DataStruct members via `get()` provides the
    appropriate result.
    @GIVEN{A DataStruct initialised with a non empty dictionary}
    @WHEN{The DataStruct is accessed using the `get()` method}
    @AND_W{The parameter passed to `get()` corresponds to an entry in the
           initial dictionary}
    @THEN{The returned value is of the same type and value as in the initial
          dictionary}
    @END_SCENARIO
    """
    actual: DataStruct = DataStruct(**testClass().varDict)
    expectedInt: int = deepcopy(testClass().varInt)
    expectedStr: str = deepcopy(testClass().varStr)

    assert type(actual.get('int')) is type(expectedInt)
    assert actual.get('int') == expectedInt
    assert type(actual.get('str')) is type(expectedStr)
    assert actual.get('str') == expectedStr


def test_DataStruct_defaulted_access_nonexistant_value_no_default() -> None:
    """! @START_SCENARIO
    make sure that when no default parameter value is provided to the `get()`
    method access to nonexistant entries/members is `None`
    @GIVEN{A DataStruct}
    @WHEN{a nonexistant member/entry is accessed with `get()`}
    @AND_W{no default parameter value is provided}
    @THEN{The returned value/type is `None`}
    @END_SCENARIO
    """
    actual: DataStruct = DataStruct(**testClass().varDict)
    assert actual.get('nonExistantNonsense') is None


def test_DataStruct_defaulted_access_nonexistant_value_with_default() -> None:
    """! @START_SCENARIO
    make sure that when a default parameter value is provided to the `get()`
    method, access to nonexistant entries/members is the same type/value as the
    default value provided.
    @GIVEN{A DataStruct is accessed with the `get()` method}
    @AND_G{The entry/member attempting to be accessed does not exist}
    @WHEN{A value is provided for the `default` parameter}
    @THEN{The returned value/type is the same as the provided default}
    @END_SCENARIO
    """
    actual: DataStruct = DataStruct(**testClass().varDict)
    assert type(actual.get('nonExistantNonsense', "defaultVal")) is type("defaultVal")
    assert actual.get('nonExistantNonsense', "defaultVal") == "defaultVal"
    assert type(actual.get('nonExistantNonsense', 42)) is type(42)
    assert actual.get('nonExistantNonsense', 42) == 42
    assert type(actual.get('nonExistantNonsense', {"a": "b"})) is type({"a": "b"})
    assert actual.get('nonExistantNonsense', {"a": "b"}) == {"a": "b"}


def test_makeDataStruct_works_with_naked_dict() -> None:
    """! @todo @START_SCENARIO
    @GIVEN{ }
    @WHEN{ }
    @THEN{ }
    @END_SCENARIO
    """
    actual: DataStruct = makeDataStruct(testClass().varDict)
    expectedType = DataStruct

    assert type(actual) is expectedType
    assert actual.int == testClass().varInt
    assert actual.subdict == deepcopy(testClass().varDict['subdict'])


def test_makeDataStruct_can_construct_DataStruct_from_sub_dict() -> None:
    """! @todo @START_SCENARIO
    @GIVEN{ }
    @WHEN{ }
    @THEN{ }
    @END_SCENARIO
    """
    actual: DataStruct = makeDataStruct(testClass().varDict, "subdict")
    expectedType = DataStruct

    assert type(actual) is expectedType
    assert actual.a == "b"
