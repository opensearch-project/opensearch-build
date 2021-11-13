import logging
import os
import subprocess
import time

import requests
from aws.s3_bucket import S3Bucket

from manifests.bundle_manifest import BundleManifest
from system.process import Process
from test_workflow.test_cluster import ClusterCreationException


class ServiceOpenSearchDashboards:
    """
    Kicks of integration tests for a component based on test configurations provided in
    test_support_matrix.yml
    """

    def __init__(
        self,
        work_dir,
        component_name,
        additional_cluster_config,
        bundle_manifest,
        security_enabled,
        component_test_config,
        save_logs,
        s3_bucket_name=None,
    ):
        self.manifest = bundle_manifest
        self.work_dir = work_dir
        os.makedirs(self.work_dir, exist_ok=True)
        self.component_name = component_name
        self.security_enabled = security_enabled
        self.component_test_config = component_test_config
        self.bucket_name = s3_bucket_name
        self.additional_cluster_config = additional_cluster_config
        self.process = None
        self.save_logs = save_logs
        self.process_handler = Process()

    def start(self):
        self.download()
        self.stdout = open("stdout.txt", "w")
        self.stderr = open("stderr.txt", "w")
        self.install_dir = BundleManifest.get_tarball_name_without_extension_for_dashboards(
            self.manifest.build.version,
            self.manifest.build.platform,
            self.manifest.build.architecture
        )

        self.process_handler.start("./bin/opensearch-dashboards", self.install_dir)

        logging.info(f"Started OpenSearch with parent PID {self.process_handler.pid}")
        self.wait_for_service()

    def download(self):
        logging.info(f"Creating local test cluster for dashboards in {self.work_dir}")
        os.chdir(self.work_dir)
        logging.info("Downloading bundle from s3")
        bundle_name = self.__download_tarball_from_s3()
        logging.info(f"Downloaded bundle to {os.path.realpath(bundle_name)}")
        logging.info("Unpacking")
        subprocess.check_call(f"tar -xzf {bundle_name}", shell=True)
        logging.info("Unpacked")

    def url(self, path=""):
        return f'{"https" if self.security_enabled else "http"}://{self.endpoint()}:{self.port()}{path}'

    def __download_tarball_from_s3(self):
        s3_path = BundleManifest.get_tarball_relative_location_for_dashboards(
            self.manifest.build.id,
            self.manifest.build.version,
            self.manifest.build.platform,
            self.manifest.build.architecture,
        )

        S3Bucket(self.bucket_name).download_file(s3_path, self.work_dir)
        return BundleManifest.get_tarball_name_for_dashboards(
            self.manifest.build.version,
            self.manifest.build.platform,
            self.manifest.build.architecture,
        )

    def wait_for_service(self):
        logging.info("Waiting for Dashboards service to become available")
        url = self.url("/api/status")

        for attempt in range(10):
            try:
                logging.info(f"Pinging {url} attempt {attempt}")
                response = requests.get(url, verify=False)

                logging.info(f"{response.status_code}: {response.text}")
                if response.status_code == 200 and ('"status":"green"' or '"status":"yellow"' in response.text):
                    logging.info("Service is available")
                    return
            except requests.exceptions.ConnectionError:
                logging.info("Service not available yet")
            time.sleep(10)
        raise ClusterCreationException("Cluster is not available after 10 attempts")

    def terminate_process(self):
        self.return_code, self.local_cluster_stdout, self.local_cluster_stderr = self.process_handler.terminate()

    def endpoint(self):
        return "localhost"

    def port(self):
        return 5601
