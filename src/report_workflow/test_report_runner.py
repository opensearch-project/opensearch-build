# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import typing
import urllib.request
from typing import Any
from urllib.error import HTTPError

import validators
import yaml
from bs4 import BeautifulSoup

from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestManifest
from manifests.test_report_manifest import TestReportManifest
from report_workflow.report_args import ReportArgs


class TestReportRunner:
    args: ReportArgs
    test_manifest: TestManifest
    tests_dir: str
    test_report_manifest: TestReportManifest
    test_report_data: dict
    bundle_manifest: BundleManifest

    def __init__(self, args: ReportArgs, test_manifest: TestManifest) -> None:
        self.args = args
        self.base_path = args.base_path
        self.test_manifest = test_manifest
        self.release_candidate = self.args.release_candidate
        self.test_report_data = self.test_report_manifest_data_template("manifest")
        self.product_name = test_manifest.__to_dict__().get("name")
        self.name = self.product_name.replace(" ", "-").lower()
        self.components = self.args.components
        self.test_run_id = args.test_run_id
        self.test_type = self.args.test_type
        self.test_manifest_path = self.args.test_manifest_path
        self.artifact_paths = ""
        for k, v in self.args.artifact_paths.items():
            self.artifact_paths = " ".join([self.artifact_paths, k + "=" + v]).strip(" ")

        self.dist_manifest = "/".join([self.args.artifact_paths[self.name], "dist", self.name, "manifest.yml"]) if self.args.artifact_paths[self.name].startswith("https://") \
            else os.path.join(self.args.artifact_paths[self.name], "dist", self.name, "manifest.yml")
        self.test_components = self.test_manifest.components
        self.bundle_manifest = BundleManifest.from_urlpath(self.dist_manifest)
        self.bundle_components_list = []
        for component in self.bundle_manifest.components.select(focus=self.args.components):
            self.bundle_components_list.append(component.name)

    def update_data(self) -> dict:
        self.test_report_data["name"] = self.product_name
        self.test_report_data["version"] = self.bundle_manifest.build.version
        self.test_report_data["platform"] = self.bundle_manifest.build.platform
        self.test_report_data["architecture"] = self.bundle_manifest.build.architecture
        self.test_report_data["distribution"] = self.bundle_manifest.build.distribution
        self.test_report_data["id"] = self.bundle_manifest.build.id
        self.test_report_data["rc"] = self.release_candidate
        self.test_report_data["test-run"] = self.update_test_run_data()
        for component in self.test_components.select(focus=self.args.components):
            if component.name not in self.bundle_components_list:
                logging.info(f"Skipping {component.name} as it's not included in the bundle manifest.")
                continue
            if self.test_manifest.components[component.name].__to_dict__().get(self.test_type) is not None:
                component_ci_group = getattr(component, self.test_type.replace("-", "_")).get("ci-groups", None)
                if component_ci_group:
                    for i in range(component_ci_group):
                        self.test_report_data["components"].append(self.component_entry(component.name, i + 1))
                else:
                    self.test_report_data["components"].append(self.component_entry(component.name))
        return self.test_report_data

    def update_test_run_data(self) -> dict:
        test_run_data = {
            "Command": generate_test_command(self.test_type, self.test_manifest_path, self.artifact_paths),
            "TestType": self.test_type,
            "TestManifest": self.test_manifest_path,
            "DistributionManifest": self.dist_manifest,
            "TestID": str(self.test_run_id)
        }
        return test_run_data

    def generate_report(self, data: dict, output_dir: str) -> Any:
        test_report_manifest = TestReportManifest(data)
        test_report_manifest_file = os.path.join(output_dir, "test-report.yml")
        logging.info(f"Generating test-report.yml in {output_dir}")
        return test_report_manifest.to_file(test_report_manifest_file)

    def component_entry(self, component_name: str, ci_group: int = None) -> Any:
        component = self.test_report_manifest_data_template("component")
        test_report_component_name = component_name if not ci_group else f"{component_name}-ci-group-{ci_group}"
        component["name"] = test_report_component_name
        component["command"] = generate_test_command(self.test_type, self.test_manifest_path, self.artifact_paths, component_name)
        component["repository"] = self.bundle_manifest.components[component_name].repository

        test_component = self.test_manifest.components[component_name]

        config_names = [config for config in test_component.__to_dict__().get(self.test_type)["test-configs"]]
        logging.info(f"Configs for {component_name} on {self.test_type} are {config_names}")
        for config in config_names:
            config_dict = {
                "name": config,
            }

            component_yml_ref = generate_component_yml_ref(self.base_path, str(self.test_run_id), self.test_type, test_report_component_name, config)
            logging.info(f"Loading {component_yml_ref}")
            try:
                if validators.url(component_yml_ref):
                    with urllib.request.urlopen(component_yml_ref) as f:
                        component_yml = yaml.safe_load(f.read().decode("utf-8"))
                else:
                    with open(component_yml_ref, "r", encoding='utf8') as f:
                        component_yml = yaml.safe_load(f)

                test_result = component_yml["test_result"]

                # Issues with windows where certain path separator are encoded as `%5C`
                if self.name == "opensearch":
                    test_result_files = [f.replace("%5C", "/") for f in component_yml["test_result_files"] if f.endswith("index.html")]
                else:
                    test_result_files = [f.replace("%5C", "/") for f in component_yml["test_result_files"] if f.endswith(".xml")]

            except (FileNotFoundError, HTTPError):
                logging.info(f"Component yml file for {component_name} for {config} is missing or the base path is incorrect.")
                test_result = "Not Available"
                test_result_files = []
                component_yml_ref = "URL not available"
            config_dict["yml"] = component_yml_ref
            config_dict["status"] = test_result
            config_dict["test_stdout"] = get_test_logs(self.base_path, str(self.test_run_id), self.test_type, test_report_component_name, config, self.name)[0]
            config_dict["test_stderr"] = get_test_logs(self.base_path, str(self.test_run_id), self.test_type, test_report_component_name, config, self.name)[1]
            config_dict["cluster_stdout"] = get_os_cluster_logs(self.base_path, str(self.test_run_id), self.test_type, test_report_component_name, config, self.name)[0]
            config_dict["cluster_stderr"] = get_os_cluster_logs(self.base_path, str(self.test_run_id), self.test_type, test_report_component_name, config, self.name)[1]
            config_dict["failed_test"] = get_failed_tests(self.name, test_result, test_result_files)
            component["configs"].append(config_dict)
        return component

    def test_report_manifest_data_template(self, template_type: str) -> Any:
        templates = {
            "manifest": {
                "schema-version": "1.1",
                "name": "",
                "version": "",
                "platform": "",
                "architecture": "",
                "distribution": "",
                "id": "",
                "rc": "",
                "test-run": {},
                "components": []
            },
            "component": {
                "name": "",
                "command": "",
                "configs": []
            }
        }

        return templates[template_type]


