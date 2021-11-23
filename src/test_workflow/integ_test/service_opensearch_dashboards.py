# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess
import tarfile

import requests
import yaml

from paths.tree_walker import walk
from system.process import Process
from test_workflow.integ_test.service import Service
from test_workflow.test_recorder.test_result_data import TestResultData


class ServiceOpenSearchDashboards(Service):
    def __init__(
        self,
        manifest,
        component_name,
        component_test_config,
        additional_cluster_config,
        security_enabled,
        dependency_installer,
        save_logs,
        work_dir
    ):
        self.manifest = manifest
        self.component_name = component_name
        self.component_test_config = component_test_config

        self.additional_cluster_config = additional_cluster_config
        self.security_enabled = security_enabled
        self.dependency_installer = dependency_installer
        self.save_logs = save_logs
        self.work_dir = work_dir

        self.install_dir = os.path.join(
            self.work_dir, f"opensearch-dashboards-{self.manifest.build.version}-{self.manifest.build.platform}-{self.manifest.build.architecture}")
        self.process_handler = Process()

    def start(self):
        logging.info(f"Starting OpenSearch Dashboards service from {self.work_dir}")
        self.__download()

        self.opensearch_dashboards_yml_dir = os.path.join(self.install_dir, "config", "opensearch_dashboards.yml")
        self.executable_dir = os.path.join(self.install_dir, "bin")

        if not self.security_enabled:
            self.__remove_security()

        if self.additional_cluster_config:
            self.__add_plugin_specific_config(self.additional_cluster_config)

        self.process_handler.start("./opensearch-dashboards", self.executable_dir)
        logging.info(f"Started OpenSearch Dashboards with parent PID {self.process_handler.pid}")

    def __remove_security(self):
        subprocess.check_call("./opensearch-dashboards-plugin remove securityDashboards", cwd=self.executable_dir, shell=True)

        with open(self.opensearch_dashboards_yml_dir, "w") as yamlfile:
            yamlfile.close()

    def __download(self):
        logging.info("Downloading OpenSearch Dashboards bundle")
        bundle_name = self.dependency_installer.download_dist(self.work_dir)
        logging.info(f"Downloaded bundle to {os.path.realpath(bundle_name)}")

        logging.info(f"Unpacking {bundle_name}")
        with tarfile.open(bundle_name, 'r') as bundle_tar:
            bundle_tar.extractall(self.work_dir)

        logging.info(f"Unpacked {bundle_name}")

    def url(self, path=""):
        return f'http://{self.endpoint()}:{self.port()}{path}'

    def get_service_response(self):
        url = self.url("/api/status")
        logging.info(f"Pinging {url}")
        return requests.get(url, verify=False, auth=("kibanaserver", "kibanaserver") if self.security_enabled else None)

    def terminate(self):
        if not self.process_handler.started:
            logging.info("OpenSearch Dashboards service is not started")
            return

        self.return_code = self.process_handler.terminate()

        self.__test_result_data()

    def __test_result_data(self):
        log_files = walk(os.path.join(self.install_dir, "logs"))
        test_result_data = TestResultData(
            self.component_name, self.component_test_config, self.return_code, self.process_handler.stdout_data, self.process_handler.stderr_data, log_files
        )
        self.save_logs.save_test_result_data(test_result_data)

    def __add_plugin_specific_config(self, additional_config):
        with open(self.opensearch_dashboards_yml_dir, "a") as yamlfile:
            yamlfile.write(yaml.dump(additional_config))

    def endpoint(self):
        return "localhost"

    def port(self):
        return 5601
