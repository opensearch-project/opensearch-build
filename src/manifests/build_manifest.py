# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from manifests.build.build_manifest_1_0 import BuildManifest_1_0
from manifests.build.build_manifest_1_1 import BuildManifest_1_1
from manifests.component_manifest import ComponentManifest

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


class BuildManifest(ComponentManifest):
    components: list

    VERSIONS = {
        "1.0": BuildManifest_1_0,
        "1.1": BuildManifest_1_1,
        # "1.2" : current
    }

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

    def __to_dict__(self):
        return {
            "schema-version": "1.2",
            "build": self.build.__to_dict__(),
            "components": self.components.__to_dict__()
        }

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
                "id": self.id
            }

    class Components(ComponentManifest.Components):
        @classmethod
        def __create__(self, data):
            return BuildManifest.Component(data)

    class Component(ComponentManifest.Component):
        def __init__(self, data):
            super().__init__(data)
            self.repository = data["repository"]
            self.ref = data["ref"]
            self.commit_id = data["commit_id"]
            self.artifacts = data.get("artifacts", {})
            self.version = data["version"]

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
