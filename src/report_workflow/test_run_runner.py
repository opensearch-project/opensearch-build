# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import sys
import os
import logging
import urllib.request
import yaml
from urllib.error import HTTPError
from typing import Any

from manifests.component_manifest import Components
from manifests.test_manifest import TestManifest
from system import console
import validators
from report_workflow.report_args import ReportArgs
from manifests.test_run_manifest import TestRunManifest





class TestRunRunner:
    args: ReportArgs
    test_manifest: TestManifest
    tests_dir: str
    test_run_manifest: TestRunManifest
    test_run_data: dict

    def __init__(self, args: ReportArgs, test_manifest: TestManifest) -> None:
        self.args = args
        self.base_path = args.base_path
        self.test_manifest = test_manifest
        self.test_run_data = self.test_run_manifest_data_template("manifest")
        self.product_name = test_manifest.__to_dict__().get("name")
        self.name = self.product_name.replace(" ", "-").lower()
        self.components = self.args.components # <list>
        self.test_run_id = args.test_run_id
        self.test_type = self.args.test_type
        self.test_manifest_path = self.args.test_manifest_path
        self.artifact_paths = ""
        for k, v in self.args.artifact_paths.items():
            self.artifact_paths = " ".join([self.artifact_paths, k + "=" + v]).strip(" ")

        #"https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar/dist/opensearch/manifest.yml"
        self.dist_manifest = "/".join([self.args.artifact_paths[self.name], "dist", self.name, "manifest.yml"])
        self.test_components = self.test_manifest.components

        logging.info("-------------------------test-run runner started-------------------------------")

    def generate_report(self, data: dict, output_dir: str = "/Users/zelinhao/workplace/reporting_system/reporting_workflow/opensearch-build") -> Any:
        test_run_manifest = TestRunManifest(data)
        test_run_manifetest_run_manifest_file = os.path.join(output_dir, "test-run.yml")
        test_run_manifest.to_file(test_run_manifetest_run_manifest_file)
        logging.info("-------------------------test-run.yml generated-------------------------------")
        self.update_test_run_data()
        return 0


    def update_data(self) -> dict:
        self.test_run_data["name"] = self.product_name
        self.test_run_data["test-run"] = self.update_test_run_data()
        for component in self.test_components.select(focus=self.args.components):
            self.test_run_data["components"].append(self.newComponent(component.name))
        return self.test_run_data

    def update_test_run_data(self) -> dict:

        #"https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar/dist/opensearch/manifest.yml"


        test_run_data = {
            "Command": generate_test_command(self.test_type, self.test_manifest_path, self.artifact_paths),
            "TestType": self.test_type,
            "TestManifest": self.test_manifest_path,
            "DistributionManifest": self.dist_manifest,
            "TestID": str(self.test_run_id)
        }
        return test_run_data

    def newComponent(self, component_name: str) -> dict:
        # component = {
        #     "name": "sql",
        #     "command": "./test.sh integ-test manifests/2.7.0/opensearch-2.7.0-test.yml --component sql --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar",
        #     "configs": [            # configs is a list of dict
        #         {
        #             "name": "with-security",
        #             "status": "pass",
        #             "yml": "https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/4967/integ-test/sql/with-security/sql.yml"
        #         },
        #         {
        #             "name": "without-security",
        #             "status": "fail",
        #             "yml": "https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/4967/integ-test/sql/without-security/sql.yml"
        #         }
        #     ]
        # }
        component = self.test_run_manifest_data_template("component")
        component["name"] = component_name
        component["command"] = generate_test_command(self.test_type, self.test_manifest_path, self.artifact_paths, component_name)
        component["configs"] = []
        # dict = {
        #     "name": "with-security",
        #     "status": "pass",
        #     "yml": "https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/4967/integ-test/sql/with-security/sql.yml"
        # }
        test_config = self.test_manifest.components[component_name] # TestComponent object

        config_names = [config for config in test_config.__to_dict__().get(self.test_type)["test-configs"]]
        logging.info(config_names)
        for config in config_names:
            logging.info(config)
            dict = {
                "name": config,
            }
            # component_yml_url = "https://ci.opensearch.org/ci/dbc/integ-test/2.8.0/7935/linux/x64/tar/test-results/5109/integ-test/sql/with-security/sql.yml"
            component_yml_url = generate_component_yml_url(self.base_path, str(self.test_run_id), self.test_type, component_name, config)
            logging.info(f"Loading {component_yml_url}")
            try:
                if validators.url(component_yml_url):
                        with urllib.request.urlopen(component_yml_url) as f:
                            component_yml = yaml.safe_load(f.read().decode("utf-8"))
                            test_result = component_yml["test_result"]
                            logging.info("this yml status" + test_result)

                else:
                    with open(component_yml_url, "r", encoding='utf8') as f:
                        component_yml = yaml.safe_load(f)
                        test_result = component_yml["test_result"]
                        logging.info("this yml status" + test_result)
            except (FileNotFoundError, HTTPError):
                test_result = "Not Available"
                component_yml_url = "URL not available"
            dict["yml"] = component_yml_url
            dict["status"] = test_result
            component["configs"].append(dict)
        return component

    def test_run_manifest_data_template(self, template_type: str) -> dict:
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




    def temp(self) -> dict:
        data = {
            "schema-version": "1.0",
            "name": "OpenSearch",
            "test-run": {
                "Command": "./test.sh integ-test manifests/2.8.6/opensearch-2.7.0-test.yml --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar",
                "TestType": "integ-test",
                "TestManifest": "manifests/2.7.0/opensearch-2.7.0-test.yml",
                "DistributionManifest": "https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar/dist/opensearch/manifest.yml",
                "TestID": "2345"
            },
            "components": [{
                "name": "sql",
                "command": "./test.sh integ-test manifests/2.7.0/opensearch-2.7.0-test.yml --component sql --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar",
                "configs": [            # configs is a list of dict
                    {
                        "name": "with-security",
                        "status": "pass",
                        "yml": "https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/4967/integ-test/sql/with-security/sql.yml"
                    },
                    {
                        "name": "without-security",
                        "status": "fail",
                        "yml": "https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/4967/integ-test/sql/without-security/sql.yml"
                    }
                ]
            },
                {
                    "name": "anomaly-detection",
                    "command": "./test.sh integ-test manifests/2.7.0/opensearch-2.7.0-test.yml --component anomaly-detection --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar",
                    "configs": [            # configs is a list of dict
                        {
                            "name": "with-security",
                            "status": "pass",
                            "yml": "https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/4967/integ-test/anomaly-detection/with-security/anomaly-detection.yml"
                        },
                        {
                            "name": "without-security",
                            "status": "fail",
                            "yml": "https://ci.opensearch.org/ci/dbc/integ-test/2.7.0/7771/linux/x64/tar/test-results/4967/integ-test/anomaly-detection/without-security/anomaly-detection.yml"
                        }
                    ]
                }
            ]
        }
        return data

def generate_component_yml_url(base_path: str, test_number: str, test_type: str, component_name: str, config: str) -> str:
    return "/".join([base_path, "test-results", test_number, test_type, component_name, config, f"{component_name}.yml"])
    # return "https://ci.opensearch.org/ci/dbc/integ-test/2.8.0/7935/linux/x64/tar/test-results/5109/integ-test/sql/with-security/sql.yml"


def generate_test_command(test_type: str, test_manifest_path: str, artifacts_path: str, component: str = "") -> str:
    # "./test.sh integ-test manifests/2.8.6/opensearch-2.7.0-test.yml --paths opensearch=https://ci.opensearch.org/ci/dbc/distribution-build-opensearch/2.7.0/7771/linux/x64/tar"
    command = " ".join(["./test.sh", test_type, test_manifest_path, "--paths", artifacts_path])
    if component is not None:
        command = " ".join([command, "--component", component])
    logging.info(command)
    return command


TestRunRunner.__test__ = False  # type:ignore
