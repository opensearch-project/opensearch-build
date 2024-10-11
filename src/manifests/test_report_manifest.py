# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Optional

from manifests.component_manifest import Component, ComponentManifest, Components
from manifests.test_report.test_report_manifest_1_0 import TestReportManifest_1_0


class TestReportManifest(ComponentManifest['TestReportManifest', 'TestComponents']):
    """
    TestReportManifest contains the aggregated test results for the components.

    The format for schema version 1.1 is:
        schema-version: '1.1'
        name: name of the product e.g. OpenSearch
        version: string
        platform: linux, darwin or windows
        architecture: x64 or arm64
        distribution: tar, zip, deb and rpm
        id: build id
        rc: release candidate information
        test-run:
          Command: command to trigger the integ test
          TestType: type of test this manifest reports. e.g. integ-test
          TestManifest: location of the test manifest used
          DistributionManifest: URL or local path of the bundle manifest.
          TestID: test id
        components:
          - name: sql
            command: command to trigger the integ test for only sql component
            repository: the repository url of the component
            configs:
              - name: with-security
                status: the status of the test run with this config. e.g. pass/fail
                yml: URL or local path to the component yml file
                test_stdout: URL or local path to the test stdout log
                test_stderr: URL or local path to the test stderr log
                cluster_stdout:
                  - URL or local path to the OpenSearch cluster logs
                cluster_stderr:
                  - URL or local path to the OpenSearch cluster error logs
                failed test:
                  - ClassName#TestName for failed test case
    """

    VERSIONS = {
        "1.0": TestReportManifest_1_0,
        # "1.1": current
    }

    SCHEMA = {
        "schema-version": {"required": True, "type": "string", "allowed": ["1.1"]},
        "name": {"required": True, "type": "string", "allowed": ["OpenSearch", "OpenSearch Dashboards"]},
        "version": {"required": True, "type": "string"},  # added in 1.1
        "platform": {"required": True, "type": "string"},  # added in 1.1
        "architecture": {"required": True, "type": "string"},  # added in 1.1
        "distribution": {"required": True, "type": "string"},  # added in 1.1
        "id": {"required": True, "type": "string"},  # added in 1.1
        "rc": {"required": True, "type": "string"},  # added in 1.1
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
                    "repository": {"type": "string"},
                    "configs": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "name": {"type": "string"},
                                "status": {"type": "string"},
                                "yml": {"type": "string"},
                                "test_stdout": {"type": "string"},
                                "test_stderr": {"type": "string"},
                                "cluster_stdout": {"type": "list"},
                                "cluster_stderr": {"type": "list"},
                                "failed_test": {"type": "list"}
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
        self.version = str(data["version"])
        self.platform = str(data["platform"])
        self.architecture = str(data["architecture"])
        self.distribution = str(data["distribution"])
        self.build_id = str(data["id"])
        self.release_candidate = str(data["rc"])
        self.test_run = self.TestRun(data.get("test-run", None))
        self.components = TestComponents(data.get("components", []))  # type: ignore[assignment]

    def __to_dict__(self) -> dict:
        return {
            "schema-version": "1.1",
            "name": self.name,
            "version": self.version,
            "platform": self.platform,
            "architecture": self.architecture,
            "distribution": self.distribution,
            "id": self.build_id,
            "rc": self.release_candidate,
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


class TestComponents(Components['TestComponent']):
    @classmethod
    def __create__(self, data: dict) -> 'TestComponent':
        return TestComponent(data)


class TestComponent(Component):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.command = data["command"]
        self.repository = data["repository"]
        self.configs = self.TestComponentConfigs(data.get("configs", None))

    def __to_dict__(self) -> dict:
        return {
            "name": self.name,
            "command": self.command,
            "repository": self.repository,
            "configs": self.configs.__to_list__()
        }

    class TestComponentConfigs:
        def __init__(self, data: list) -> None:
            self.configs = []
            for config in data:
                self.configs.append(self.TestComponentConfig(config).__to_dict__())

        def __to_list__(self) -> list:
            return self.configs

        class TestComponentConfig:
            def __init__(self, data: dict) -> None:
                self.name = data["name"]
                self.status = data["status"]
                self.yml = data["yml"]
                self.test_stdout = data["test_stdout"]
                self.test_stderr = data["test_stderr"]
                self.cluster_stdout = data["cluster_stdout"]
                self.cluster_stderr = data["cluster_stderr"]
                self.failed_test = data["failed_test"]

            def __to_dict__(self) -> dict:
                return {
                    "name": self.name,
                    "status": self.status,
                    "yml": self.yml,
                    "test_stdout": self.test_stdout,
                    "test_stderr": self.test_stderr,
                    "cluster_stdout": self.cluster_stdout,
                    "cluster_stderr": self.cluster_stderr,
                    "failed_test": self.failed_test
                }


TestReportManifest.VERSIONS = {"1.0": TestReportManifest_1_0, "1.1": TestReportManifest}

TestComponent.__test__ = False  # type: ignore[attr-defined]
TestReportManifest.__test__ = False  # type: ignore[attr-defined]
