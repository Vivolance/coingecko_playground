from datetime import datetime, timezone
from io import BytesIO
from typing import Generator

import boto3
from dotenv import load_dotenv
from mypy_boto3_s3 import S3Client, ListObjectsV2Paginator
from mypy_boto3_s3.type_defs import ListObjectsV2OutputTypeDef, ObjectTypeDef

from src.models.file_info import FileInfo


class S3Explorer:
    """
    This class is responsible for uploading and downloading raw coin list
    to and from S3.
    """
    def __init__(self, s3_client: S3Client):
        self._s3_client = s3_client

    def upload_file(self, local_file_path: str, bucket_name: str, s3_path: str) -> None:
        self._s3_client.upload_file(local_file_path, bucket_name, s3_path)

    def upload_file_buffer(self, bytes_io: BytesIO, bucket_name: str, s3_path: str) -> None:
        bytes_io.seek(0)
        self._s3_client.upload_fileobj(bytes_io, bucket_name, s3_path)

    def download_file(self, bucket_name: str, s3_path: str, local_file_path) -> None:
        self._s3_client.download_file(bucket_name, s3_path, local_file_path)

    def download_file_buffer(self, bucket_name: str, s3_path: str, bytes_io:BytesIO) -> None:
        bytes_io.seek(0)
        self._s3_client.download_fileobj(bucket_name, s3_path, bytes_io)

    def paginate(self, bucket: str, s3_path: str, last_modified_date: datetime) -> Generator[FileInfo, None, None]:
        """
        Iterates and gives back file metadata (key + modified date) of files in a S3 path
        """
        paginator: ListObjectsV2Paginator = self._s3_client.get_paginator("list_objects_v2")
        for page in paginator.paginate(Bucket=bucket, Prefix=s3_path):
            page: ListObjectsV2OutputTypeDef
            if "Contents" in page:
                current_page_content: list[ObjectTypeDef] = page["Contents"]
                for single_file in current_page_content:
                    current_last_modified_date: datetime = single_file["LastModified"].astimezone(timezone.utc).replace(tzinfo=None)
                    if current_last_modified_date > last_modified_date:
                        yield FileInfo(
                            key=single_file["Key"],
                            last_modified_date=current_last_modified_date
                        )


if __name__ == "__main__":
    load_dotenv()
    s3_client: S3Client = boto3.client("s3")
    s3_explorer: S3Explorer = S3Explorer(s3_client)
    for item in s3_explorer.paginate(bucket="coingecko", s3_path="coins_list", last_modified_date=datetime(year=2025, month=1, day=1)):
        print(item)