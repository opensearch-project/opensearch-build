# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from manifests.manifest import Manifest


class TestManifest(Manifest):
    """
    TestManifest contains the test support matrix for any component.

    The format for schema version 1.0 is:
        schema-version: '1.0'
        components:
          - name: index-management
            working-directory: optional relative directory to run commands in
            integ-test:
              test-configs:
                - with-security
                - without-security
                - with-less-security
              additional-cluster-configs:
                - key : value
            bwc-test:
              test-configs:
                - with-security
                - without-security
    """

    SCHEMA = {
        "schema-version": {"required": True, "type": "string", "allowed": ["1.0"]},
        "components": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "name": {"required": True, "type": "string"},
                    "working-directory": {"type": "string"},
                    "integ-test": {
                        "type": "dict",
                        "schema": {
                            "build-dependencies": {"type": "list"},
                            "test-configs": {
                                "type": "list",
                                "allowed": [
                                    "with-security",
                                    "without-security",
                                ],
                            },
                            "additional-cluster-configs": {
                                "type": "dict",
                            },
                        },
                    },
                    "bwc-test": {
                        "type": "dict",
                        "schema": {
                            "build-dependencies": {"type": "list"},
                            "test-configs": {
                                "type": "list",
                                "allowed": [
                                    "with-security",
                                    "without-security",
                                    "with-less-security",
                                ],
                            },
                        },
                    },
                },
            },
        },
    }

    def __init__(self, data):
        super().__init__(data)
        self.components = list(map(lambda entry: self.Component(entry), data["components"]))

    def __to_dict__(self):
        return {
            "schema-version": "1.0",
            "components": list(map(lambda component: component.__to_dict__(), self.components)),
        }

    class Component:
        def __init__(self, data):
            self.name = data["name"]
            self.working_directory = data.get("working-directory", None)
            self.integ_test = data["integ-test"]
            self.bwc_test = data["bwc-test"]

        def __to_dict__(self):
            return Manifest.compact(
                {
                    "name": self.name,
                    "working-directory": self.working_directory,
                    "integ-test": self.integ_test,
                    "bwc-test": self.bwc_test,
                }
            )


TestManifest.VERSIONS = {
    "1.0": TestManifest
}

TestManifest.__test__ = False  # type:ignore
