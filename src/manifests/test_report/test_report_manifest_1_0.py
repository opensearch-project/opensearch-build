# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Optional

from manifests.component_manifest import Component, ComponentManifest, Components


class TestReportManifest_1_0(ComponentManifest['TestReportManifest_1_0', 'TestComponents_1_0']):
    """
    TestReportManifest contains the aggregated test results for the components.

    The format for schema version 1.0 is:
        schema-version: '1.0'
        name: name of the product e.g. OpenSearch
        test-run:
          Command: command to trigger the integ test
          TestType: type of test this manifest reports. e.g. integ-test
          TestManifest: location of the test manifest used
          DistributionManifest: URL or local path of the bundle manifest.
          TestID: test id
        components:
          - name: sql
            command: command to trigger the integ test for only sql component
            configs:
              - name: with-security
                status: the status of the test run with this config. e.g. pass/fail
                yml: URL or local path to the component yml file
                cluster_stdout:
                  - URL or local path to the OpenSearch cluster logs
                cluster_stderr:
                  - URL or local path to the OpenSearch cluster error logs
    """

    SCHEMA = {
        "schema-version": {"required": True, "type": "string", "allowed": ["1.0"]},
        "name": {"required": True, "type": "string", "allowed": ["OpenSearch", "OpenSearch Dashboards"]},
        "test-run": {
            "required": False,
            "type": "dict",
            "schema": {
                "Command": {"required": False, "type": "string"},
                "TestType": {"required": False, "type": "string"},
                "TestManifest": {"required": False, "type": "string"},
                "DistributionManifest": {"required": False, "type": "string"},
                "TestID": {"required": False, "type": "string"}
            },
        },
        "components": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "name": {"required": True, "type": "string"},
                    "command": {"type": "string"},
                    "configs": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "name": {"type": "string"},
                                "status": {"type": "string"},
                                "yml": {"type": "string"},
                                "cluster_stdout": {"type": "list"},
                                "cluster_stderr": {"type": "list"}
                            }
                        },
                    },
                },
            },
        },
    }

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.name = str(data["name"])
        self.test_run = self.TestRun(data.get("test-run", None))
        self.components = TestComponents_1_0(data.get("components", []))  # type: ignore[assignment]

    def __to_dict__(self) -> dict:
        return {
            "schema-version": "1.0",
            "name": self.name,
            "test-run": None if self.test_run is None else self.test_run.__to_dict__(),
            "components": self.components.__to_dict__()
        }

    class TestRun:
        def __init__(self, data: dict) -> None:
            if data is None:
                self.test_run = None
            else:
                self.command = data["Command"]
                self.test_type = data["TestType"]
                self.test_manifest = data["TestManifest"]
                self.distribution_manifest = data["DistributionManifest"]
                self.test_id = data["TestID"]

        def __to_dict__(self) -> Optional[dict]:
            if (self.command and self.test_type and self.test_manifest and self.distribution_manifest and self.test_id) is None:
                return None
            else:
                return {
                    "Command": self.command,
                    "TestType": self.test_type,
                    "TestManifest": self.test_manifest,
                    "DistributionManifest": self.distribution_manifest,
                    "TestID": self.test_id
                }


class TestComponents_1_0(Components['TestComponent_1_0']):
    @classmethod
    def __create__(self, data: dict) -> 'TestComponent_1_0':
        return TestComponent_1_0(data)


class TestComponent_1_0(Component):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.command = data["command"]
        self.configs = self.TestComponentConfigs_1_0(data.get("configs", None))

    def __to_dict__(self) -> dict:
        return {
            "name": self.name,
            "command": self.command,
            "configs": self.configs.__to_list__()
        }

    class TestComponentConfigs_1_0:
        def __init__(self, data: list) -> None:
            self.configs = []
            for config in data:
                self.configs.append(self.TestComponentConfig_1_0(config).__to_dict__())

        def __to_list__(self) -> list:
            return self.configs

        class TestComponentConfig_1_0:
            def __init__(self, data: dict) -> None:
                self.name = data["name"]
                self.status = data["status"]
                self.yml = data["yml"]
                self.cluster_stdout = data["cluster_stdout"]
                self.cluster_stderr = data["cluster_stderr"]

            def __to_dict__(self) -> dict:
                return {
                    "name": self.name,
                    "status": self.status,
                    "yml": self.yml,
                    "cluster_stdout": self.cluster_stdout,
                    "cluster_stderr": self.cluster_stderr
                }


TestReportManifest_1_0.VERSIONS = {"1.0": TestReportManifest_1_0}

TestComponent_1_0.__test__ = False  # type: ignore[attr-defined]
TestReportManifest_1_0.__test__ = False  # type: ignore[attr-defined]
