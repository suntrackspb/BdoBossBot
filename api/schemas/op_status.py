from dataclasses import dataclass
from typing import Any


@dataclass
class OpStatusSchema:
    status_code: int
    message: str | None = None
    data: Any | None = None
