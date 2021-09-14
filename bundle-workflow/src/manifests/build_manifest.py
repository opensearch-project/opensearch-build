# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from aws.s3_bucket import S3Bucket
from manifests.manifest import Manifest

"""
A BuildManifest is an immutable view of the outputs from a build step
The manifest contains information about the product that was built (in the `build` section),
and the components that made up the build in the `components` section.

The format for schema version 1.0 is:
schema-version: 1.0
build:
  name: string
  version: string
  architecture: x64 or arm64
components:
  - name: string
    repository: URL of git repository
    ref: git ref that was built (sha, branch, or tag)
    commit_id: The actual git commit ID that was built (i.e. the resolved "ref")
    artifacts:
      maven:
        - maven/relative/path/to/artifact
        - ...
      plugins:
        - plugins/relative/path/to/artifact
        - ...
      libs:
        - libs/relative/path/to/artifact
        - ...
  - ...
"""


class BuildManifest(Manifest):
    def __init__(self, data):
        super().__init__(data)

        self.build = self.Build(data["build"])
        self.components = list(
            map(lambda entry: self.Component(entry), data["components"])
        )

    def to_dict(self):
        return {
            "schema-version": "1.0",
            "build": self.build.to_dict(),
            "components": list(
                map(lambda component: component.to_dict(), self.components)
            ),
        }

    @staticmethod
    def get_build_manifest_relative_location(build_id, opensearch_version, architecture):
        return f"builds/{opensearch_version}/{build_id}/{architecture}/manifest.yml"

    @staticmethod
    def from_s3(bucket_name, build_id, opensearch_version, architecture):
        local_path = str(os.getcwd())
        manifest_s3_path = BuildManifest.get_build_manifest_relative_location(build_id, opensearch_version, architecture)
        S3Bucket(bucket_name).download_file(manifest_s3_path, local_path)
        with open('manifest.yml', 'r') as file:
            return BuildManifest.from_file(file)

    class Build:
        def __init__(self, data):
            self.name = data["name"]
            self.version = data["version"]
            self.architecture = data["architecture"]
            self.id = data["id"]

        def to_dict(self):
            return {
                "name": self.name,
                "version": self.version,
                "architecture": self.architecture,
                "id": self.id,
            }

    class Component:
        def __init__(self, data):
            self.name = data["name"]
            self.repository = data["repository"]
            self.ref = data["ref"]
            self.commit_id = data["commit_id"]
            self.artifacts = data["artifacts"]
            self.version = data["version"]

        def to_dict(self):
            return {
                "name": self.name,
                "repository": self.repository,
                "ref": self.ref,
                "commit_id": self.commit_id,
                "artifacts": self.artifacts,
                "version": self.version,
            }
