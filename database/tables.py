from sqlalchemy import MetaData, Table, Column, TEXT, JSON

metadata: MetaData = MetaData()
coin_list_table: Table = Table(
    "coin_list",
    metadata,
    Column("id", TEXT, primary_key=True),
    Column("symbol", TEXT, nullable=False),
    Column("name", TEXT, nullable=True),
    Column("platform", JSON, nullable=True)
)