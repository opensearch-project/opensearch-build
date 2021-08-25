# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import boto3


class read_write_files:

    # get_S3Objects:Used for getting the files from S3
    # bucketname: Name of the bucket you want to get the file from
    # RoleArn: Amazon Resource Name (ARN) of the role that you want to assume
    # RoleSessionName: Name for the session
    # bucket_bundle: Object path from where you want to get the bundle
    # bucket_manifest: Object path from where you want to get the manifest
    # path_tosave_Bundle: Path where you want to save the bundle at
    # path_tosave_Manifest: Path where you want to save the manifest at
    def get_S3Objects(self, bucketname, RoleArn, RoleSessionName, bucket_bundle, bucket_manifest, path_tosave_Bundle, path_tosave_Manifest):
        sts_connection = boto3.client('sts')
        acct_b = sts_connection.assume_role(
            RoleArn=RoleArn,
            RoleSessionName=RoleSessionName,
            DurationSeconds=3600)['Credentials']

        client = boto3.client(
                    's3',
                    aws_access_key_id=acct_b['AccessKeyId'],
                    aws_secret_access_key=acct_b['SecretAccessKey'],
                    aws_session_token=acct_b['SessionToken'])

        try:
            client.download_file(bucketname, bucket_bundle, path_tosave_Bundle)
            client.download_file(bucketname, bucket_manifest, path_tosave_Manifest)
        except:
            print("An exception occurred. No file is present in the bucket.")

    # put_S3Objects:Used for putting the files into S3
    # filename: The file that you want to put in the S3 bucket
    # filePath: The Object path where you want to save the file
    def put_S3Objects(self, bucketname, RoleArn, RoleSessionName, filename, filePath):
        sts_connection = boto3.client('sts')
        acct_b = sts_connection.assume_role(
            RoleArn=RoleArn,
            RoleSessionName=RoleSessionName,
            DurationSeconds=3600)['Credentials']


        client = boto3.client(
                    's3',
                     aws_access_key_id=acct_b['AccessKeyId'],
                     aws_secret_access_key=acct_b['SecretAccessKey'],
                     aws_session_token=acct_b['SessionToken'])

        try:
            client.upload_file(filename, bucketname, filePath)
        except:
            print("An exception occurred. No file found for uploading.")

    print("Done.")