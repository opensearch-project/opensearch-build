# !/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
import argparse
from enum import Enum

import read_write_s3


class DocumentType(Enum):
    FILE = "file"
    FOLDER = "folder"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class GetBundleManifest:

    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-a", "--assume_role", nargs="?", default="os.getenv('OPENSEARCH_TESTING_ROLE')", help="Assume role")
        parser.add_argument("-s", "--session", nargs="?", default="get-files-session", help="Session name")
        parser.add_argument("-b", "--bucket_name", help="Bucketname", required=True)
        parser.add_argument("-o", "--object_bundle", help="ObjectPath in Bucket for Bundle", required=True)
        parser.add_argument("-bp", "--bundle_path", help="Path for storing the bundle locally", required=True)
        parser.add_argument("-f", "--file", help="Parameter for either file or folder", default="folder")

        args = parser.parse_args()

        if not (DocumentType.has_value(args.file)):
            raise ValueError("The document type given is not present. Document types to be given are file or folder")
        return args

    def download_files_from_S3(self, args):
        objectname = read_write_s3.S3Bucket(args.assume_role, args.session, args.bucket_name)
        objectname.download(args.object_bundle, args.bundle_path, args.file)


getbm = GetBundleManifest()
args = getbm.parse_arguments()
getbm.download_files_from_S3(args)
