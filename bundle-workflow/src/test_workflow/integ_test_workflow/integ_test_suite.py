# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import subprocess

from git.git_repository import GitRepository
from paths.script_finder import ScriptFinder
from test_workflow.local_test_cluster import LocalTestCluster


class IntegTestSuite:
    """
    Kicks of integration tests for a component based on test configurations provided in
    test_support_matrix.yml
    """
    def __init__(self, component, test_config, bundle_manifest, work_dir):
        self.component = component
        self.bundle_manifest = bundle_manifest
        self.work_dir = work_dir
        self.test_config = test_config
        self.script_finder = ScriptFinder()
        self.repo = GitRepository(self.component.repository, self.component.commit_id, os.path.join(self.work_dir, self.component.name))

    def execute(self):
        self._fetch_plugin_specific_dependencies()
        for config in self.test_config.integ_test['test-configs']:
            self._setup_cluster_and_execute_test_config(config)

    def _fetch_plugin_specific_dependencies(self):
        os.chdir(self.work_dir)
        subprocess.run('mv -v job-scheduler ' + self.component.name, shell=True)
        os.chdir(self.work_dir + '/' + self.component.name + '/job-scheduler')
        subprocess.run(self.work_dir +
                       '/opensearch-build/tools/standard-test/integtest_dependencies_opensearch.sh job-scheduler ' +
                       self.bundle_manifest.build.version, shell=True)
        os.chdir(self.work_dir)
        subprocess.run('mv alerting notifications', shell=True)
        os.chdir(self.work_dir + '/' + '/notifications')
        subprocess.run(self.work_dir +
                       '/opensearch-build/tools/standard-test/integtest_dependencies_opensearch.sh alerting ' +
                       self.bundle_manifest.build.version, shell=True)

    def _is_security_enabled(self, config):
        # TODO: Separate this logic in function once we have test-configs defined
        if config == 'with-security':
            return True
        else:
            return False

    def _setup_cluster_and_execute_test_config(self, config):
        security = self._is_security_enabled(config)
        try:
            # Spin up a test cluster
            cluster = LocalTestCluster(self.work_dir, self.bundle_manifest, security)
            cluster.create()
            print("component name: " + self.component.name)
            os.chdir(self.work_dir)
            # TODO: (Create issue) Since plugins don't have integtest.sh in version branch, hardcoded it to main
            # repo = GitRepository(component.repository, component.commit_id, os.path.join(work_dir, component.name))
            # repo = GitRepository(component.repository, 'main', os.path.join(work_dir, component.name))
            self._execute_integtest_sh(cluster, security)
        finally:
            cluster.destroy()

    def _execute_integtest_sh(self, cluster, security):
        script = self.script_finder.find_integ_test_script(self.component.name, self.repo.dir)
        if os.path.exists(script):
            self.repo.execute(
                f"{script} -b {cluster.endpoint()} -p {cluster.port()} -s {str(security).lower()}"
            )
        else:
            print(f"{script} does not exist. Skipping integ tests for {self.name}")