def generate_component_yml_ref(base_path: str, test_number: str, test_type: str, component_name: str,
                               config: str) -> str:
    if base_path.startswith("https://"):
        return "/".join([base_path.strip("/"), "test-results", test_number, test_type, component_name, config,
                         f"{component_name}.yml"])
    else:
        return os.path.join(base_path, "test-results", test_number, test_type, component_name, config,
                            f"{component_name}.yml")


def generate_test_command(test_type: str, test_manifest_path: str, artifacts_path: str, component: str = "") -> str:
    command = " ".join(["./test.sh", test_type, test_manifest_path, "--paths", artifacts_path])
    if component:
        command = " ".join([command, "--component", component])
    logging.info(command)
    return command


def get_test_logs(base_path: str, test_number: str, test_type: str, component_name: str, config: str,
                  product_name: str) -> typing.List[str]:
    if base_path.startswith("https://"):
        return ["/".join([base_path.strip("/"), "test-results", test_number, test_type, component_name, config, "stdout.txt"]),
                "/".join([base_path.strip("/"), "test-results", test_number, test_type, component_name, config, "stderr.txt"])]
    else:
        return [os.path.join(base_path, "test-results", test_number, test_type, component_name, config, "stdout.txt"),
                os.path.join(base_path, "test-results", test_number, test_type, component_name, config, "stderr.txt")]


