# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

from typing import Optional

from manifests.component_manifest import Component, ComponentManifest, Components


class TestManifest(ComponentManifest['TestManifest', 'TestComponents']):
    """
    TestManifest contains the test support matrix for any component.

    The format for schema version 1.0 is:
        schema-version: '1.0'
        name: 'OpenSearch'
        ci:
            image:
                name: docker image name to pull
                args: args to execute builds with, e.g. -e JAVA_HOME=...
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
              ci-group: 6
            bwc-test:
              test-configs:
                - with-security
                - without-security
            smoke-test:
              test-spec: spec.yml
    """

    SCHEMA = {
        "schema-version": {"required": True, "type": "string", "allowed": ["1.0"]},
        "name": {"required": True, "type": "string", "allowed": ["OpenSearch", "OpenSearch Dashboards"]},
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
                "type": "dict",
                "schema": {
                    "name": {"required": True, "type": "string"},
                    "working-directory": {"type": "string"},
                    "integ-test": {
                        "type": "dict",
                        "schema": {
                            "build-dependencies": {"type": "list"},
                            "topology": {
                                "type": "list", "required": False,
                                "schema": {
                                    "type": "dict",
                                    "schema": {
                                        "cluster_name": {"required": True, "type": "string"},
                                        "data_nodes": {"type": "integer", "required": True},
                                        "cluster_manager_nodes": {"type": "integer"}
                                    }

                                }

                            },
                            "test-configs": {"type": "list", "allowed": ["with-security", "without-security"]},
                            "additional-cluster-configs": {"type": "dict"},
                            "ci-groups": {"type": "integer"}
                        },
                    },
                    "bwc-test": {
                        "type": "dict",
                        "schema": {
                            "build-dependencies": {"type": "list"},
                            "test-configs": {"type": "list", "allowed": ["with-security", "without-security", "with-less-security"]},
                        },
                    },
                    "smoke-test": {
                        "type": "dict",
                        "schema": {
                            "test-spec": {"type": "string"},
                        },
                    },
                },
            },
        },
    }

    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.name = str(data["name"])
        self.ci = self.Ci(data.get("ci", None))
        self.components = TestComponents(data.get("components", []))  # type: ignore[assignment]

    def __to_dict__(self) -> dict:
        return {
            "schema-version": "1.0",
            "name": self.name,
            "ci": None if self.ci is None else self.ci.__to_dict__(),
            "components": self.components.__to_dict__()
        }

    class Ci:
        def __init__(self, data: dict) -> None:
            self.image = None if data is None else self.Image(data.get("image", None))

        def __to_dict__(self) -> Optional[dict]:
            return None if self.image is None else {"image": self.image.__to_dict__()}

        class Image:
            def __init__(self, data: dict) -> None:
                self.name = data["name"]
                self.args = data.get("args", None)

            def __to_dict__(self) -> dict:
                return {
                    "name": self.name,
                    "args": self.args
                }


class TestComponents(Components['TestComponent']):
    @classmethod
    def __create__(self, data: dict) -> 'TestComponent':
        return TestComponent(data)


class ClusterConfig:
    def __init__(self, cluster_config_data: dict):
        self.cluster_name = cluster_config_data['cluster_name']
        self.data_nodes = cluster_config_data['data_nodes']
        self.cluster_manager_nodes = cluster_config_data['cluster_manager_nodes'] if "cluster_manager_nodes" in cluster_config_data.keys() else 0
        assert self.cluster_manager_nodes == 0, "Cluster manager nodes are not supported so use value 0 or skip this parameter"


class TestComponentTopology:
    def __init__(self, data: dict):
        if data is not None:
            self.cluster_configs = []
            total_nodes = 0
            for cluster_config_data in data:
                cluster_config = ClusterConfig(cluster_config_data)
                total_nodes += cluster_config.data_nodes + cluster_config.cluster_manager_nodes
                self.cluster_configs.append(cluster_config)
            assert total_nodes <= 100, "More than 100 nodes(data_nodes and cluster_manager_nodes) over all clusters are not supported"
        else:
            self.cluster_configs = [ClusterConfig({'cluster_name': 'cluster1', 'data_nodes': 1, 'cluster_manager_nodes': 0})]  # type: ignore[assignment]


class TestComponent(Component):
    def __init__(self, data: dict) -> None:
        super().__init__(data)
        self.working_directory = data.get("working-directory", None)
        self.integ_test = data.get("integ-test", None)
        self.bwc_test = data.get("bwc-test", None)
        self.smoke_test = data.get("smoke-test", None)
        self.topology = TestComponentTopology(self.integ_test.get("topology", None)) if self.integ_test is not None else TestComponentTopology(None)
        self.components = TestComponents(data.get("components", []))  # type: ignore[assignment]

    def __to_dict__(self) -> dict:
        return {
            "name": self.name,
            "working-directory": self.working_directory,
            "integ-test": self.integ_test,
            "bwc-test": self.bwc_test,
            "smoke-test": self.smoke_test
        }


TestManifest.VERSIONS = {"1.0": TestManifest}

TestComponent.__test__ = False  # type: ignore[attr-defined]
TestManifest.__test__ = False  # type: ignore[attr-defined]
