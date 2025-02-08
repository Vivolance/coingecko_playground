import os
from typing import Any

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine, Table, insert

from database.tables import coin_list_table
from src.models.coin_list import CoinsList
from src.service.extractor import CoinListExtractor


class CoinListDAO:
    def __init__(self, connection_string: str) -> None:
        self._engine: Engine = create_engine(connection_string)
        self._table: Table = coin_list_table

    def insert(self, raw_results: list[CoinsList]) -> None:
        with self._engine.begin() as conn:
            deserialized_results: list[dict[str, Any]] = [
                raw_result.model_dump() for raw_result in raw_results
            ]
            conn.execute(insert(self._table), deserialized_results)


if __name__ == "__main__":
    load_dotenv()
    coin_list_extractor: CoinListExtractor = CoinListExtractor()
    extracted_raw_result: list[CoinsList] = coin_list_extractor.coin_gecko_request()
    coin_list_dao: CoinListDAO = CoinListDAO(os.getenv("POSTGRES_URL"))
    coin_list_dao.insert(extracted_raw_result)


