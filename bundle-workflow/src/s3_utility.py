# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from pathlib import Path
from urllib.parse import urlparse

import boto3
from botocore.exceptions import ClientError


class S3Bucket:
    def __init__(self, bucket_name, role_arn=None, role_session_name=None):
        """
        Provides methods to download/upload files and folders to S3 bucket

        :param bucket_name: The s3 bucket name
        :param role_arn: the arn of the role that has permissions to access S3
        :param role_session_name: the aws role session name
        """
        self.bucket_name = bucket_name
        self.role_arn = (
            role_arn
            if role_arn is not None
            else os.environ.get("AWS_ROLE_ARN")
        )
        self.role_session_name = (
            role_session_name
            if role_session_name is not None
            else os.environ.get("AWS_ROLE_SESSION_NAME")
        )
        assumed_role_cred = self.__assume_role()
        self.__s3_client = boto3.client(
            "s3",
            aws_access_key_id=assumed_role_cred["AccessKeyId"],
            aws_secret_access_key=assumed_role_cred["SecretAccessKey"],
            aws_session_token=assumed_role_cred["SessionToken"],
        )
        self.__s3_resource = boto3.resource(
            "s3",
            aws_access_key_id=assumed_role_cred["AccessKeyId"],
            aws_secret_access_key=assumed_role_cred["SecretAccessKey"],
            aws_session_token=assumed_role_cred["SessionToken"],
        )

    def __assume_role(self):
        try:
            sts_connection = boto3.client("sts")
            return sts_connection.assume_role(
                RoleArn=self.role_arn,
                RoleSessionName=self.role_session_name,
                DurationSeconds=3600,
            )["Credentials"]
        except Exception as e:
            print("Assume role failed due to ", str(e.__repr__()))
            raise e


    @classmethod
    def download_folder(cls, bucket_name, prefix, dest, role_arn=None, role_session_name=None):
        """
        Download the contents of a folder directory

        :param bucket_name: The s3 bucket name
        :param prefix: The folder path inside the bucket
        :param dest: local destination to download the folder at
        :param role_arn: the arn of the role that has permissions to access S3
        :param role_session_name: the aws role session name
        """
        s3bucket = cls(bucket_name, role_arn, role_session_name)
        bucket = s3bucket.__s3_resource.Bucket(bucket_name)
        s3_path = urlparse(prefix).path.lstrip("/")
        local_dir = Path(dest)
        for obj in bucket.objects.filter(Prefix=s3_path):
            target = (
                obj.key
                if local_dir is None
                else local_dir / Path(obj.key).relative_to(s3_path)
            )
            target.parent.mkdir(parents=True, exist_ok=True)
            if obj.key[-1] == "/":
                continue
            s3bucket.__file_download_helper(bucket, obj.key, str(target))

    @classmethod
    def download_file(cls, bucket_name, key, dest, role_arn=None, role_session_name=None):
        """
        Download a single object from s3.

        :param bucket_name: The s3 bucket name
        :param key: The s3 key for the object to download
        :param dest: local destination
        :param role_arn: the arn of the role that has permissions to access S3
        :param role_session_name: the aws role session name
        """
        s3bucket = cls(bucket_name, role_arn, role_session_name)
        bucket = s3bucket.__s3_resource.Bucket(bucket_name)
        local_dir = Path(dest)
        file_name = key.split("/")[-1]
        target = Path(local_dir) / Path(file_name)
        return s3bucket.__file_download_helper(bucket, key, str(target))

    @staticmethod
    def __file_download_helper(bucket, key, path):
        try:
            bucket.download_file(key, path)
        except ClientError as e:
            raise S3DownloadFailureException(e)


    @classmethod
    def upload_file(cls, bucket_name, key, source, role_arn=None, role_session_name=None):
        """
        Upload a file to s3.

        :param bucket_name: The s3 bucket name
        :param key: The s3 key for the uploaded object
        :param source: local path of the file
        :param role_arn: the arn of the role that has permissions to access S3
        :param role_session_name: the aws role session name
        """
        s3bucket = cls(bucket_name, role_arn, role_session_name)
        try:
            s3bucket.__s3_client.upload_file(source, bucket_name, key)
        except ClientError as e:
            raise S3UploadFailureException(e)


class S3DownloadFailureException(Exception):
    pass


class S3UploadFailureException(Exception):
    pass
