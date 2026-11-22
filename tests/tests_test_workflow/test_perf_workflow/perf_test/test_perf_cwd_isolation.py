# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import json
import os
import shutil
import tempfile
import unittest
from unittest.mock import Mock, patch

from manifests.bundle_manifest import BundleManifest
from test_workflow.perf_test.perf_test_cluster_config import PerfTestClusterConfig
from test_workflow.perf_test.perf_test_suite import PerfTestSuite

from .test_perf_test_cluster import DummyPerfTestCluster


class TestPerfTestCwdIsolation(unittest.TestCase):
    """
    The perf test workflow must not move the process's working directory.

    The issue asks for every chdir to become an explicit cwd= argument.
    A chdir changes the directory for every thread in the process, so a
    library call that chdirs is an implicit global side effect; passing
    cwd= to subprocess keeps the same behavior locally and leaves the
    process where it was.
    """

    DATA = os.path.join(os.path.dirname(__file__), "data")
    BUNDLE_MANIFEST = os.path.join(DATA, "bundle_manifest.yml")

    def setUp(self) -> None:
        self.manifest = BundleManifest.from_path(self.BUNDLE_MANIFEST)
        self.config = {
            "Constants": {
                "SecurityGroupId": "sg-00000000",
                "VpcId": "vpc-12345",
                "AccountId": "12345678",
                "Region": "us-west-2",
                "Role": "role-arn",
            }
        }
        self.start_dir = os.getcwd()
        self.addCleanup(os.chdir, self.start_dir)

        self.workspace = os.path.realpath(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.workspace, True)
        self.work_dir = os.path.join(self.workspace, "test_dir")
        os.mkdir(self.work_dir)

    def _write_cdk_output(self) -> None:
        with open(os.path.join(self.work_dir, "output.json"), "w") as out:
            json.dump({"stack": {"PrivateIp": "10.10.10.10"}}, out)

    def test_cluster_start_does_not_change_process_cwd(self) -> None:
        self._write_cdk_output()
        cluster = DummyPerfTestCluster(
            bundle_manifest=self.manifest,
            config=self.config,
            stack_name="stack",
            cluster_config=PerfTestClusterConfig(security=True),
            current_workspace=self.workspace,
        )

        with patch("subprocess.check_call") as mock_check_call:
            with patch.object(cluster, "create_endpoint") as mock_create_endpoint:
                cluster.start()

        self.assertEqual(
            os.getcwd(),
            self.start_dir,
            "start() moved the process's working directory instead of "
            "running the command in work_dir",
        )
        self.assertEqual(mock_check_call.call_args.kwargs.get("cwd"), self.work_dir)
        # start() reads its CDK output relatively on main, so the chdir was
        # doing real work there. Reading it from work_dir is what keeps that
        # file reachable now that the process no longer moves.
        mock_create_endpoint.assert_called_once_with({"stack": {"PrivateIp": "10.10.10.10"}})

    def test_cluster_terminate_does_not_change_process_cwd(self) -> None:
        cluster = DummyPerfTestCluster(
            bundle_manifest=self.manifest,
            config=self.config,
            stack_name="stack",
            cluster_config=PerfTestClusterConfig(security=True),
            current_workspace=self.workspace,
        )

        with patch("subprocess.check_call") as mock_check_call:
            cluster.terminate()

        self.assertEqual(
            os.getcwd(),
            self.start_dir,
            "terminate() moved the process's working directory instead of "
            "running the command in work_dir",
        )
        self.assertEqual(mock_check_call.call_args.kwargs.get("cwd"), self.work_dir)

    def test_suite_execute_does_not_change_process_cwd(self) -> None:
        args = Mock()
        args.workload = "nyc_taxis"
        args.workload_options = "{}"
        args.warmup_iters = 0
        args.test_iters = 1
        suite = PerfTestSuite(
            bundle_manifest=self.manifest,
            endpoint="abc.com",
            security=False,
            current_workspace=self.workspace,
            test_results_path=os.path.join(self.workspace, "results"),
            args=args,
        )
        os.mkdir(os.path.join(self.workspace, "mensor"))

        with patch("subprocess.check_call") as mock_check_call:
            suite.execute()

        self.assertEqual(
            os.getcwd(),
            self.start_dir,
            "execute() left the process in "
            f"{os.getcwd()} instead of {self.start_dir}",
        )
        self.assertEqual(mock_check_call.call_count, 2)
        expected_cwd = os.path.realpath(os.path.join(self.workspace, "mensor"))
        for call in mock_check_call.call_args_list:
            # realpath, not a string compare: PerfTestSuite.work_dir is built as
            # current_workspace + "/mensor/" (perf_test_suite.py:43), so the
            # directory the chdir used to set carries a trailing slash. What
            # matters is the directory, and this PR must not change that
            # spelling, only stop the process from moving.
            self.assertEqual(os.path.realpath(call.kwargs.get("cwd")), expected_cwd)
