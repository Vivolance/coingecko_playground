from typing import Optional

from pydantic import BaseModel


class RawCoinsList(BaseModel):
    id: str
    symbol: str
    name: Optional[str] = None
    platforms: Optional[dict[str, str]] = None

