# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, List

from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import ClusterConfig
from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.integ_test.local_test_cluster import LocalTestCluster
from test_workflow.test_recorder.test_recorder import TestRecorder


class Topology:

    def __init__(
        self,
        topology_config: list,
        dependency_installer: DependencyInstaller,
        work_dir: Path,
        component_name: str,
        additional_cluster_config: dict,
        bundle_manifest: BundleManifest,
        security_enabled: bool,
        component_test_config: str,
        test_recorder: TestRecorder
    ) -> None:
        self.topology_config = topology_config
        self.dependency_installer = dependency_installer
        self.work_dir = work_dir
        self.component_name = component_name
        self.additional_cluster_config = additional_cluster_config
        self.bundle_manifest = bundle_manifest
        self.security_enabled = security_enabled
        self.component_test_config = component_test_config
        self.test_recorder = test_recorder
        self.clusters: list = []

    @classmethod
    @contextmanager
    def create(cls, *args: Any) -> Generator[List, None, None]:
        topology = cls(*args)
        try:
            yield topology.create_clusters()
        finally:
            topology.destroy()

    def create_clusters(self) -> List:
        topology_endpoints_list = []

        current_port = 9200
        current_transport_port = 9300
        current_work_dir_num = 1
        for cluster_config in self.topology_config:
            cluster = TopologyTestCluster(
                cluster_config.cluster_name,
                cluster_config,
                current_port,
                current_transport_port,
                current_work_dir_num,
                self.additional_cluster_config,
                self.component_name,
                self.bundle_manifest,
                self.security_enabled,
                self.component_test_config,
                self.test_recorder,
                self.dependency_installer,
                self.work_dir
            )
            self.clusters.append(cluster)
            data_node_endpoints = []
            cluster_manager_nodes_endpoints = []
            for data_node in cluster.data_nodes:
                data_node_endpoints.append(NodeEndpoint(data_node))
            for cluster_manager_node in cluster.cluster_manager_nodes:
                cluster_manager_nodes_endpoints.append(NodeEndpoint(cluster_manager_node))

            topology_endpoints_list.append(ClusterEndpoint(cluster_config.cluster_name, data_node_endpoints, cluster_manager_nodes_endpoints))
            total_nodes_in_cluster = cluster_config.data_nodes + cluster_config.cluster_manager_nodes
            current_port += total_nodes_in_cluster
            current_work_dir_num += total_nodes_in_cluster
            current_transport_port += total_nodes_in_cluster
        return topology_endpoints_list

    def destroy(self) -> None:
        for topology_cluster in self.clusters:
            for datanode in topology_cluster.data_nodes:
                datanode.cluster.terminate()
            for managernode in topology_cluster.cluster_manager_nodes:
                managernode.cluster.terminate()
        self.clusters = []


class DataNode:
    def __init__(
        self,
        dependency_installer: DependencyInstaller,
        work_dir: str,
        component_name: str,
        additional_cluster_config: dict,
        bundle_manifest: BundleManifest,
        security_enabled: bool,
        component_test_config: str,
        test_recorder: TestRecorder,
        current_transport_port: int,
        cluster_port: int = 9200
    ):
        self.cluster = LocalTestCluster.create_cluster(
            dependency_installer,
            work_dir,
            component_name,
            additional_cluster_config,
            bundle_manifest,
            security_enabled,
            component_test_config,
            test_recorder,
            cluster_port)
        self.port = cluster_port
        self.transport = current_transport_port


class NodeEndpoint:
    def __init__(self, *args: Any):
        if len(args) == 1:
            self.endpoint = args[0].cluster.endpoint
            self.port = args[0].port
            self.transport = args[0].transport
        else:
            self.endpoint = args[0]
            self.port = args[1]
            self.transport = args[2]


class TopologyTestCluster:
    def __init__(
        self,
        cluster_name: str,
        cluster_config: ClusterConfig,
        current_port: int,
        current_transport_port: int,
        current_work_dir_num: int,
        additional_cluster_config: dict,
        component_name: str,
        bundle_manifest: BundleManifest,
        security_enabled: bool,
        component_test_config: str,
        test_recorder: TestRecorder,
        dependency_installer: DependencyInstaller,
        work_dir: Path
    ):
        self.cluster_name = cluster_name
        self.data_nodes: list = []
        self.cluster_manager_nodes: list = []
        additional_cluster_config['cluster.name'] = "opensearch" + cluster_config.cluster_name

        for i in range(cluster_config.data_nodes):
            additional_cluster_config['http.port'] = current_port
            additional_cluster_config['node.name'] = "node_name_" + f'{current_port}'
            additional_cluster_config['path.shared_data'] = '/tmp'
            self.data_nodes.append(DataNode(
                dependency_installer,
                os.path.join(work_dir, f'{current_work_dir_num}'),
                component_name,
                additional_cluster_config,
                bundle_manifest,
                security_enabled,
                component_test_config,
                test_recorder,
                current_transport_port,
                current_port
            ))
            current_port = current_port + 1
            current_work_dir_num = current_work_dir_num + 1
            current_transport_port = current_transport_port + 1


class ClusterEndpoint:
    def __init__(self, cluster_name: str, data_nodes: list, cluster_manager_nodes: list):
        self.cluster_name = cluster_name
        self.data_nodes = data_nodes
        self.cluster_manager_nodes = cluster_manager_nodes
