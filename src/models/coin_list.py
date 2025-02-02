from pydantic import BaseModel


class CoinsList(BaseModel):
    id: str
    symbol: str
    name: str
    platforms: dict[str, str]

