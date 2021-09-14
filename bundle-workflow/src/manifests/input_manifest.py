# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

"""
An InputManifest is an immutable view of the input manifest for the build system.
The manifest contains information about the product that is being built (in the `build` section),
and the components that make up the product in the `components` section.

The format for schema version 1.0 is:
schema-version: "1.0"
build:
  name: string
  version: string
components:
  - name: string
    repository: URL of git repository
    ref: git ref to build (sha, branch, or tag)
    working_directory: optional relative directory to run commands in
    checks: CI checks
      - check1
      - ...
  - ...
"""

from manifests.manifest import Manifest


class InputManifest(Manifest):
    def __init__(self, data):
        super().__init__(data)

        self.build = self.Build(data["build"])
        self.components = list(
            map(lambda entry: self.Component(entry), data["components"])
        )

    def __to_dict__(self):
        return {
            "schema-version": "1.0",
            "build": self.build.__to_dict__(),
            "components": list(
                map(lambda component: component.__to_dict__(), self.components)
            ),
        }

    class Build:
        def __init__(self, data):
            self.name = data["name"]
            self.version = data["version"]

        def __to_dict__(self):
            return {"name": self.name, "version": self.version}

    class Component:
        def __init__(self, data):
            self.name = data["name"]
            self.repository = data["repository"]
            self.ref = data["ref"]
            self.working_directory = data.get("working_directory", None)
            self.checks = data.get("checks", [])

        def __to_dict__(self):
            return Manifest.compact(
                {
                    "name": self.name,
                    "repository": self.repository,
                    "ref": self.ref,
                    "working_directory": self.working_directory,
                    "checks": self.checks,
                }
            )
