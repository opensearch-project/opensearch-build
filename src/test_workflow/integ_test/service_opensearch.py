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


class ServiceOpenSearch(Service):
    def __init__(
        self,
        filename,
        version,
        distribution,
        additional_config,
        security_enabled,
        dependency_installer,
        work_dir
    ):
        super().__init__(work_dir, filename, version, distribution, security_enabled, additional_config, dependency_installer)

        self.dependency_installer = dependency_installer
        self.filename = filename
        self.distribution = distribution

        logging.info(f'{self.filename} distribution: {self.distribution}')
        self.install_dir = self.install_dir_map[self.distribution]

    def start(self):
        self.__download()

        self.opensearch_yml_dir = self.config_file_map[self.distribution]
        self.security_plugin_dir = os.path.join(self.install_dir, "plugins", "opensearch-security")

        if not self.security_enabled and os.path.isdir(self.security_plugin_dir):
            self.__add_plugin_specific_config({"plugins.security.disabled": "true"})

        if self.additional_config:
            self.__add_plugin_specific_config(self.additional_config)

        self.process_handler.start(self.start_cmd_map[f"{self.distribution}-{self.filename}"], self.install_dir)
        logging.info(f"Started OpenSearch with parent PID {self.process_handler.pid}")

    def __download(self):
        logging.info(f"Creating local test cluster in {self.work_dir}")
        logging.info("Downloading bundle")
        bundle_name = self.dependency_installer.download_dist(self.work_dir)
        logging.info(f"Downloaded bundle to {os.path.realpath(bundle_name)}")

        logging.info(f"Installing {bundle_name} in {self.install_dir}")

        if self.distribution == "tar":
            with tarfile.open(bundle_name, 'r') as bundle_tar:
                bundle_tar.extractall(self.work_dir)
        elif self.distribution == "rpm":
            logging.info("rpm installation requires sudo, script will exit if current user does not have sudo access")
            rpm_install_cmd = " ".join(
                [
                    'yum',
                    'remove',
                    '-y',
                    self.filename,
                    '&&',
                    'yum',
                    'install',
                    '-y',
                    bundle_name
                ]
            )
            subprocess.check_call(rpm_install_cmd, cwd=self.work_dir, shell=True)
        else:
            raise(f'{self.distribution} is not supported in integ-test yet')

        logging.info(f"Installed {bundle_name}")

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
