# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import logging
import os
import subprocess

from git.git_repository import GitRepository
from paths.script_finder import ScriptFinder
from system.execute import execute
from test_workflow.integ_test.local_test_cluster import LocalTestCluster


class IntegTestSuite:
    """
    Kicks of integration tests for a component based on test configurations provided in
    test_support_matrix.yml
    """

    def __init__(self, component, test_config, bundle_manifest, work_dir, s3_bucket_name):
        self.component = component
        self.bundle_manifest = bundle_manifest
        self.work_dir = work_dir
        self.test_config = test_config
        self.s3_bucket_name = s3_bucket_name
        self.script_finder = ScriptFinder()
        self.repo = GitRepository(
            self.component.repository,
            self.component.commit_id,
            os.path.join(self.work_dir, self.component.name),
        )

    def execute(self):
        self._fetch_plugin_specific_dependencies()
        for config in self.test_config.integ_test["test-configs"]:
            self._setup_cluster_and_execute_test_config(config)

    # TODO: fetch pre-built dependencies from s3
    def _fetch_plugin_specific_dependencies(self):
        dependencies_dir = os.path.join(self.work_dir, 'dependencies')
        os.chdir(self.work_dir)
        subprocess.check_output(
            "cp -r dependencies/job-scheduler " + self.component.name, cwd=self.work_dir, shell=True
        )
        job_scheduler_dir = os.path.join(self.work_dir, self.component.name, 'job-scheduler')
        os.chdir(job_scheduler_dir)
        deps_script = os.path.join(
            self.work_dir,
            "opensearch-build/tools/standard-test/integtest_dependencies_opensearch.sh",
        )
        subprocess.check_output(
            f"{deps_script} job-scheduler {self.bundle_manifest.build.version}",
            cwd=job_scheduler_dir,
            shell=True
        )
        os.chdir(dependencies_dir)
        if not (os.path.isdir('notifications')):
            subprocess.check_output("cp -r alerting notifications", cwd=dependencies_dir, shell=True)
        notifications_dir = os.path.join(dependencies_dir, 'notifications')
        os.chdir(notifications_dir)
        subprocess.check_output(
            f"{deps_script} alerting {self.bundle_manifest.build.version}",
            cwd=notifications_dir,
            shell=True
        )

    # TODO: revisit this once the test_manifest.yml is finalized
    def _is_security_enabled(self, config):
        # TODO: Separate this logic in function once we have test-configs defined
        if config == "with-security":
            return True
        else:
            return False

    def _setup_cluster_and_execute_test_config(self, config):
        security = self._is_security_enabled(config)
        with LocalTestCluster.create(self.work_dir, self.bundle_manifest, security, self.s3_bucket_name) as (test_cluster_endpoint, test_cluster_port):
            logging.info("component name: " + self.component.name)
            os.chdir(self.work_dir)
            # TODO: (Create issue) Since plugins don't have integtest.sh in version branch, hardcoded it to main
            self._execute_integtest_sh(test_cluster_endpoint, test_cluster_port, security)

    def _execute_integtest_sh(self, endpoint, port, security):
        script = self.script_finder.find_integ_test_script(
            self.component.name, self.repo.dir
        )
        if os.path.exists(script):
            cmd = f"{script} -b {endpoint} -p {port} -s {str(security).lower()} -v {self.bundle_manifest.build.version}"
            (status, stdout, stderr) = execute(cmd, self.repo.dir, True, False)
        else:
            logging.info(
                f"{script} does not exist. Skipping integ tests for {self.name}"
            )
