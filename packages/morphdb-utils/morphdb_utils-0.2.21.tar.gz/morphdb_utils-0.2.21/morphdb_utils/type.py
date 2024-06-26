from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, TypedDict, Union


class Protocol(Enum):
    FILE = "file://"
    S3 = "morph-storage://"


class NullValue(Enum):
    NULL_VALUE = 0


class ListValue(TypedDict):
    values: List["Value"]


class Struct(TypedDict):
    fields: Dict[str, "Value"]


class Value(TypedDict):
    kind: Dict[str, Any]


class SqlResultRowResponse(TypedDict):
    value: Dict[str, Value]


@dataclass
class SqlResultResponse:
    headers: List[str]
    rows: List[SqlResultRowResponse]


@dataclass
class SignedUrlResponse:
    url: str


@dataclass
class RefResponse:
    canvas_json_path: str
    cell_type: str
    filename: str
    settings: Dict[str, int]
    description: Optional[str]
    code: Optional[str]
    parent_cells: List[str]
    connection_type: Optional[str]
    connection_slug: Optional[str]
    storage_path: Optional[str]


class SheetCellParams(TypedDict):
    type: Literal["sheet"]
    cell_name: str
    filename: Optional[str]
    timestamp: Optional[int]
    base_url: Optional[str]
    team_slug: Optional[str]
    authorization: Optional[str]
    notebook_id: Optional[str]


class SqlCellParams(TypedDict):
    type: Literal["sql"]
    sql: str
    connection_slug: Optional[str]
    database_id: Optional[str]
    base_url: Optional[str]
    team_slug: Optional[str]
    authorization: Optional[str]
    notebook_id: Optional[str]


class PythonCellParams(TypedDict):
    type: Literal["python"]
    cell_name: str
    filename: Optional[str]
    timestamp: Optional[int]
    base_url: Optional[str]
    team_slug: Optional[str]
    authorization: Optional[str]
    notebook_id: Optional[str]


LoadDataParams = Union[RefResponse, SheetCellParams, SqlCellParams]


@dataclass
class StorageFile:
    name: str
    path: str
    size: int

@dataclass
class StorageDirectory:
    name: str
    path: str
    directories: List[StorageDirectory]
    files: List[StorageFile]

@dataclass
class ListStorageDirectoryResponse:
    path: str
    directories: List[StorageDirectory]
    files: List[StorageFile]