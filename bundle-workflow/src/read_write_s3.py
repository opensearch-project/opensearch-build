# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import boto3


class ReadWriteFiles:

    # get_S3Objects:Used for getting the files from S3
    # bucket_name: Name of the bucket you want to get the file from
    # role_arn: Amazon Resource Name (ARN) of the role that you want to assume
    # role_session_name: Name for the session
    # bucket_bundle: Object path from where you want to get the bundle
    # bucket_manifest: Object path from where you want to get the manifest
    # path_to_save_bundle: Path where you want to save the bundle at
    # path_to_save_manifest: Path where you want to save the manifest at
    def __init__(self, role_arn, role_session_name):
        self.role_arn = role_arn
        self.role_session_name = role_session_name

    def get_S3_objects(self, bucket_name, bucket_bundle, bucket_manifest, path_to_save_bundle, path_to_save_manifest):
        sts_connection = boto3.client('sts')
        assumed_role = sts_connection.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=self.role_session_name,
            DurationSeconds=3600)['Credentials']

        client = boto3.client('s3', aws_access_key_id=assumed_role['AccessKeyId'], aws_secret_access_key=assumed_role['SecretAccessKey'],
                              aws_session_token=assumed_role['SessionToken'])

        try:
            client.download_file(bucket_name, bucket_bundle, path_to_save_bundle)
            client.download_file(bucket_name, bucket_manifest, path_to_save_manifest)
        except:
            print("An exception occurred. No file is present in the bucket.")

    # put_S3Objects:Used for putting the files into S3
    # file_name: The file that you want to put in the S3 bucket
    # file_path: The Object path where you want to save the file
    def put_S3_objects(self, bucket_name, file_name, file_path):
        sts_connection = boto3.client('sts')
        assumed_role = sts_connection.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=self.role_session_name,
            DurationSeconds=3600)['Credentials']

        client = boto3.client('s3', aws_access_key_id=assumed_role['AccessKeyId'], aws_secret_access_key=assumed_role['SecretAccessKey'],
                              aws_session_token=assumed_role['SessionToken'])

        try:
            client.upload_file(file_name, bucket_name, file_path)
        except:
            print("An exception occurred. No file found for uploading.")
