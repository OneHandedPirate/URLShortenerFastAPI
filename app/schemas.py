import datetime

from pydantic import BaseModel, ConfigDict, AnyUrl


class TokenResponse(BaseModel):
    original_url: AnyUrl
    short_url: str
    clicks_count: int
    created_at: datetime.datetime
