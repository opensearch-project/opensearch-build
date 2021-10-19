# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import unittest
from unittest.mock import MagicMock, call, patch

from botocore.exceptions import ClientError

from aws.s3_bucket import S3Bucket, S3DownloadError, STSError

mock_sts = MagicMock()
mock_s3_resource = MagicMock()
mock_s3_client = MagicMock()
bucket_name = "unitTestBucket"


class MockS3Response:
    class ObjectSummary:
        def __init__(self, bucket_name, key):
            self.bucket_name = bucket_name
            self.key = key

    @staticmethod
    def mock_list_objects_response(*args, **kwargs):
        response = [
            MockS3Response.ObjectSummary(bucket_name, "tests/"),
            MockS3Response.ObjectSummary(bucket_name, "tests/1.1.0/"),
            MockS3Response.ObjectSummary(bucket_name, "tests/1.1.0/x64/"),
            MockS3Response.ObjectSummary(bucket_name, "tests/1.1.0/x64/opensearch-1.1.0-linux-x64.tar.gz"),
            MockS3Response.ObjectSummary(bucket_name, "maven/org/opensearch/xyz-1.1.0.tar.gz"),
        ]
        mock_s3_resource.Bucket(bucket_name).objects.filter.return_value = response
        return mock_s3_resource


class MockSTSResponse:
    @staticmethod
    def successful_response():
        return {
            "AssumedRoleUser": {
                "Arn": "arn:aws:sts::123456789012:assumed-role/opensearch-test/dummy-session",
                "AssumedRoleId": "AROA3QLFMSBFVM2ZRZRBW:dummy-session",
            },
            "Credentials": {
                "AccessKeyId": "AFRI3QLFMSBFYALQPMZE",
                "Expiration": "2021-09-03T15:03:20Z",
                "SecretAccessKey": "qvK2qOg5EzlqVAhtuxQd+JsNnU0knG2xFraFDMGO",
                "SessionToken": "FwoGZXIvY+Gjg77ZBj5IN2i3v",
            },
            "ResponseMetadata": {
                "HTTPHeaders": {
                    "content-length": "1052",
                    "content-type": "text/xml",
                    "date": "Fri, 03 Sep 2028 22:58:20 GMT",
                    "x-amzn-requestid": "e75e483e-ab03-4837-88e0-8032ffc46e43",
                },
                "HTTPStatusCode": 200,
                "RequestId": "e75e483e-ab03-4837-88e0-8032ffc46e43",
                "RetryAttempts": 0,
            },
        }


