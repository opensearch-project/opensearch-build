# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import itertools
import os
import subprocess
import time
import urllib.request

import requests

from paths.tree_walker import walk
from test_workflow.test_cluster import ClusterCreationException, TestCluster


class LocalTestCluster(TestCluster):
    """
    Represents an on-box test cluster. This class downloads a bundle (from a BundleManifest) and runs it as a background process.
    """

    def __init__(self, work_dir, bundle_manifest, security_enabled):
        self.manifest = bundle_manifest
        self.work_dir = os.path.join(work_dir, "local-test-cluster")
        os.makedirs(self.work_dir, exist_ok=True)
        self.security_enabled = security_enabled
        self.process = None

    def create(self):
        self.download()
        self.stdout = open("stdout.txt", "w")
        self.stderr = open("stderr.txt", "w")
        self.install_dir = f"opensearch-{self.manifest.build.version}"
        if not self.security_enabled:
            self.disable_security(self.install_dir)
        self.process = subprocess.Popen(
            "./opensearch-tar-install.sh",
            cwd=self.install_dir,
            shell=True,
            stdout=self.stdout,
            stderr=self.stderr,
        )
        print(f"Started OpenSearch with PID {self.process.pid}")
        self.wait_for_service()

    def endpoint(self):
        return "localhost"

    def port(self):
        return 9200

    def destroy(self, test_recorder):
        if self.process is None:
            print("Local test cluster is not started")
            return
        self.terminate_process()
        test_recorder.record_cluster_logs(
            itertools.chain(
                [
                    (os.path.realpath(self.stdout.name), "stdout"),
                    (os.path.realpath(self.stderr.name), "stderr"),
                ],
                walk(os.path.join(self.install_dir, "logs")),
            )
        )

    def url(self, path=""):
        return f'{"https" if self.security_enabled else "http"}://{self.endpoint()}:{self.port()}{path}'

    def download(self):
        print(f"Creating local test cluster in {self.work_dir}")
        os.chdir(self.work_dir)
        print(f"Downloading bundle from {self.manifest.build.location}")
        urllib.request.urlretrieve(self.manifest.build.location, "bundle.tgz")
        print(f'Downloaded bundle to {os.path.realpath("bundle.tgz")}')

        print("Unpacking")
        subprocess.check_call("tar -xzf bundle.tgz", shell=True)
        print("Unpacked")

    def disable_security(self, dir):
        subprocess.check_call(
            f'echo "plugins.security.disabled: true" >> {os.path.join(dir, "config", "opensearch.yml")}',
            shell=True,
        )

    def wait_for_service(self):
        print("Waiting for service to become available")
        url = self.url("/_cluster/health")

        for attempt in range(10):
            try:
                print(f"Pinging {url} attempt {attempt}")
                response = requests.get(url, verify=False, auth=("admin", "admin"))
                print(f"{response.status_code}: {response.text}")
                if response.status_code == 200 and '"status":"green"' in response.text:
                    print("Cluster is green")
                    return
            except requests.exceptions.ConnectionError:
                print("Service not available yet")
            time.sleep(10)
        raise ClusterCreationException("Cluster is not green after 10 attempts")

    def terminate_process(self):
        print(f"Sending SIGTERM to PID {self.process.pid}")
        self.process.terminate()
        try:
            print("Waiting for process to terminate")
            self.process.wait(10)
        except subprocess.TimeoutExpired:
            print("Process did not terminate after 10 seconds. Sending SIGKILL")
            self.process.kill()
            try:
                print("Waiting for process to terminate")
                self.process.wait(10)
            except subprocess.TimeoutExpired:
                print("Process failed to terminate even after SIGKILL")
                raise
        finally:
            print(f"Process terminated with exit code {self.process.returncode}")
            self.stdout.close()
            self.stderr.close()
            self.process = None
