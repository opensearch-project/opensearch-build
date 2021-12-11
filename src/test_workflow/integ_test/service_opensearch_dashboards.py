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

from test_workflow.integ_test.service import Service


class ServiceOpenSearchDashboards(Service):
    def __init__(
        self,
        version,
        additional_config,
        security_enabled,
        dependency_installer,
        work_dir
    ):
        super().__init__(work_dir, version, security_enabled, additional_config, dependency_installer)
        self.install_dir = os.path.join(self.work_dir, f"opensearch-dashboards-{self.version}")

    def start(self):
        logging.info(f"Starting OpenSearch Dashboards service from {self.work_dir}")
        self.__download()

        self.opensearch_dashboards_yml_dir = os.path.join(self.install_dir, "config", "opensearch_dashboards.yml")
        self.executable_dir = os.path.join(self.install_dir, "bin")

        if not self.security_enabled:
            self.__remove_security()

        self.__set_logging_dest()

        if self.additional_config:
            self.__add_plugin_specific_config(self.additional_config)

        self.process_handler.start("./opensearch-dashboards", self.executable_dir)
        logging.info(f"Started OpenSearch Dashboards with parent PID {self.process_handler.pid}")

    def __set_logging_dest(self):
        self.log_dir = os.path.join(self.install_dir, "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        self.additional_config["logging.dest"] = os.path.join(self.log_dir, "opensearch_dashboards.log")

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

    def __add_plugin_specific_config(self, additional_config):
        with open(self.opensearch_dashboards_yml_dir, "a") as yamlfile:
            yamlfile.write(yaml.dump(additional_config))

    def port(self):
        return 5601

    def check_service_response_text(self, response_text):
        return ('"state":"green"' in response_text) or ('"state":"yellow"' in response_text)

    @property
    def log_files(self):
        return {"opensearch-dashboards-service-logs": os.path.join(self.install_dir, "logs")}
