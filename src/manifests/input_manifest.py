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
  patches: optional list of compatible versions this build is patching
  platform: optional default platform
  architecture: optional default architecture
  snapshot: optional default snapshot
ci:
  image:
    name: docker image name to pull
    args: args to execute builds with, e.g. -e JAVA_HOME=...
components:
  - name: string
    repository: URL of git repository
    ref: git ref to build (sha, branch, or tag)
    working_directory: optional relative directory to run commands in
    checks: CI checks
      - check1
      - ...
    platforms: optional list of supported platforms
      - windows
      - darwin
      - linux
  - ...
"""
import copy
import itertools
import logging

from git.git_repository import GitRepository
from manifests.component_manifest import ComponentManifest


class InputManifest(ComponentManifest):
    SCHEMA = {
        "schema-version": {"required": True, "type": "string", "allowed": ["1.0"]},
        "build": {
            "required": True,
            "type": "dict",
            "schema": {
                "name": {"required": True, "type": "string"},
                "version": {"required": True, "type": "string"},
                "patches": {"type": "list", "schema": {"type": "string"}},
                "platform": {"type": "string"},
                "architecture": {"type": "string"},
                "snapshot": {"type": "boolean"},
            },
        },
        "ci": {
            "required": False,
            "type": "dict",
            "schema": {
                "image": {
                    "required": False,
                    "type": "dict",
                    "schema": {"name": {"required": True, "type": "string"}, "args": {"required": False, "type": "string"}},
                }
            },
        },
        "components": {
            "type": "list",
            "schema": {
                "anyof": [
                    {
                        "type": "dict",
                        "schema": {
                            "name": {"required": True, "type": "string"},
                            "ref": {"required": True, "type": "string"},
                            "repository": {"required": True, "type": "string"},
                            "working_directory": {"type": "string"},
                            "checks": {"type": "list", "schema": {"anyof": [{"type": "string"}, {"type": "dict"}]}},
                            "platforms": {"type": "list", "schema": {"type": "string", "allowed": ["linux", "windows", "darwin"]}},
                        },
                    },
                    {
                        "type": "dict",
                        "schema": {
                            "name": {"required": True, "type": "string"},
                            "dist": {"required": True, "type": "string"},
                            "checks": {"type": "list", "schema": {"anyof": [{"type": "string"}, {"type": "dict"}]}},
                            "platforms": {"type": "list", "schema": {"type": "string", "allowed": ["linux", "windows", "darwin"]}},
                        },
                    },
                ]
            },
        },
    }

    def __init__(self, data):
        super().__init__(data)

        self.build = self.Build(data["build"])
        self.ci = self.Ci(data.get("ci", None))
        self.components = self.Components(data.get("components", []))

    def __to_dict__(self):
        return {
            "schema-version": "1.0",
            "build": self.build.__to_dict__(),
            "ci": None if self.ci is None else self.ci.__to_dict__(),
            "components": self.components.__to_dict__(),
        }

    def stable(self, architecture=None, platform=None, snapshot=False):
        manifest = copy.deepcopy(self)
        manifest.build.__stabilize__(
            platform=platform,
            architecture=architecture,
            snapshot=snapshot
        )
        manifest.components.__stabilize__()
        return manifest

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
                return {
                    "name": self.name,
                    "args": self.args
                }

    class Build:
        def __init__(self, data):
            self.name = data["name"]
            self.version = data["version"]
            self.platform = data.get("platform", None)
            self.architecture = data.get("architecture", None)
            self.snapshot = data.get("snapshot", None)
            self.patches = data.get("patches", [])

        def __stabilize__(self, platform, architecture, snapshot):
            self.architecture = architecture
            self.platform = platform
            self.snapshot = snapshot

        def __to_dict__(self):
            return {
                "name": self.name,
                "version": self.version,
                "patches": self.patches,
                "platform": self.platform,
                "architecture": self.architecture,
                "snapshot": self.snapshot,
            }

    class Components(ComponentManifest.Components):
        @classmethod
        def __create__(self, data):
            return InputManifest.Component._from(data)

        def __stabilize__(self):
            for component in self.values():
                component.__stabilize__()

        def select(self, focus=None, platform=None):
            """
            Select components.

            :param str focus: Choose one component.
            :param str platform: Only components targeting a given platform.
            :return: Collection of components.
            :raises ValueError: Invalid platform or component name specified.
            """
            selected, it = itertools.tee(filter(lambda component: component.__matches__(focus, platform), self.values()))

            if not any(it):
                raise ValueError(f"No components matched focus={focus}, platform={platform}.")

            return selected

    class Component(ComponentManifest.Component):
        def __init__(self, data):
            super().__init__(data)
            self.platforms = data.get("platforms", None)

        @classmethod
        def _from(self, data):
            if "repository" in data:
                return InputManifest.ComponentFromSource(data)
            elif "dist" in data:
                return InputManifest.ComponentFromDist(data)
            else:
                raise ValueError(f"Invalid component data: {data}")

        def __matches__(self, focus=None, platform=None):
            matches = ((not focus) or (self.name == focus)) and ((not platform) or (not self.platforms) or (platform in self.platforms))

            if not matches:
                logging.info(f"Skipping {self.name}")

            return matches

        def __stabilize__(self):
            pass

    class ComponentFromSource(Component):
        def __init__(self, data):
            super().__init__(data)
            self.repository = data["repository"]
            self.ref = data["ref"]
            self.working_directory = data.get("working_directory", None)
            self.checks = list(map(lambda entry: InputManifest.Check(entry), data.get("checks", [])))

        def __stabilize__(self):
            ref, name = GitRepository.stable_ref(self.repository, self.ref)
            logging.info(f"Updating ref for {self.repository} from {self.ref} to {ref} ({name})")
            self.ref = ref

        def __to_dict__(self):
            return {
                "name": self.name,
                "repository": self.repository,
                "ref": self.ref,
                "working_directory": self.working_directory,
                "checks": list(map(lambda check: check.__to_dict__(), self.checks)),
                "platforms": self.platforms,
            }

    class ComponentFromDist(Component):
        def __init__(self, data):
            super().__init__(data)
            self.dist = data["dist"]
            self.checks = list(map(lambda entry: InputManifest.Check(entry), data.get("checks", [])))

        def __to_dict__(self):
            return {
                "name": self.name,
                "dist": self.dist,
                "platforms": self.platforms,
                "checks": list(map(lambda check: check.__to_dict__(), self.checks))
            }

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


InputManifest.VERSIONS = {"1.0": InputManifest}
