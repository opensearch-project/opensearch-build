# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
# !/usr/bin/env python3

import argparse


import read_write_s3


class getBundleManifest:
    def parse_arguments(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-r", "--assume", help="Assume role")
        parser.add_argument("-s", "--session", help="Session name")
        parser.add_argument("-bkt", "--bktname", help="Bucketname")
        parser.add_argument("-ob", "--obj_bundle", help="ObjectPath in Bucket for Bundle")
        parser.add_argument("-om", "--obj_manifest", help="ObjectPath in Bucket for Manifest")
        parser.add_argument("-bp", "--bundlepath", help="Filepath for the bundle")
        parser.add_argument("-mp", "--manifestpath", help="Filepath for the manifest")

        args = parser.parse_args()

        return args

    def get_S3files(self, args):
        objectname = read_write_s3.read_write_files(args.assume, args.session)
        objectname.get_S3Objects(args.bktname, args.obj_bundle, args.obj_manifest, args.bundlepath, args.manifestpath)


getbm = getBundleManifest()
args = getbm.parse_arguments()
getbm.get_S3files(args)
