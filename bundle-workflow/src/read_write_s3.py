# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import boto3


class ReadWriteFiles:
    """
    get_S3Objects:Used for getting the files from S3
    bucket_name: Name of the bucket you want to get the file from
    role_arn: Amazon Resource Name (ARN) of the role that you want to assume
    Here, default value for role is taken. Can be changed through -a <role-name>
    role_session_name: Name for the session
    Here, default value for session is taken. Can be changed through -s <session-name>
    bucket_bundle: Object path from where you want to get the bundle
    path_to_save_bundle: Path where you want to save the bundle at
    """
    def __init__(self, role_arn, role_session_name):
        self.role_arn = role_arn
        self.role_session_name = role_session_name

    def get_S3_objects(self, bucket_name, bucket_bundle, path_to_save_bundle=None):
        sts_connection = boto3.client('sts')
        assumed_role = sts_connection.assume_role(
            RoleArn=self.role_arn,
            RoleSessionName=self.role_session_name,
            DurationSeconds=3600)['Credentials']

        boto3.client('s3',
                     aws_access_key_id=assumed_role['AccessKeyId'],
                     aws_secret_access_key=assumed_role['SecretAccessKey'],
                     aws_session_token=assumed_role['SessionToken'])

        try:
            s3_resource = boto3.resource('s3')
            my_bucket = s3_resource.Bucket(bucket_name)
            objects = my_bucket.objects.filter(Prefix=bucket_bundle)
            for obj in objects:
                target = obj.key if path_to_save_bundle is None \
                    else os.path.join(path_to_save_bundle, os.path.relpath(obj.key, bucket_bundle))
                if not os.path.exists(os.path.dirname(target)):
                    os.makedirs(os.path.dirname(target))
                if obj.key[-1] == '/':
                    continue
                my_bucket.download_file(obj.key, target)
        except Exception as e:
            print(e)
    """
    put_S3Objects:Used for putting the files into S3
    file_name: The file that you want to put in the S3 bucket
    file_path: The Object path where you want to save the file
    """
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
        except Exception as e:
            print(e)
