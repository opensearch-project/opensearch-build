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
    SCHEMA = {
        "build": {
            "required": True,
            "type": "dict",
            "schema": {
                "name": {"required": True, "type": "string"},
                "version": {"required": True, "type": "string"},
            },
        },
        "ci": {
            "required": False,
            "type": "dict",
            "schema": {
                "image": {
                    "required": False,
                    "type": "dict",
                    "schema": {
                        "name": {"required": True, "type": "string"},
                        "args": {"required": False, "type": "string"}
                    },
                },
            },
        },
        "schema-version": {"required": True, "type": "string", "allowed": ["1.0"]},
        "components": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "name": {"required": True, "type": "string"},
                    "ref": {"required": True, "type": "string"},
                    "repository": {"required": True, "type": "string"},
                    "working_directory": {"type": "string"},
                    "checks": {
                        "type": "list",
                        "schema": {"anyof": [{"type": "string"}, {"type": "dict"}]},
                    },
                },
            },
        },
    }

    def __init__(self, data):
        super().__init__(data)

        self.build = self.Build(data["build"])
        self.ci = self.Ci(data.get("ci", None))
        self.components = list(map(lambda entry: self.Component(entry), data["components"]))

    def __to_dict__(self):
        return {
            "schema-version": "1.0",
            "build": self.build.__to_dict__(),
            "ci": None if self.ci is None else self.ci.__to_dict__(),
            "components": list(map(lambda component: component.__to_dict__(), self.components)),
        }

    class Ci:
        def __init__(self, data):
            self.image = None if data is None else self.Image(data.get("image", None))

        def __to_dict__(self):
            return None if self.image is None else {"image": self.image.__to_dict__()}

        class Image:
            def __init__(self, data):
                self.name = data["name"]
                self.args = data.get("args", None)

            def __to_dict__(self):
                return {"name": self.name, "args": self.args}

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
            self.checks = list(map(lambda entry: InputManifest.Check(entry), data.get("checks", [])))

        def __to_dict__(self):
            return Manifest.compact(
                {
                    "name": self.name,
                    "repository": self.repository,
                    "ref": self.ref,
                    "working_directory": self.working_directory,
                    "checks": list(map(lambda check: check.__to_dict__(), self.checks)),
                }
            )

    class Check:
        def __init__(self, data):
            if isinstance(data, dict):
                if len(data) != 1:
                    raise ValueError(f"Invalid check format: {data}")
                self.name, self.args = next(iter(data.items()))
            else:
                self.name = data
                self.args = None

        def __to_dict__(self):
            if self.args:
                return {self.name: self.args}
            else:
                return self.name


InputManifest.VERSIONS = {
    "1.0": InputManifest
}
