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


def file_download_helper(bucket, key, path):
    try:
        bucket.download_file(key, path)
    except ClientError as e:  # TODO: handle the right exception
        if e.response["Error"]["Code"] == "404":
            print("The object does not exist.")
        else:
            raise


class S3ReadWrite:
    def __init__(self, role_arn=None, role_session_name=None):
        self.role_arn = (
            role_arn if role_arn is not None else os.environ.get("JENKINS_S3_ROLE_ARN")
        )
        self.role_session_name = (
            role_session_name
            if role_session_name is not None
            else os.environ.get("JENKINS_S3_ROLE_SESSION_NAME")
        )
        self.s3_resource = boto3.resource("s3")
        self.s3_client = boto3.client("s3")
        # TODO: make sts role logic work for local dev
        # sts_connection = boto3.client('sts')
        # assumed_role = sts_connection.assume_role(
        #     RoleArn=self.role_arn,
        #     RoleSessionName=self.role_session_name,
        #     DurationSeconds=3600)['Credentials']
        # self.s3_client = boto3.client('s3', aws_access_key_id=assumed_role['AccessKeyId'], aws_secret_access_key=assumed_role['SecretAccessKey'],
        #                       aws_session_token=assumed_role['SessionToken'])
        # self.s3_resource = boto3.resource('s3', aws_access_key_id=assumed_role['AccessKeyId'], aws_secret_access_key=assumed_role['SecretAccessKey'],
        #                                 aws_session_token=assumed_role['SessionToken'])

    def download_folder(self, s3_uri, local_dir):
        """
        Download the contents of a folder directory

        :param s3_uri: the s3 uri to the top level of the files you wish to download
        :param local_dir: a relative or absolute directory path in the local file system
        """
        bucket = self.s3_resource.Bucket(urlparse(s3_uri).hostname)
        s3_path = urlparse(s3_uri).path.lstrip("/")
        local_dir = Path(local_dir)
        for obj in bucket.objects.filter(Prefix=s3_path):
            target = (
                obj.key
                if local_dir is None
                else local_dir / Path(obj.key).relative_to(s3_path)
            )
            target.parent.mkdir(parents=True, exist_ok=True)
            if obj.key[-1] == "/":
                continue
            file_download_helper(bucket, obj.key, str(target))

    def download_file(self, s3_uri, local_dir, file_name=None):
        """
        Download a single object from s3.

        :param s3_uri: s3 location of the file
        :param local_dir: location to download the file at
        :param file_name: (Optional) If provided, overrides the filename locally with file_name.
        """
        bucket = self.s3_resource.Bucket(urlparse(s3_uri).hostname)
        key = urlparse(s3_uri).path.lstrip("/")
        file_name = file_name if file_name is not None else key.split("/")[-1]
        target = Path(local_dir) / Path(file_name)
        file_download_helper(bucket, key, str(target))

    def upload_file(self, file_path, bucket_name, object_name):
        """
        Upload a file to s3.

        :param file_path: local path of the file to upload
        :param bucket_name: s3 bucket name
        :param object_name: s3 object name for the file
        """
        try:
            response = self.s3_client.upload_file(file_path, bucket_name, object_name)
        except ClientError as e:
            return False
        return True
