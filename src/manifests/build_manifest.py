# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import itertools
import logging
import os

from aws.s3_bucket import S3Bucket
from manifests.build.build_manifest_1_0 import BuildManifest_1_0
from manifests.build.build_manifest_1_1 import BuildManifest_1_1
from manifests.manifest import Manifest

"""
A BuildManifest is an immutable view of the outputs from a build step
The manifest contains information about the product that was built (in the `build` section),
and the components that made up the build in the `components` section.

The format for schema version 1.2 is:
schema-version: "1.2"
build:
  name: string
  version: string
  platform: linux, darwin or windows
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
    components: list

    SCHEMA = {
        "build": {
            "required": True,
            "type": "dict",
            "schema": {
                "platform": {"required": True, "type": "string"},  # added in 1.2
                "architecture": {"required": True, "type": "string"},
                "id": {"required": True, "type": "string"},
                "name": {"required": True, "type": "string"},
                "version": {"required": True, "type": "string"},
            },
        },
        "schema-version": {"required": True, "type": "string", "allowed": ["1.2"]},
        "components": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "artifacts": {
                        "type": "dict",
                        "schema": {
                            "maven": {"type": "list"},
                            "plugins": {"type": "list"},
                            "dist": {"type": "list"},  # replaced "build" in 1.1
                            "core-plugins": {"type": "list"},
                            "libs": {"type": "list"},
                        },
                    },
                    "commit_id": {"required": True, "type": "string"},
                    "name": {"required": True, "type": "string"},
                    "ref": {"required": True, "type": "string"},
                    "repository": {"required": True, "type": "string"},
                    "version": {"required": True, "type": "string"},
                },
            },
        },
    }

    def __init__(self, data):
        super().__init__(data)

        self.build = self.Build(data["build"])
        self.components = BuildManifest.Components(data.get("components", []))

    def __to_dict__(self):
        return {"schema-version": "1.2", "build": self.build.__to_dict__(), "components": self.components.to_dict()}

    @staticmethod
    def get_build_manifest_relative_location(build_id, opensearch_version, platform, architecture):
        # TODO: use platform, https://github.com/opensearch-project/opensearch-build/issues/669
        return f"builds/{opensearch_version}/{build_id}/{architecture}/manifest.yml"

    @staticmethod
    def from_s3(bucket_name, build_id, opensearch_version, platform, architecture, work_dir=None):
        work_dir = work_dir if not None else str(os.getcwd())
        manifest_s3_path = BuildManifest.get_build_manifest_relative_location(build_id, opensearch_version, platform, architecture)
        S3Bucket(bucket_name).download_file(manifest_s3_path, work_dir)
        build_manifest = BuildManifest.from_path("manifest.yml")
        os.remove(os.path.realpath(os.path.join(work_dir, "manifest.yml")))
        return build_manifest

    class Build:
        def __init__(self, data):
            self.name = data["name"]
            self.version = data["version"]
            self.platform = data["platform"]
            self.architecture = data["architecture"]
            self.id = data["id"]

        def __to_dict__(self):
            return {
                "name": self.name,
                "version": self.version,
                "platform": self.platform,
                "architecture": self.architecture,
                "id": self.id,
            }

    class Components(dict):
        def __init__(self, data):
            super().__init__(map(lambda component: (component["name"], BuildManifest.Component(component)), data))

        def to_dict(self):
            return list(map(lambda component: component.__to_dict__(), self.values()))

        def select(self, focus=None):
            """
            Select components.

            :param str focus: Choose one component.
            :return: Collection of components.
            :raises ValueError: Invalid platform or component name specified.
            """
            selected, it = itertools.tee(filter(lambda component: component.matches(focus), self.values()))

            if not any(it):
                raise ValueError(f"No components matched focus={focus}.")

            return selected

    class Component:
        def __init__(self, data):
            self.name = data["name"]
            self.repository = data["repository"]
            self.ref = data["ref"]
            self.commit_id = data["commit_id"]
            self.artifacts = data.get("artifacts", [])
            self.version = data["version"]

        def matches(self, focus=None, platform=None):
            matches = ((not focus) or (self.name == focus)) and ((not platform) or (not self.platforms) or (platform in self.platforms))

            if not matches:
                logging.info(f"Skipping {self.name}")

            return matches

        def __to_dict__(self):
            return {
                "name": self.name,
                "repository": self.repository,
                "ref": self.ref,
                "commit_id": self.commit_id,
                "artifacts": self.artifacts,
                "version": self.version,
            }


BuildManifest.VERSIONS = {"1.0": BuildManifest_1_0, "1.1": BuildManifest_1_1, "1.2": BuildManifest}
