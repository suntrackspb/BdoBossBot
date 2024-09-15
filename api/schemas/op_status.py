from dataclasses import dataclass
from typing import Any

from marshmallow import Schema


@dataclass
class Status:
    status: str
    message: str


@dataclass
class OpStatusSchema:
    status_code: int
    message: str | None = None
    data: Any | None = None