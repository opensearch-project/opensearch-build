# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess

import requests
import yaml
from requests.models import Response

from system.os import current_platform
from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.integ_test.distribution import Distribution
from test_workflow.integ_test.distributions import Distributions
from test_workflow.integ_test.service import Service
from test_workflow.integ_test.utils import get_password


class ServiceOpenSearchDashboards(Service):
    dist: Distribution
    install_dir: str
    opensearch_dashboards_yml_path: str
    executable_dir: str

    def __init__(
        self,
        version: str,
        distribution: str,
        additional_config: dict,
        security_enabled: bool,
        dependency_installer: DependencyInstaller,
        work_dir: str
    ) -> None:
        super().__init__(work_dir, version, distribution, security_enabled, additional_config, dependency_installer)
        self.dist = Distributions.get_distribution("opensearch-dashboards", distribution, version, work_dir)
        self.install_dir = self.dist.install_dir

    def start(self) -> None:
        self.dist.install(self.download())

        self.opensearch_dashboards_yml_path = self.dist.config_path
        self.executable_dir = os.path.join(self.install_dir, "bin")

        if not self.security_enabled:
            self.__remove_security()

        self.__set_logging_dest()

        # Newer version of NodeJS (16/18) might introduced bug when running test against localhost using cypress
        # https://github.com/cypress-io/github-action/issues/811
        # Temporarily set these additional configs to resolve the issue
        self.additional_config["server.host"] = '0.0.0.0'

        if self.additional_config:
            self.__add_plugin_specific_config(self.additional_config)

        self.process_handler.start(self.dist.start_cmd, self.executable_dir, self.dist.require_sudo)
        logging.info(f"Started OpenSearch Dashboards with parent PID {self.process_handler.pid}")

    def uninstall(self) -> None:
        self.dist.uninstall()

    def __set_logging_dest(self) -> None:
        self.log_dir = os.path.join(self.install_dir, "logs")
        os.makedirs(self.log_dir, exist_ok=True)
        self.additional_config["logging.dest"] = os.path.join(self.log_dir, "opensearch_dashboards.log")

    def __remove_security(self) -> None:
        self.security_plugin_dir = os.path.join(self.install_dir, "plugins", "securityDashboards")
        if os.path.isdir(self.security_plugin_dir):
            plugin_script = "opensearch-dashboards-plugin.bat" if current_platform() == "windows" else "opensearch-dashboards-plugin"
            plugin_script = os.path.join(self.executable_dir, plugin_script)
            plugin_script = "sudo " + plugin_script if self.dist.require_sudo is True else plugin_script
            subprocess.check_call(f"{plugin_script} remove --allow-root securityDashboards", cwd=self.executable_dir, shell=True)

        with open(self.opensearch_dashboards_yml_path, "w") as yamlfile:
            yamlfile.close()

    def url(self, path: str = "") -> str:
        return f'http://{self.endpoint()}:{self.port()}{path}'

    def get_service_response(self) -> Response:
        url = self.url("/api/status")
        logging.info(f"Pinging {url}")
        return requests.get(url, verify=False, auth=("admin", get_password(self.version)) if self.security_enabled else None)

    def __add_plugin_specific_config(self, additional_config: dict) -> None:
        with open(self.opensearch_dashboards_yml_path, "a") as yamlfile:
            yamlfile.write(yaml.dump(additional_config))

    def port(self) -> int:
        return 5601

    def check_service_response_text(self, response_text: str) -> bool:
        return ('"state":"green"' in response_text) or ('"state":"yellow"' in response_text)

    @property
    def log_files(self) -> dict:
        return {"opensearch-dashboards-service-logs": os.path.join(self.install_dir, "logs")}
