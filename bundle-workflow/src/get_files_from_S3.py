# !/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.


import argparse

import read_write_s3


class GetBundleManifest:
    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-a", "--assume_role", nargs="?", default="${OPENSEARCH_TESTING_ROLE}", help="Assume role")
        parser.add_argument("-s", "--session", nargs="?", default="get-files-session", help="Session name")
        parser.add_argument("-b", "--bucket_name", help="Bucketname", required=True)
        parser.add_argument("-o", "--object_bundle", help="ObjectPath in Bucket for Bundle", required=True)
        parser.add_argument("-bp", "--bundle_path", help="Path for storing the bundle locally", required=True)

        args = parser.parse_args()
        return args

    def download_files_from_S3(self, args):
        objectname = read_write_s3.ReadWriteFiles(args.assume_role, args.session)
        objectname.get_S3_objects(args.bucket_name, args.object_bundle, args.bundle_path)


getbm = GetBundleManifest()
args = getbm.parse_arguments()
getbm.download_files_from_S3(args)
