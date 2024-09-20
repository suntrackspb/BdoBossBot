from datetime import datetime

from pydantic import BaseModel


class PromoCodeSchema(BaseModel):
    code: str
    loot: str | None = None
    expire: datetime | None = None
    created_at: datetime
    owner: int
