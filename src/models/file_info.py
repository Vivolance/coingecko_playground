from datetime import datetime

from pydantic import BaseModel


class FileInfo(BaseModel):
    """
    Contains metadata of a S3 File
    Returned by S3Explorer
    """
    key: str    # Full S3 key to file e.g path/to/file.csv
    last_modified_date: datetime