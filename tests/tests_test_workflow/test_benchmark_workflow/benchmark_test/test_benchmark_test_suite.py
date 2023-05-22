# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from typing import Optional
from unittest.mock import Mock, patch

from test_workflow.benchmark_test.benchmark_test_suite import BenchmarkTestSuite


class TestBenchmarkTestSuite(unittest.TestCase):
    def setUp(self, config: Optional[str] = None, tag: Optional[str] = None,
              workload_params: Optional[str] = None, telemetry: Optional[bool] = None) -> None:
        self.args = Mock()
        self.args.workload = "nyc_taxis"
        self.args.benchmark_config = config
        self.args.user_tag = tag
        self.args.workload_params = workload_params
        self.args.capture_node_stat = telemetry
        self.endpoint = "abc.com"
        self.benchmark_test_suite = BenchmarkTestSuite(endpoint=self.endpoint, security=False, args=self.args)

    def test_execute_default(self) -> None:
        with patch("subprocess.check_call") as mock_check_call:
            self.benchmark_test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 1)
            self.assertEqual(self.benchmark_test_suite.command,
                             'docker run --rm opensearchproject/opensearch-benchmark:latest execute-test --workload=nyc_taxis '
                             '--pipeline=benchmark-only --target-hosts=abc.com')

    def test_execute_security_enabled(self) -> None:
        benchmark_test_suite = BenchmarkTestSuite(endpoint=self.endpoint, security=True, args=self.args)
        with patch("subprocess.check_call") as mock_check_call:
            benchmark_test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 1)
            self.assertEqual(benchmark_test_suite.command,
                             'docker run --rm opensearchproject/opensearch-benchmark:latest execute-test '
                             '--workload=nyc_taxis --pipeline=benchmark-only '
                             '--target-hosts=abc.com --client-options="use_ssl:true,'
                             'verify_certs:false,basic_auth_user:\'admin\',basic_auth_password:\'admin\'"')

    def test_execute_default_with_optional_args(self) -> None:
        TestBenchmarkTestSuite.setUp(self, "/home/test/benchmark.ini", "key1:value1,key2:value2", "number_of_replicas:1", True)
        with patch("subprocess.check_call") as mock_check_call:
            self.benchmark_test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 1)
            self.assertEqual(self.benchmark_test_suite.command, 'docker run --rm -v /home/test/benchmark.ini:'
                                                                '/opensearch-benchmark/.benchmark/benchmark.ini '
                                                                'opensearchproject/opensearch-benchmark:latest execute-test '
                                                                '--workload=nyc_taxis '
                                                                '--pipeline=benchmark-only --target-hosts=abc.com '
                                                                '--workload-params "number_of_replicas:1" '
                                                                '--user-tag="key1:value1,key2:value2" --telemetry node-stats')
