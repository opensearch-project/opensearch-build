# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import os

import boto3
import botocore


class S3Bucket:
    """
    get_S3Objects:Used for getting the files from S3
    bucket_name: Name of the bucket you want to get the file from
    role_arn: Amazon Resource Name (ARN) of the role that you want to assume
    Here, default value for role is taken. Can be changed through -a <role-name>
    role_session_name: Name for the session
    Here, default value for session is taken. Can be changed through -s <session-name>
    prefix: Object path from where you want to get the bundle
    dest: Path where you want to save the bundle at
    """
    def __init__(self, role_arn, role_session_name, bucket_name):
        self.role_arn = role_arn
        self.role_session_name = role_session_name
        self.bucket_name = bucket_name
        sts_connection = boto3.client('sts')
        assumed_role = sts_connection.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=self.role_session_name,
            DurationSeconds=3600)['Credentials']
        self.client = boto3.client('s3',
                                   aws_access_key_id=assumed_role['AccessKeyId'],
                                   aws_secret_access_key=assumed_role['SecretAccessKey'],
                                   aws_session_token=assumed_role['SessionToken'])

    def download(self, prefix, dest, file):

        try:
            if (file == "folder"):
                s3_resource = boto3.resource('s3')
                my_bucket = s3_resource.Bucket(self.bucket_name)
                objects = my_bucket.objects.filter(Prefix=prefix)
                for obj in objects:
                    target = obj.key if dest is None \
                        else os.path.join(dest, os.path.relpath(obj.key, prefix))
                    if not os.path.exists(os.path.dirname(target)):
                        os.makedirs(os.path.dirname(target))
                    if obj.key[-1] == '/':
                        continue
                    my_bucket.download_file(obj.key, target)
            else:
                self.client.download_file(self.bucket_name, prefix, dest)

        except botocore.exceptions.ClientError as e:
            error_message = ''.join(e.args)
            raise ValueError('ERROR DOWNLOADING FILE FROM AWS BUCKET ' + error_message)
        except OSError:
            raise ValueError("The error is either: Wrong file or file path provided.")
    """
    put_S3Objects:Used for putting the files into S3
    file_name: The file that you want to put in the S3 bucket
    file_path: The Object path where you want to save the file
    """
    def upload(self, file_name, file_path):
        try:
            self.client.upload_file(file_name, self.bucket_name, file_path)
        except Exception as e:
            raise ValueError("The Error is: " + e.__str__())
