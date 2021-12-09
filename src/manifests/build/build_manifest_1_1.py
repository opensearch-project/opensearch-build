# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Any

from manifests.component_manifest import Component, ComponentManifest, Components

"""
A BuildManifest is an immutable view of the outputs from a build step
The manifest contains information about the product that was built (in the `build` section),
and the components that made up the build in the `components` section.

The format for schema version 1.1 is:
schema-version: "1.1"
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


class BuildManifest_1_1(ComponentManifest['BuildManifest_1_1', 'BuildComponents_1_1']):
    SCHEMA = {
        "build": {
            "required": True,
            "type": "dict",
            "schema": {
                "architecture": {"required": True, "type": "string"},
                "id": {"required": True, "type": "string"},
                "name": {"required": True, "type": "string"},
                "version": {"required": True, "type": "string"},
            },
        },
        "schema-version": {"required": True, "type": "string", "allowed": ["1.1"]},
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

    def __init__(self, data: Any):
        super().__init__(data)
        self.build = self.Build(data["build"])
        self.components = BuildComponents_1_1(data.get("components", []))  # type: ignore[assignment]

    def __to_dict__(self) -> dict:
        return {
            "schema-version": "1.1",
            "build": self.build.__to_dict__(),
            "components": self.components.__to_dict__()
        }

    class Build:
        def __init__(self, data: Any):
            self.name: str = data["name"]
            self.version = data["version"]
            self.architecture = data["architecture"]
            self.id = data["id"]

        def __to_dict__(self) -> dict:
            return {
                "name": self.name,
                "version": self.version,
                "architecture": self.architecture,
                "id": self.id
            }

        @property
        def filename(self) -> str:
            return self.name.lower().replace(" ", "-")


class BuildComponents_1_1(Components['BuildComponent_1_1']):
    @classmethod
    def __create__(self, data: Any) -> 'BuildComponent_1_1':
        return BuildComponent_1_1(data)


class BuildComponent_1_1(Component):
    def __init__(self, data: Any):
        super().__init__(data)
        self.repository = data["repository"]
        self.ref = data["ref"]
        self.commit_id = data["commit_id"]
        self.artifacts = data.get("artifacts", {})
        self.version = data["version"]

    def __to_dict__(self) -> dict:
        return {
            "name": self.name,
            "repository": self.repository,
            "ref": self.ref,
            "commit_id": self.commit_id,
            "artifacts": self.artifacts,
            "version": self.version,
        }
