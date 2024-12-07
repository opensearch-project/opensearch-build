# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import shutil
import time

import requests

from git.git_repository import GitRepository
from manifests.build_manifest import BuildManifest
from manifests.bundle_manifest import BundleManifest
from manifests.test_manifest import TestManifest
from system.process import Process
from test_workflow.integ_test.distributions import Distributions
from test_workflow.test_args import TestArgs
from test_workflow.test_recorder.test_recorder import TestRecorder


class SmokeTestClusterOpenSearch():
    # dependency_installer: DependencyInstallerOpenSearch
    repo: GitRepository

    def __init__(
        self,
        args: TestArgs,
        work_dir: str,
        test_recorder: TestRecorder
    ) -> None:
        self.args = args
        self.work_dir = work_dir
        self.test_recorder = test_recorder
        self.process_handler = Process()
        self.test_manifest = TestManifest.from_path(args.test_manifest_path)
        self.product = self.test_manifest.name.lower().replace(" ", "-")
        self.path = args.paths.get(self.product)
        self.build_manifest = BuildManifest.from_urlpath(os.path.join(self.path, "builds", f"{self.product}", "manifest.yml"))
        self.bundle_manifest = BundleManifest.from_urlpath(os.path.join(self.path, "dist", f"{self.product}", "manifest.yml"))
        self.version = self.bundle_manifest.build.version
        self.platform = self.bundle_manifest.build.platform
        self.arch = self.bundle_manifest.build.architecture
        self.dist = self.bundle_manifest.build.distribution
        self.distribution = Distributions.get_distribution(self.product, self.dist, self.version, work_dir)

    def cluster_version(self) -> str:
        return self.version

    def download_or_copy_bundle(self, work_dir: str) -> str:
        extension = "tar.gz" if self.dist == "tar" else self.dist
        artifact_name = f"{self.product}-{self.version}-{self.platform}-{self.arch}.{extension}"
        src_path = '/'.join([self.path.rstrip("/"), "dist", f"{self.product}", f"{artifact_name}"]) \
            if self.path.startswith("https://") else os.path.join(self.path, "dist",
                                                                  f"{self.product}", f"{artifact_name}")
        dest_path = os.path.join(work_dir, artifact_name)

        if src_path.startswith("https://"):
            logging.info(f"Downloading artifacts to {dest_path}")
            response = requests.get(src_path)
            with open(dest_path, "wb") as file:
                file.write(response.content)
        else:
            logging.info(f"Trying to copy {src_path} to {dest_path}")
            # Only copy if it's a file
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dest_path)
                logging.info(f"Copied {src_path} to {dest_path}")
        return artifact_name

    # Reason we don't re-use test-suite from integ-test is that it's too specific and not generic and lightweight.
    def __installation__(self, work_dir: str) -> None:
        self.distribution.install(self.download_or_copy_bundle(work_dir))
        logging.info("Cluster is installed and ready to be start.")

    # Start the cluster after installed and provide endpoint.
    def __start_cluster__(self, work_dir: str) -> None:
        self.__installation__(work_dir)
        self.process_handler.start(self.distribution.start_cmd, self.distribution.install_dir, self.distribution.require_sudo)
        logging.info(f"Started OpenSearch with parent PID {self.process_handler.pid}")
        time.sleep(30)
        logging.info("Cluster is started.")

    # Check if the cluster is ready
    def __check_cluster_ready__(self) -> bool:
        url = "https://localhost:9200/"
        logging.info(f"Pinging {url}")
        try:
            request = requests.get(url, verify=False, auth=("admin", "myStrongPassword123!"))
            logging.info(f"Cluster response is {request.text}")
            return 200 <= request.status_code < 300
        except requests.RequestException as e:
            logging.info(f"Request is {request.text}")
            logging.info(f"Cluster check fails: {e}")
            return False

    def __uninstall__(self) -> None:
        self.process_handler.terminate()
        logging.info("Cluster is terminated.")
