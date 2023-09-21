# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import urllib.request
from typing import Any
from urllib.error import HTTPError

import validators
import yaml

from manifests.test_manifest import TestManifest
from manifests.test_report_manifest import TestReportManifest
from report_workflow.report_args import ReportArgs


class TestReportRunner:
    args: ReportArgs
    test_manifest: TestManifest
    tests_dir: str
    test_report_manifest: TestReportManifest
    test_run_data: dict

    def __init__(self, args: ReportArgs, test_manifest: TestManifest) -> None:
        self.args = args
        self.base_path = args.base_path
        self.test_manifest = test_manifest
        self.test_run_data = self.test_report_manifest_data_template("manifest")
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

    def update_data(self) -> dict:
        self.test_run_data["name"] = self.product_name
        self.test_run_data["test-run"] = self.update_test_run_data()
        for component in self.test_components.select(focus=self.args.components):
            if self.test_manifest.components[component.name].__to_dict__().get(self.test_type) is not None:
                self.test_run_data["components"].append(self.component_entry(component.name))
        return self.test_run_data

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

    def component_entry(self, component_name: str) -> Any:
        component = self.test_report_manifest_data_template("component")
        component["name"] = component_name
        component["command"] = generate_test_command(self.test_type, self.test_manifest_path, self.artifact_paths, component_name)

        test_component = self.test_manifest.components[component_name]

        config_names = [config for config in test_component.__to_dict__().get(self.test_type)["test-configs"]]
        logging.info(f"Configs for {component_name} on {self.test_type} are {config_names}")
        for config in config_names:
            config_dict = {
                "name": config,
            }

            component_yml_ref = generate_component_yml_ref(self.base_path, str(self.test_run_id), self.test_type, component_name, config)
            logging.info(f"Loading {component_yml_ref}")
            try:
                if validators.url(component_yml_ref):
                    with urllib.request.urlopen(component_yml_ref) as f:
                        component_yml = yaml.safe_load(f.read().decode("utf-8"))
                        test_result = component_yml["test_result"]
                else:
                    with open(component_yml_ref, "r", encoding='utf8') as f:
                        component_yml = yaml.safe_load(f)
                        test_result = component_yml["test_result"]
            except (FileNotFoundError, HTTPError):
                logging.info(f"Component yml file for {component_name} for {config} is missing or the base path is incorrect.")
                test_result = "Not Available"
                component_yml_ref = "URL not available"
            config_dict["yml"] = component_yml_ref
            config_dict["status"] = test_result
            component["configs"].append(config_dict)
        return component

    def test_report_manifest_data_template(self, template_type: str) -> Any:
        templates = {
            "manifest": {
                "schema-version": "1.0",
                "name": "",
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


def generate_component_yml_ref(base_path: str, test_number: str, test_type: str, component_name: str, config: str) -> str:
    if base_path.startswith("https://"):
        return "/".join([base_path.strip("/"), "test-results", test_number, test_type, component_name, config, f"{component_name}.yml"])
    else:
        return os.path.join(base_path, "test-results", test_number, test_type, component_name, config, f"{component_name}.yml")


def generate_test_command(test_type: str, test_manifest_path: str, artifacts_path: str, component: str = "") -> str:
    command = " ".join(["./test.sh", test_type, test_manifest_path, "--paths", artifacts_path])
    if component:
        command = " ".join([command, "--component", component])
    logging.info(command)
    return command


TestReportRunner.__test__ = False  # type:ignore
