from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CoinsList(BaseModel):
    contract_address: str
    timestamp: datetime
    id: str
    symbol: str
    name: Optional[str] = None
