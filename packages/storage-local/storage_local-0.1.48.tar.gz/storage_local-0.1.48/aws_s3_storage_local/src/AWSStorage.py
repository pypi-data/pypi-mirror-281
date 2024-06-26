import os

import boto3
from logger_local.MetaLogger import MetaLogger
from python_sdk_remote.utilities import our_get_env

from .StorageConstants import STORAGE_TYPE_ID, FILE_TYPE_ID, LOGGER_CODE_OBJECT
from .StorageDB import StorageDB
from .StorageInterface import StorageInterface
from .StorageConstants import ExtensionsEnum


AWS_ACCESS_KEY_ID = our_get_env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = our_get_env("AWS_SECRET_ACCESS_KEY")


class AwsS3Storage(StorageInterface, metaclass=MetaLogger, object=LOGGER_CODE_OBJECT):

    def __init__(self, bucket_name: str, region: str) -> None:
        self.region = region
        self.bucket_name = bucket_name
        self.storage_database = StorageDB()
        self.boto3_client = boto3.client('s3',
                                   aws_access_key_id=AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    @staticmethod
    # TODO Move this method out of this class
    def get_filename_from_path(path: str) -> str:
        return os.path.basename(path)

    def upload_file(self, *, local_file_path: str, remote_path: str, url: str = None) -> int or None:
        """uploads file to S3"""
        read_binary = 'rb'
        filename = self.get_filename_from_path(local_file_path)
        # determine type of file
        ext=os.path.splitext(local_file_path)[1]
        with open(local_file_path, read_binary) as file_obj:
            file_contents = file_obj.read()

        # Upload the file to S3 with the CRC32 checksum
        response = self.boto3_client.put_object(
            Bucket=self.bucket_name,
            Key=remote_path + filename,
            Body=file_contents,
            ChecksumAlgorithm='crc32'
        )


        if 'ETag' in response:
            # TODO: constracts should be replaced with parameters
            storage_id = self.storage_database.upload_to_database(file_path=remote_path, filename=filename,
                                                                  region=self.region, storage_type_id=STORAGE_TYPE_ID,
                                                                  file_type_id=FILE_TYPE_ID, extension_id=(self.get_eum_by_extension(ext)),
                                                                  url=url)
            return storage_id
        return None

    # download a file from s3 to local_file_path
    def download_file(self, remote_path: str, local_file_path: str) -> None:
        self.boto3_client.download_file(self.bucket_name, remote_path, local_file_path)

    # logical delete

    def delete_by_remote_path_filename(self, remote_path: str, filename: str) -> None:
        self.storage_database.delete(remote_path=remote_path, filename=filename, region=self.region)
    
    def delete_by_storage_id(self, storage_id: str, filename: str) -> None:
        self.storage_database.delete(remote_path=storage_id, filename=filename, region=self.region)

    def get_eum_by_extension(file_extension) -> int:
        if file_extension == '.txt':
            return ExtensionsEnum.txt.value
        if file_extension == '.doc':
            return ExtensionsEnum.doc.value
        if file_extension == '.pdf':
            return ExtensionsEnum.pdf.value
        if file_extension == '.xls':
            return ExtensionsEnum.xls.value
        if file_extension == '.jpg':
            return ExtensionsEnum.jpg.value
        else:
            raise ValueError(f"Unsupported file extension: {file_extension}")