class TestS3Bucket(unittest.TestCase):
    def setUp(self):
        pass

    def get_mock_boto_client(*args, **kwargs):
        mock_sts.reset_mock()
        mock_s3_client.reset_mock()
        if args[0] == "sts":
            return mock_sts
        else:
            return mock_s3_client

    @patch("boto3.resource")
    @patch("boto3.client", side_effect=get_mock_boto_client)
    def test_s3_bucket_obj(self, mock_boto_client, mock_boto_resource):
        expected_sts_response = MockSTSResponse.successful_response()
        mock_sts.assume_role.return_value = expected_sts_response
        S3Bucket(bucket_name)
        calls = [
            call("sts"),
            call(
                "s3",
                aws_access_key_id=expected_sts_response["Credentials"]["AccessKeyId"],
                aws_secret_access_key=expected_sts_response["Credentials"]["SecretAccessKey"],
                aws_session_token=expected_sts_response["Credentials"]["SessionToken"],
            ),
        ]
        mock_boto_client.assert_has_calls(calls)
        mock_boto_resource.assert_called_once_with(
            "s3",
            aws_access_key_id=expected_sts_response["Credentials"]["AccessKeyId"],
            aws_secret_access_key=expected_sts_response["Credentials"]["SecretAccessKey"],
            aws_session_token=expected_sts_response["Credentials"]["SessionToken"],
        )

    @patch("boto3.client")
    def test_s3_bucket_obj_sts_error(self, mock_boto_client):
        expected_sts_response = MockSTSResponse.successful_response()
        mock_boto_client("sts").assume_role.side_effect = ClientError(error_response={"Error": {"Code": "403"}}, operation_name="AssumeRole")
        mock_boto_client("sts").assume_role.return_value = expected_sts_response
        with self.assertRaises(STSError):
            S3Bucket(bucket_name)
        mock_boto_client("s3").assert_not_called()

    @patch("boto3.client")
    def test_upload_file(self, mock_boto_client):
        expected_sts_response = MockSTSResponse.successful_response()
        mock_boto_client("sts").assume_role.return_value = expected_sts_response
        s3bucket = S3Bucket(bucket_name)
        s3bucket.upload_file(
            "tests/1.1.0/x64/opensearch-1.1.0-linux-x64.tar.gz",
            os.path.join("tmp", "opensearch-1.1.0-linux-x64.tar.gz"),
        )
        mock_boto_client("s3").upload_file.assert_called_once_with(
            os.path.join("tmp", "opensearch-1.1.0-linux-x64.tar.gz"),
            bucket_name,
            "tests/1.1.0/x64/opensearch-1.1.0-linux-x64.tar.gz",
        )

    @patch("boto3.client")
    @patch("boto3.resource", side_effect=MockS3Response.mock_list_objects_response)
    def test_download_folder(self, mock_boto_resource, mock_boto_client):
        expected_sts_response = MockSTSResponse.successful_response()
        mock_boto_client("sts").assume_role.return_value = expected_sts_response
        folder_path = "/"
        s3bucket = S3Bucket(bucket_name)
        s3bucket.download_folder(folder_path, "tmp")
        calls = [
            call(
                "tests/1.1.0/x64/opensearch-1.1.0-linux-x64.tar.gz",
                os.path.join("tmp", "tests", "1.1.0", "x64", "opensearch-1.1.0-linux-x64.tar.gz"),
            ),
            call(
                "maven/org/opensearch/xyz-1.1.0.tar.gz",
                os.path.join("tmp", "maven", "org", "opensearch", "xyz-1.1.0.tar.gz"),
            ),
        ]
        mock_s3_resource.Bucket(bucket_name).download_file.assert_has_calls(calls)
        self.assertTrue(mock_s3_resource.Bucket(bucket_name).download_file.call_count, 2)

    @patch("boto3.client")
    @patch("boto3.resource", side_effect=MockS3Response.mock_list_objects_response)
    def test_download_file(self, mock_boto_resource, mock_boto_client):
        expected_sts_response = MockSTSResponse.successful_response()
        mock_boto_client("sts").assume_role.return_value = expected_sts_response
        key = "tests/1.1.0/x64/opensearch-1.1.0-linux-x64.tar.gz"
        s3bucket = S3Bucket(bucket_name)
        s3bucket.download_file(key, "tmp")
        calls = [
            call(key, os.path.join("tmp", "opensearch-1.1.0-linux-x64.tar.gz")),
        ]
        mock_s3_resource.Bucket(bucket_name).download_file.assert_has_calls(calls)
        self.assertTrue(mock_s3_resource.Bucket(bucket_name).download_file.call_count, 1)

    @patch("boto3.client")
    @patch("boto3.resource")
    def test_download_file_failure(self, mock_boto_resource, mock_boto_client):
        mock_boto_client("sts").assume_role.return_value = MockSTSResponse.successful_response()
        file_path = os.path.join("tests", "1.1.0", "x64", "opensearch-1.1.0-linux-x64.tar.gz")
        mock_boto_resource("s3").Bucket(bucket_name).download_file.side_effect = ClientError(
            error_response={"Error": {"Code": "403"}}, operation_name="GetObject"
        )
        s3bucket = S3Bucket(bucket_name)
        with self.assertRaises(S3DownloadError):
            s3bucket.download_file(file_path, "tmp")
