# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.

import os
from manifests.bundle_manifest import BundleManifest
from aws.s3_bucket import S3Bucket


class BundleManifestProvider:
    @staticmethod
    def get_tarball_relative_location(build_id, opensearch_version, architecture):
        return f"bundles/{opensearch_version}/{build_id}/{architecture}/opensearch-{opensearch_version}-linux-{architecture}.tar.gz"

    @staticmethod
    def get_tarball_name(opensearch_version, architecture):
        return f"opensearch-{opensearch_version}-linux-{architecture}.tar.gz"

    @staticmethod
    def get_bundle_manifest_relative_location(build_id, opensearch_version, architecture):
        return f"bundles/{opensearch_version}/{build_id}/{architecture}/manifest.yml"

    @staticmethod
    def load_manifest(bucket_name, build_id, opensearch_version, architecture):
        local_path = str(os.getcwd())
        manifest_s3_path = BundleManifestProvider.get_bundle_manifest_relative_location(build_id, opensearch_version, architecture)
        S3Bucket(bucket_name).download_file(manifest_s3_path, local_path)
        with open('manifest.yml', 'r') as file:
            return BundleManifest.from_file(file)



