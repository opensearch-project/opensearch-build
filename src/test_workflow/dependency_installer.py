# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

from aws.s3_bucket import S3Bucket


class DependencyInstaller:
    """
    Provides a dependency installer for the test suites.
    """

    ARTIFACT_S3_BUCKET = "artifact-bucket-stack-buildbucket-9omh0hnpg12q"

    def __init__(self, build):
        self.build_id = build.id
        self.version = build.version
        self.platform = build.platform
        self.architecture = build.architecture
        self.s3_bucket = S3Bucket(self.ARTIFACT_S3_BUCKET)
        self.s3_maven_location = f"builds/{self.version}/{self.build_id}/{self.platform}/{self.architecture}/maven/org/opensearch"
        self.s3_build_location = f"builds/{self.version}/{self.build_id}/{self.platform}/{self.architecture}/plugins"
        self.maven_local_path = os.path.join(os.path.expanduser("~"), ".m2/repository/org/opensearch/")

    def install_all_maven_dependencies(self):
        """
        Downloads all pre-built maven dependencies from S3 bucket
        """
        logging.info("Downloading all pre-built maven dependencies from s3")
        self.s3_bucket.download_folder(f"{self.s3_maven_location}", self.maven_local_path)
        logging.info("Successfully downloaded maven dependencies")

    def install_build_dependencies(self, dependency_dict, custom_local_path):
        """
        Downloads the build dependencies from S3 and puts them on the given custom path
        for each dependency in the dependencies.

        :param dependencies: dictionary of dependency names with version for which the build artifacts need to be downloaded.
        Example: {'opensearch-job-scheduler':'1.1.0.0'}
        """
        os.makedirs(custom_local_path, exist_ok=True)
        for dependency, version in dependency_dict.items():
            s3_path = f"{self.s3_build_location}/{dependency}-{version}.zip"
            self.s3_bucket.download_file(s3_path, custom_local_path)
