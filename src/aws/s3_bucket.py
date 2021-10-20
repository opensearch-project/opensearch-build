# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
from pathlib import Path
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError


class S3Bucket:
    AWS_ROLE_ARN = "AWS_ROLE_ARN"
    AWS_ROLE_SESSION_NAME = "AWS_ROLE_SESSION_NAME"

    def __init__(self, bucket_name, role_arn=None, role_session_name=None):
        """
        Provides methods to download/upload files and folders to S3 bucket

        :param bucket_name: The s3 bucket name
        :param role_arn: the arn of the role that has permissions to access S3
        :param role_session_name: the aws role session name
        """
        self.bucket_name = bucket_name
        self.role_arn = role_arn if role_arn is not None else os.environ.get(S3Bucket.AWS_ROLE_ARN)
        self.role_session_name = role_session_name if role_session_name is not None else os.environ.get(S3Bucket.AWS_ROLE_SESSION_NAME)
        # TODO: later use for credential refereshing
        assumed_role_creds = self.__sts_assume_role()
        self.__s3_client, self.__s3_resource = self.__create_s3_clients(assumed_role_creds)

    def __sts_assume_role(self):
        try:
            sts_connection = boto3.client("sts")
            response = sts_connection.assume_role(
                RoleArn=self.role_arn,
                RoleSessionName=self.role_session_name,
                DurationSeconds=3600,
            )
            return response["Credentials"]
        except Exception as e:
            raise STSError(e)

    def __create_s3_clients(self, assumed_role_cred):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=assumed_role_cred["AccessKeyId"],
            aws_secret_access_key=assumed_role_cred["SecretAccessKey"],
            aws_session_token=assumed_role_cred["SessionToken"],
        )
        s3_resource = boto3.resource(
            "s3",
            aws_access_key_id=assumed_role_cred["AccessKeyId"],
            aws_secret_access_key=assumed_role_cred["SecretAccessKey"],
            aws_session_token=assumed_role_cred["SessionToken"],
        )
        return s3_client, s3_resource

    def download_folder(self, prefix, dest):
        """
        Download the contents of a folder directory

        :param prefix: The folder path inside the bucket
        :param dest: local destination to download the folder at
        """
        bucket = self.__s3_resource.Bucket(self.bucket_name)
        s3_path = urlparse(prefix).path.lstrip("/")
        local_dir = Path(dest)
        s3_response = bucket.objects.filter(Prefix=s3_path)
        for obj in s3_response:
            target = obj.key if local_dir is None else local_dir / Path(obj.key).relative_to(s3_path)
            target.parent.mkdir(parents=True, exist_ok=True)
            if obj.key[-1] == "/":
                continue
            self.__download(bucket, obj.key, str(target))

    def download_file(self, key, dest):
        """
        Download a single object from s3.

        :param key: The s3 key for the object to download
        :param dest: local destination
        """
        bucket = self.__s3_resource.Bucket(self.bucket_name)
        local_dir = Path(dest)
        file_name = key.split("/")[-1]
        target = Path(local_dir) / Path(file_name)
        return self.__download(bucket, key, str(target))

    @staticmethod
    def __download(bucket, key, path):
        try:
            bucket.download_file(key, path)
        except ClientError as e:
            logging.error(f"Failed to download s3 key: {key} from path: {path}")
            raise S3DownloadError(e)

    def upload_file(self, key, source):
        """
        Upload a file to s3.

        :param key: The s3 key for the uploaded object
        :param source: local path of the file
        """
        try:
            self.__s3_client.upload_file(source, self.bucket_name, key)
        except ClientError as e:
            logging.error(f"Failed to upload s3 key: {key} from local source: {source}")
            raise S3UploadError(e)


class S3Error(Exception):
    """Base class for S3 Errors"""

    pass


class STSError(Exception):
    """Base class for STS Error"""

    pass


class S3DownloadError(S3Error):
    """Raised when there is a download object failure"""

    pass


class S3UploadError(S3Error):
    """Raised when there is an upload object failure"""

    pass
