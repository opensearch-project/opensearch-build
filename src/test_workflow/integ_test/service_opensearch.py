# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os

import requests
import yaml
from requests.models import Response

from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.integ_test.distribution import Distribution
from test_workflow.integ_test.distributions import Distributions
from test_workflow.integ_test.service import Service
from test_workflow.integ_test.utils import get_password


class ServiceOpenSearch(Service):
    dist: Distribution
    dependency_installer: DependencyInstaller
    install_dir: str
    opensearch_yml_path: str
    security_plugin_dir: str

    def __init__(
        self,
        version: str,
        distribution: str,
        additional_config: dict,
        security_enabled: bool,
        dependency_installer: DependencyInstaller,
        work_dir: str,
        cluster_port: int = 9200
    ) -> None:
        super().__init__(work_dir, version, distribution, security_enabled, additional_config, dependency_installer)
        self.cluster_port = cluster_port
        self.dist = Distributions.get_distribution("opensearch", distribution, version, work_dir)
        self.dependency_installer = dependency_installer
        self.install_dir = self.dist.install_dir

    def start(self) -> None:
        self.dist.install(self.download())
        self.dist.configure_jvm_options([("-Xms1g", "-Xms2g"), ("-Xmx1g", "-Xmx2g")])

        self.opensearch_yml_path = self.dist.config_path
        self.security_plugin_dir = os.path.join(self.install_dir, "plugins", "opensearch-security")

        if not self.security_enabled and os.path.isdir(self.security_plugin_dir):
            # Disable the security plugin, and remove any configured audit sink so audit logging
            # stays fully off. In disabled mode the plugin still initializes standalone audit
            # whenever plugins.security.audit.type is set (the distribution's demo config sets it
            # to internal_opensearch), which asynchronously writes to security-auditlog-* indices;
            # those writes can linger past a test and break teardown task-wait checks. Stripping
            # audit.type leaves it unset, so the plugin uses a NullAuditLog and registers no audit
            # filter/interceptor at all.
            self.__remove_plugin_specific_config("plugins.security.audit.type")
            self.__add_plugin_specific_config({"plugins.security.disabled": "true"})

        if self.additional_config:
            self.__add_plugin_specific_config(self.additional_config)

        self.process_handler.start(self.dist.start_cmd, self.install_dir, self.dist.require_sudo)
        logging.info(f"Started OpenSearch with parent PID {self.process_handler.pid}")

    def uninstall(self) -> None:
        self.dist.uninstall()

    def url(self, path: str = "") -> str:
        return f'{"https" if self.security_enabled else "http"}://{self.endpoint()}:{self.port()}{path}'

    def get_service_response(self) -> Response:
        url = self.url("/_cluster/health")
        logging.info(f"Pinging {url}")
        return requests.get(url, verify=False, auth=("admin", get_password(self.version)))

    def __add_plugin_specific_config(self, additional_config: dict) -> None:
        with open(self.opensearch_yml_path, "a") as yamlfile:
            yamlfile.write(yaml.dump(additional_config))

    def __remove_plugin_specific_config(self, key: str) -> None:
        if not os.path.isfile(self.opensearch_yml_path):
            return
        with open(self.opensearch_yml_path, "r") as yamlfile:
            lines = yamlfile.readlines()
        with open(self.opensearch_yml_path, "w") as yamlfile:
            yamlfile.writelines(line for line in lines if not line.lstrip().startswith(key))

    def port(self) -> int:
        return self.cluster_port

    def check_service_response_text(self, response_text: str) -> bool:
        return ('"status":"green"' in response_text) or ('"status":"yellow"' in response_text)

    @property
    def log_files(self) -> dict:
        return {"opensearch-service-logs": os.path.join(self.install_dir, "logs")}