def get_os_cluster_logs(base_path: str, test_number: str, test_type: str, component_name: str, config: str,
                        product_name: str) -> typing.List[list]:
    os_stdout: list = []
    os_stderr: list = []
    cluster_ids: list

    if product_name == 'opensearch':
        cluster_ids = ['id-0'] if config == 'with-security' else ['id-1']
    else:
        cluster_ids = ['id-0', 'id-1'] if config == 'with-security' else ['id-2', 'id-3']

    for ids in cluster_ids:
        if base_path.startswith("https://"):
            os_stdout.append("/".join([base_path.strip("/"), "test-results", test_number, test_type, component_name, config, "local-cluster-logs", ids, "stdout.txt"]))
            os_stderr.append("/".join([base_path.strip("/"), "test-results", test_number, test_type, component_name, config, "local-cluster-logs", ids, "stderr.txt"]))
        else:
            os_stdout.append(os.path.join(base_path, "test-results", test_number, test_type, component_name, config, "local-cluster-logs", ids, "stdout.txt"))
            os_stderr.append(os.path.join(base_path, "test-results", test_number, test_type, component_name, config, "local-cluster-logs", ids, "stderr.txt"))

    return [os_stdout, os_stderr]


def get_failed_tests(product_name: str, test_result: str, test_result_files: list) -> typing.List[list]:
    failed_test_list: list = []
    result_path_list: list = []

    if test_result == "PASS":
        failed_test_list.append("No Failed Test")
        return failed_test_list

    if test_result == "Not Available":
        failed_test_list.append("Test Result Not Available")
        return failed_test_list

    if test_result_files:
        result_path_list = test_result_files
    else:
        failed_test_list.append("Test Result Files List Not Available")
        return failed_test_list

    for result_path in result_path_list:
        logging.info(f"Processing {result_path}")
        result_content: str = ''
        try:
            if validators.url(result_path):
                with urllib.request.urlopen(result_path) as f:
                    result_content = f.read().decode("utf-8")
            else:
                with open(result_path, "r", encoding='utf8') as f:
                    result_content = f.read()
        except (FileNotFoundError, HTTPError):
            logging.info(f"Test Result File Not Available {result_path}")
            failed_test_list.append("Test Result File Not Available")
            return failed_test_list

        if not result_content:
            logging.info(f"Test Result File Has No Content {result_path}")
            failed_test_list.append("Test Result File Has No Content")
            return failed_test_list

        if product_name == 'opensearch':
            soup = BeautifulSoup(result_content, "html.parser")
            target_div = soup.find("div", {"id": "tab0"})
            target_a_hash = [a for li in target_div.find_all("li") for a in li.find_all("a", href=True) if "#" in a["href"]]
            for a in target_a_hash:
                failed_test_list.append(a["href"].replace("classes/", "").replace(".html", ""))
        else:
            soup = BeautifulSoup(result_content, "xml")
            class_name = "DefaultClassName"
            for testsuite in soup.find_all("testsuite"):
                if testsuite["name"] == "Root Suite":
                    class_name = os.path.basename(testsuite["file"])
                testsuite_failures = int(testsuite["failures"])
                if testsuite_failures > 0:
                    for testcase in testsuite.find_all("testcase"):
                        if testcase.find("failure"):
                            failed_test_list.append(f"{class_name}#{testcase['name']}")

    return failed_test_list


TestReportRunner.__test__ = False  # type:ignore
