# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import yaml


class TestManifest:
    """
    TestManifest contains the test support matrix for any component.

    The format for schema version 1.0 is:
        schema-version: '1.0'
        components:
          - name: index-management
            integ-test:
              dependencies:
                - job-scheduler
                - alerting
              test-configs:
                - with-security
                - without-security
                - with-less-security
            bwc-test:
              dependencies:
              test-configs:
                - with-security
                - without-security
    """

    @staticmethod
    def from_file(file):
        return TestManifest(yaml.safe_load(file))

    def __init__(self, data):
        self.version = str(data["schema-version"])
        if self.version != "1.0":
            raise ValueError(f"Unsupported schema version: {self.version}")
        self.components = list(
            map(lambda entry: self.Component(entry), data["components"])
        )

    def to_dict(self):
        return {
            "schema-version": "1.0",
            "components": list(
                map(lambda component: component.to_dict(), self.components)
            ),
        }

    class Component:
        def __init__(self, data):
            self.name = data["name"]
            self.integ_test = data["integ-test"]
            self.bwc_test = data["bwc-test"]

        def to_dict(self):
            return {
                "name": self.name,
                "integ-test": self.integ_test,
                "bwc-test": self.bwc_test,
            }
