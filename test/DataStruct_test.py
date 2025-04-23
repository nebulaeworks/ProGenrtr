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
    actual: DataStruct = DataStruct(**testClass().varDict)
    expectedInt: int = deepcopy(testClass().varInt)
    expectedStr: str = deepcopy(testClass().varStr)

    assert type(actual['int']) is type(expectedInt)
    assert actual['int'] == expectedInt
    assert type(actual['str']) is type(expectedStr)
    assert actual['str'] == expectedStr


def test_DataStruct_bad_dictionary_access() -> None:
    actual: DataStruct = DataStruct(**testClass().varDict)

    with pytest.raises(KeyError):
        actual['nonExistantNonsense']


def test_DataStruct_good_defaulted_access() -> None:
    actual: DataStruct = DataStruct(**testClass().varDict)
    expectedInt: int = deepcopy(testClass().varInt)
    expectedStr: str = deepcopy(testClass().varStr)

    assert type(actual.get('int')) is type(expectedInt)
    assert actual.get('int') == expectedInt
    assert type(actual.get('str')) is type(expectedStr)
    assert actual.get('str') == expectedStr


def test_DataStruct_defaulted_access_nonexistant_value_no_default() -> None:
    actual: DataStruct = DataStruct(**testClass().varDict)
    assert actual.get('nonExistantNonsense') is None


def test_DataStruct_defaulted_access_nonexistant_value_with_default() -> None:
    actual: DataStruct = DataStruct(**testClass().varDict)
    assert type(actual.get('nonExistantNonsense', "defaultVal")) is type("defaultVal")
    assert actual.get('nonExistantNonsense', "defaultVal") == "defaultVal"
    assert type(actual.get('nonExistantNonsense', 42)) is type(42)
    assert actual.get('nonExistantNonsense', 42) == 42
    assert type(actual.get('nonExistantNonsense', {"a": "b"})) is type({"a": "b"})
    assert actual.get('nonExistantNonsense', {"a": "b"}) == {"a": "b"}


def test_makeDataStruct_works_with_naked_dict() -> None:
    actual: DataStruct = makeDataStruct(testClass().varDict)
    expectedType = DataStruct

    assert type(actual) is expectedType
    assert actual.int == testClass().varInt
    assert actual.subdict == deepcopy(testClass().varDict['subdict'])


def test_makeDataStruct_can_construct_DataStruct_from_sub_dict() -> None:
    actual: DataStruct = makeDataStruct(testClass().varDict, "subdict")
    expectedType = DataStruct

    assert type(actual) is expectedType
    assert actual.a == "b"
