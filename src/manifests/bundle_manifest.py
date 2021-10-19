# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os

from aws.s3_bucket import S3Bucket
from manifests.manifest import Manifest


class BundleManifest(Manifest):
    """
    A BundleManifest is an immutable view of the outputs from a assemble step
    The manifest contains information about the bundle that was built (in the `assemble` section),
    and the components that made up the bundle in the `components` section.

    The format for schema version 1.1 is:
        schema-version: "1.1"
        build:
          name: string
          version: string
          platform: linux, darwin or windows
          architecture: x64 or arm64
          location: /relative/path/to/tarball
        components:
          - name: string
            repository: URL of git repository
            ref: git ref that was built (sha, branch, or tag)
            commit_id: The actual git commit ID that was built (i.e. the resolved "ref")
            location: /relative/path/to/artifact
    """

    SCHEMA = {
        "build": {
            "required": True,
            "type": "dict",
            "schema": {
                "platform": {"required": True, "type": "string"},
                "architecture": {"required": True, "type": "string"},
                "id": {"required": True, "type": "string"},
                "location": {"required": True, "type": "string"},
                "name": {"required": True, "type": "string"},
                "version": {"required": True, "type": "string"},
            },
        },
        "schema-version": {"required": True, "type": "string", "allowed": ["1.1"]},
        "components": {
            "required": True,
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "commit_id": {"required": True, "type": "string"},
                    "location": {"required": True, "type": "string"},
                    "name": {"required": True, "type": "string"},
                    "ref": {"required": True, "type": "string"},
                    "repository": {"required": True, "type": "string"},
                },
            },
        },
    }

    def __init__(self, data):
        super().__init__(data)
        self.build = self.Build(data["build"])
        self.components = list(map(lambda entry: self.Component(entry), data["components"]))

    def __to_dict__(self):
        return {
            "schema-version": "1.1",
            "build": self.build.__to_dict__(),
            "components": list(map(lambda component: component.__to_dict__(), self.components)),
        }

    @staticmethod
    def from_s3(bucket_name, build_id, opensearch_version, platform, architecture, work_dir=None):
        work_dir = work_dir if not None else str(os.getcwd())
        manifest_s3_path = BundleManifest.get_bundle_manifest_relative_location(build_id, opensearch_version, platform, architecture)
        S3Bucket(bucket_name).download_file(manifest_s3_path, work_dir)
        bundle_manifest = BundleManifest.from_path(os.path.join(work_dir, "manifest.yml"))
        os.remove(os.path.realpath(os.path.join(work_dir, "manifest.yml")))
        return bundle_manifest

    @staticmethod
    def get_tarball_relative_location(build_id, opensearch_version, platform, architecture):
        # TODO: use platform, https://github.com/opensearch-project/opensearch-build/issues/669
        return f"bundles/{opensearch_version}/{build_id}/{architecture}/opensearch-{opensearch_version}-{platform}-{architecture}.tar.gz"

    @staticmethod
    def get_tarball_name(opensearch_version, platform, architecture):
        return f"opensearch-{opensearch_version}-{platform}-{architecture}.tar.gz"

    @staticmethod
    def get_bundle_manifest_relative_location(build_id, opensearch_version, platform, architecture):
        # TODO: use platform, https://github.com/opensearch-project/opensearch-build/issues/669
        return f"bundles/{opensearch_version}/{build_id}/{architecture}/manifest.yml"

    class Build:
        def __init__(self, data):
            self.name = data["name"]
            self.version = data["version"]
            self.platform = data["platform"]
            self.architecture = data["architecture"]
            self.location = data["location"]
            self.id = data["id"]

        def __to_dict__(self):
            return {
                "name": self.name,
                "version": self.version,
                "platform": self.platform,
                "architecture": self.architecture,
                "location": self.location,
                "id": self.id,
            }

    class Component:
        def __init__(self, data):
            self.name = data["name"]
            self.repository = data["repository"]
            self.ref = data["ref"]
            self.commit_id = data["commit_id"]
            self.location = data["location"]

        def __to_dict__(self):
            return {
                "name": self.name,
                "repository": self.repository,
                "ref": self.ref,
                "commit_id": self.commit_id,
                "location": self.location,
            }
