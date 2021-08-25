import boto3
import json

class read_write_files:

    #get_S3Objects:Used for getting the files from s3
    def get_S3Objects(self, bucketname, RoleArn, RoleSessionName, bucket_bundle, bucket_manifest, path_tosave_Bundle, path_tosave_Manifest):
        sts_connection = boto3.client('sts')
        acct_b = sts_connection.assume_role(
            RoleArn=RoleArn,
            RoleSessionName=RoleSessionName,
            DurationSeconds=3600)['Credentials']
        print (acct_b)

        client = boto3.client('s3',
                              aws_access_key_id=acct_b['AccessKeyId'],
                              aws_secret_access_key=acct_b['SecretAccessKey'],
                              aws_session_token=acct_b['SessionToken'])

        try:
            result_bundle = client.download_file(bucketname, bucket_bundle, path_tosave_Bundle)
            result_manifest = client.download_file(bucketname, bucket_manifest, path_tosave_Manifest)
        except:
            print("An exception occurred. No file is present in the bucket.")

    #put_S3Objects:Used for putting the files into s3
    def put_S3Objects(self, bucketname, RoleArn, RoleSessionName, filename, filePath):
        sts_connection = boto3.client('sts')
        acct_b = sts_connection.assume_role(
            RoleArn=RoleArn,
            RoleSessionName=RoleSessionName,
            DurationSeconds=3600)['Credentials']
        print (acct_b)

        client = boto3.client('s3',
                              aws_access_key_id=acct_b['AccessKeyId'],
                              aws_secret_access_key=acct_b['SecretAccessKey'],
                              aws_session_token=acct_b['SessionToken'])

        try:
            result = client.upload_file(filename, bucketname, filePath)
        except:
            print("An exception occurred. No file found for uploading.")



