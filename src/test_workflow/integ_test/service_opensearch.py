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

from test_workflow.integ_test.service import Service


class ServiceOpenSearch(Service):
    def __init__(
        self,
        version,
        additional_config,
        security_enabled,
        dependency_installer,
        work_dir
    ):
        super().__init__(work_dir, version, security_enabled, additional_config, dependency_installer)

        self.dependency_installer = dependency_installer

        self.install_dir = os.path.join(self.work_dir, f"opensearch-{self.version}")

    def start(self):
        self.__download()

        self.opensearch_yml_dir = os.path.join(self.install_dir, "config", "opensearch.yml")

        if not self.security_enabled:
            self.__add_plugin_specific_config({"plugins.security.disabled": "true"})

        if self.additional_config:
            self.__add_plugin_specific_config(self.additional_config)

        self.process_handler.start("./opensearch-tar-install.sh", self.install_dir)
        logging.info(f"Started OpenSearch with parent PID {self.process_handler.pid}")

    def __download(self):
        logging.info(f"Creating local test cluster in {self.work_dir}")
        logging.info("Downloading bundle")
        bundle_name = self.dependency_installer.download_dist(self.work_dir)
        logging.info(f"Downloaded bundle to {os.path.realpath(bundle_name)}")

        logging.info(f"Unpacking {bundle_name}")
        with tarfile.open(bundle_name, 'r') as bundle_tar:
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

    def port(self):
        return 9200

    def check_service_response_text(self, response_text):
        return ('"status":"green"' in response_text) or ('"status":"yellow"' in response_text)

    @property
    def log_files(self):
        return {"opensearch-service-logs": os.path.join(self.install_dir, "logs")}
