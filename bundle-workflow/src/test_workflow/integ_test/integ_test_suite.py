# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import glob
import logging
import os

from git.git_repository import GitRepository
from paths.script_finder import ScriptFinder
from system.execute import execute
from test_workflow.dependency_installer import DependencyInstaller
from test_workflow.integ_test.local_test_cluster import LocalTestCluster


class IntegTestSuite:
    """
    Kicks of integration tests for a component based on test configurations provided in
    test_support_matrix.yml
    """

    def __init__(self, component, test_config, bundle_manifest, build_manifest, work_dir, s3_bucket_name):
        self.component = component
        self.bundle_manifest = bundle_manifest
        self.build_manifest = build_manifest
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
        self.__install_build_dependencies()
        for config in self.test_config.integ_test["test-configs"]:
            security = self.__is_security_enabled(config)
            self.__setup_cluster_and_execute_test_config(security)

    def __install_build_dependencies(self):
        if 'build-dependencies' in self.test_config.integ_test:
            dependency_list = self.test_config.integ_test['build-dependencies']
            if len(dependency_list) == 1 and 'job-scheduler' in dependency_list:
                self.__copy_job_scheduler_artifact()
            else:
                raise InvalidTestConfigError(
                    'Integration test job only supports job-scheduler build dependency at present.')

    def __copy_job_scheduler_artifact(self):
        custom_local_path = os.path.join(self.repo.dir, 'src/test/resources/job-scheduler')
        for file in glob.glob(custom_local_path + '/opensearch-job-scheduler-*.zip'):
            os.unlink(file)
        version = None
        for component in self.build_manifest.components:
            if component.name == 'job-scheduler':
                version = component.version
                break
        if version:
            DependencyInstaller(self.build_manifest.build).install_build_dependencies(
                {'opensearch-job-scheduler': version}, custom_local_path)
        else:
            raise MissingArtifactError('job-scheduler not found in build manifest.yml')

    @staticmethod
    def __is_security_enabled(config):
        if config in ['with-security', 'without-security']:
            return True if config == 'with-security' else False
        else:
            raise InvalidTestConfigError('Unsupported test config: ' + config)

    def __setup_cluster_and_execute_test_config(self, security):
        with LocalTestCluster.create(self.work_dir, self.bundle_manifest, security, self.s3_bucket_name) as (test_cluster_endpoint, test_cluster_port):
            self.__pretty_print_message("Running integration tests for " + self.component.name)
            os.chdir(self.work_dir)
            self.__execute_integtest_sh(test_cluster_endpoint, test_cluster_port, security)

    def __execute_integtest_sh(self, endpoint, port, security):
        script = self.script_finder.find_integ_test_script(
            self.component.name, self.repo.dir
        )
        if os.path.exists(script):
            cmd = f"{script} -b {endpoint} -p {port} -s {str(security).lower()} -v {self.bundle_manifest.build.version}"
            work_dir = os.path.join(self.repo.dir,
                                    self.test_config.working_directory) if self.test_config.working_directory is not None else self.repo.dir
            (status, stdout, stderr) = execute(cmd, work_dir, True, False)
            if stderr:
                logging.info("Integration test run failed for component " + self.component.name)
                logging.info(stderr)
        else:
            logging.info(
                f"{script} does not exist. Skipping integ tests for {self.name}"
            )

    @staticmethod
    def __pretty_print_message(message):
        logging.info("===============================================")
        logging.info(message)
        logging.info("===============================================")


class MissingArtifactError(Exception):
    pass


class InvalidTestConfigError(Exception):
    pass
