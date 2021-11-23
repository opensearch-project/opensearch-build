# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import tarfile

import requests
import yaml

from system.process import Process
from test_workflow.integ_test.service import Service


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
        self.dependency_installer = dependency_installer
        self.save_logs = save_logs
        self.work_dir = work_dir

        self.install_dir = os.path.join(self.work_dir, f"opensearch-{self.manifest.build.version}")
        self.process_handler = Process()

    def start(self):
        self.__download()

        self.opensearch_yml_dir = os.path.join(self.install_dir, "config", "opensearch.yml")

        if not self.security_enabled:
            self.__add_plugin_specific_config({"plugins.security.disabled": "true"})

        if self.additional_cluster_config:
            self.__add_plugin_specific_config(self.additional_cluster_config)

        self.process_handler.start("./opensearch-tar-install.sh", self.install_dir)
        logging.info(f"Started OpenSearch with parent PID {self.process_handler.pid}")

    def __download(self):
        logging.info(f"Creating local test cluster in {self.work_dir}")
        logging.info("Downloading bundle")
        bundle_name = self.dependency_installer.download_dist(self.work_dir)
        logging.info(f"Downloaded bundle to {os.path.realpath(bundle_name)}")

        logging.info(f"Unpacking {bundle_name}")
        bundle_tar = tarfile.open(bundle_name, 'r')
        bundle_tar.extractall(self.work_dir)

        logging.info(f"Unpacked {bundle_name}")

    def url(self, path=""):
        return f'{"https" if self.security_enabled else "http"}://{self.endpoint()}:{self.port()}{path}'

    def get_service_response(self):
        url = self.url("/_cluster/health")
        logging.info(f"Pinging {url}")
        return requests.get(url, verify=False, auth=("admin", "admin"))

    def __add_plugin_specific_config(self, additional_config):
        with open(self.opensearch_yml_dir, "a") as yamlfile:
            yamlfile.write(yaml.dump(additional_config))

    def endpoint(self):
        return "localhost"

    def port(self):
        return 9200
