# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess
import time

import requests
import yaml

from paths.tree_walker import walk
from system.process import Process
from test_workflow.integ_test.service import Service
from test_workflow.test_cluster import ClusterCreationException
from test_workflow.test_recorder.test_result_data import TestResultData


class ServiceOpenSearch(Service):
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
        self.process_handler = Process()
        self.dependency_installer = dependency_installer
        self.save_logs = save_logs
        self.work_dir = work_dir

    def start(self):
        self.download()
        self.install_dir = f"opensearch-{self.manifest.build.version}"
        if not self.security_enabled:
            self.disable_security(self.install_dir)

        if self.additional_cluster_config:
            self.__add_plugin_specific_config(
                self.additional_cluster_config,
                os.path.join(self.install_dir, "config", "opensearch.yml")
            )

        self.process_handler.start("./opensearch-tar-install.sh", self.install_dir)
        logging.info(f"Started OpenSearch with parent PID {self.process_handler.pid}")

    def download(self):
        logging.info(f"Creating local test cluster in {self.work_dir}")
        os.chdir(self.work_dir)
        logging.info("Downloading bundle")
        bundle_name = self.dependency_installer.download_dist(self.work_dir)
        logging.info(f"Downloaded bundle to {os.path.realpath(bundle_name)}")
        logging.info(f"Unpacking {bundle_name}")
        subprocess.check_call(f"tar -xzf {bundle_name}", cwd=self.work_dir, shell=True)
        logging.info(f"Unpacked {bundle_name}")

    def url(self, path=""):
        return f'{"https" if self.security_enabled else "http"}://{self.endpoint()}:{self.port()}{path}'

    def get_service_response(self):
        url = self.url("/_cluster/health")
        logging.info(f"Pinging {url}")
        return requests.get(url, verify=False, auth=("admin", "admin"))

    def terminate(self):
        if not self.process_handler.started:
            logging.info("Local test cluster is not started")
            return

        self.return_code = self.process_handler.terminate()

        self.__test_result_data()

    def __test_result_data(self):
        log_files = walk(os.path.join(self.work_dir, self.install_dir, "logs"))
        test_result_data = TestResultData(
            self.component_name, self.component_test_config, self.return_code, self.process_handler.stdout_data, self.process_handler.stderr_data, log_files
        )
        self.save_logs.save_test_result_data(test_result_data)

    def __add_plugin_specific_config(self, additional_config: dict, file):
        with open(file, "a") as yamlfile:
            yamlfile.write(yaml.dump(additional_config))

    def disable_security(self, dir):
        with open(os.path.join(dir, "config", "opensearch.yml"), "a") as yamlfile:
            yamlfile.write(yaml.dump({"plugins.security.disabled", "true"}))

    def endpoint(self):
        return "localhost"

    def port(self):
        return 9200
