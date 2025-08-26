"""Type definitions for yaml2sheet."""

from typing import TypedDict, List, Dict, Any, Union


# Basic type definitions
class M17nField(TypedDict):
    ja: str
    en: str


class Link(TypedDict):
    text: M17nField
    url: M17nField


class ConditionStatement(TypedDict):
    platform: str
    summary: M17nField


class Procedure(TypedDict):
    id: str
    platform: str
    target: str
    tool: str
    procedure: M17nField
    toolLink: Link


class Condition(TypedDict):
    type: str
    platform: str
    target: str
    procedure: Procedure
    conditions: List['Condition']
    conditionStatements: List[ConditionStatement]


class Check(TypedDict):
    id: str
    checkId: str
    subcheckId: str
    sortKey: Union[int, None]
    target: str
    platform: List[str]
    severity: str
    check: M17nField
    result: Union[M17nField, None]
    conditions: Union[List[Condition], None]
    guidelines: Union[List[Link], None]
    info: Union[List[Link], None]
    isSubcheck: Union[bool, None]
    subchecks: Union[Dict[str, Dict[str, Union[int, List[Any]]]], None]


class ColumnSetByTarget(TypedDict):
    plainData1: List[str]
    plainData2: List[str]
    linkData: List[str]
    generatedData: List[str]


class ColumnSet(TypedDict):
    idCols: List[str]
    userEntered: List[str]
    common: ColumnSetByTarget
    designWeb: ColumnSetByTarget
    designMobile: ColumnSetByTarget
    codeWeb: ColumnSetByTarget
    codeMobile: ColumnSetByTarget
    productWeb: ColumnSetByTarget
    productIos: ColumnSetByTarget
    productAndroid: ColumnSetByTarget


class ColumnInfo(TypedDict):
    name: Dict[str, M17nField]
    width: Dict[str, int]
