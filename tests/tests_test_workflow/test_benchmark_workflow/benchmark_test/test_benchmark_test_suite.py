# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import unittest
from typing import Any
from unittest.mock import Mock, patch

from test_workflow.benchmark_test.benchmark_test_suite import BenchmarkTestSuite
from test_workflow.integ_test.utils import get_password


class TestBenchmarkTestSuite(unittest.TestCase):
    def setUp(self, **kwargs: Any) -> None:
        self.args = Mock()
        self.args.workload = "nyc_taxis"
        self.args.benchmark_config = kwargs['config'] if 'config' in kwargs else None
        self.args.user_tag = kwargs['tags'] if 'tags' in kwargs else None
        self.args.workload_params = kwargs['workload_params'] if 'workload_params' in kwargs else None
        self.args.telemetry = kwargs['telemetry'] if 'telemetry' in kwargs else None
        self.args.telemetry_params = kwargs['telemetry_params'] if 'telemetry_params' in kwargs else None
        self.args.test_procedure = kwargs['test_procedure'] if 'test_procedure' in kwargs else None
        self.args.exclude_tasks = kwargs['exclude_tasks'] if 'exclude_tasks' in kwargs else None
        self.args.include_tasks = kwargs['include_tasks'] if 'include_tasks' in kwargs else None
        self.endpoint = "abc.com"
        self.benchmark_test_suite = BenchmarkTestSuite(endpoint=self.endpoint, security=False, args=self.args, password=get_password('2.3.0'))

    def test_execute_default(self) -> None:
        with patch("subprocess.check_call") as mock_check_call:
            self.benchmark_test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 1)
            self.assertEqual(self.benchmark_test_suite.command,
                             'docker run --rm opensearchproject/opensearch-benchmark:latest execute-test --workload=nyc_taxis '
                             '--pipeline=benchmark-only --target-hosts=abc.com --client-options="timeout:300"')

    def test_execute_security_enabled_version_212_or_greater(self) -> None:
        benchmark_test_suite = BenchmarkTestSuite(endpoint=self.endpoint, security=True, args=self.args, password=get_password('2.12.0'))
        with patch("subprocess.check_call") as mock_check_call:
            benchmark_test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 1)
            self.assertEqual(benchmark_test_suite.command,
                             'docker run --rm opensearchproject/opensearch-benchmark:latest execute-test '
                             '--workload=nyc_taxis --pipeline=benchmark-only '
                             '--target-hosts=abc.com --client-options="timeout:300,use_ssl:true,'
                             'verify_certs:false,basic_auth_user:\'admin\',basic_auth_password:\'myStrongPassword123!\'"')

    def test_execute_security_enabled(self) -> None:
        benchmark_test_suite = BenchmarkTestSuite(endpoint=self.endpoint, security=True, args=self.args, password=get_password('2.3.0'))
        with patch("subprocess.check_call") as mock_check_call:
            benchmark_test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 1)
            self.assertEqual(benchmark_test_suite.command,
                             'docker run --rm opensearchproject/opensearch-benchmark:latest execute-test '
                             '--workload=nyc_taxis --pipeline=benchmark-only '
                             '--target-hosts=abc.com --client-options="timeout:300,use_ssl:true,'
                             'verify_certs:false,basic_auth_user:\'admin\',basic_auth_password:\'admin\'"')

    def test_execute_default_with_optional_args(self) -> None:
        TestBenchmarkTestSuite.setUp(self, config="/home/test/benchmark.ini", tags="key1:value1,key2:value2",
                                     workload_params="{\"number_of_replicas\":\"1\"}", telemetry=['node-stats', 'test'],
                                     telemetry_params="{\"example_key\":\"example_value\"}")
        with patch("subprocess.check_call") as mock_check_call:
            self.benchmark_test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 1)
            self.assertEqual(self.benchmark_test_suite.command, 'docker run --rm -v /home/test/benchmark.ini:'
                                                                '/opensearch-benchmark/.benchmark/benchmark.ini '
                                                                'opensearchproject/opensearch-benchmark:latest execute-test '
                                                                '--workload=nyc_taxis '
                                                                '--pipeline=benchmark-only --target-hosts=abc.com '
                                                                '--workload-params \'{"number_of_replicas":"1"}\' '
                                                                '--user-tag="key1:value1,key2:value2" --telemetry node-stats,test, --telemetry-params \'{"example_key":"example_value"}\' '
                                                                '--client-options="timeout:300"')

    def test_execute_default_with_no_telemetry_params(self) -> None:
        TestBenchmarkTestSuite.setUp(self, config="/home/test/benchmark.ini", tags="key1:value1,key2:value2",
                                     workload_params="{\"number_of_replicas\":\"1\"}", telemetry=['node-stats', 'test'])
        with patch("subprocess.check_call") as mock_check_call:
            self.benchmark_test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 1)
            self.assertEqual(self.benchmark_test_suite.command, 'docker run --rm -v /home/test/benchmark.ini:'
                                                                '/opensearch-benchmark/.benchmark/benchmark.ini '
                                                                'opensearchproject/opensearch-benchmark:latest execute-test '
                                                                '--workload=nyc_taxis '
                                                                '--pipeline=benchmark-only --target-hosts=abc.com '
                                                                '--workload-params \'{"number_of_replicas":"1"}\' '
                                                                '--user-tag="key1:value1,key2:value2" --telemetry node-stats,test, '
                                                                '--client-options="timeout:300"')

    def test_execute_with_test_procedure_params(self) -> None:
        TestBenchmarkTestSuite.setUp(self, config="/home/test/benchmark.ini", tags="key1:value1,key2:value2",
                                     workload_params="{\"number_of_replicas\":\"1\"}", test_procedure="test-proc1,test-proc2")
        with patch("subprocess.check_call") as mock_check_call:
            self.benchmark_test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 1)
            self.assertEqual(self.benchmark_test_suite.command, 'docker run --rm -v /home/test/benchmark.ini:'
                                                                '/opensearch-benchmark/.benchmark/benchmark.ini '
                                                                'opensearchproject/opensearch-benchmark:latest execute-test '
                                                                '--workload=nyc_taxis '
                                                                '--pipeline=benchmark-only --target-hosts=abc.com '
                                                                '--workload-params \'{"number_of_replicas":"1"}\' '
                                                                '--test-procedure="test-proc1,test-proc2" '
                                                                '--user-tag="key1:value1,key2:value2" '
                                                                '--client-options="timeout:300"')

    def test_execute_with_include_exclude_params(self) -> None:
        TestBenchmarkTestSuite.setUp(self, config="/home/test/benchmark.ini", tags="key1:value1,key2:value2",
                                     workload_params="{\"number_of_replicas\":\"1\"}", include_tasks="task1,type:index",
                                     exclude_tasks="task2,type:search")
        with patch("subprocess.check_call") as mock_check_call:
            self.benchmark_test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 1)
            self.assertEqual(self.benchmark_test_suite.command, 'docker run --rm -v /home/test/benchmark.ini:'
                                                                '/opensearch-benchmark/.benchmark/benchmark.ini '
                                                                'opensearchproject/opensearch-benchmark:latest execute-test '
                                                                '--workload=nyc_taxis '
                                                                '--pipeline=benchmark-only --target-hosts=abc.com '
                                                                '--workload-params \'{"number_of_replicas":"1"}\' '
                                                                '--exclude-tasks="task2,type:search" '
                                                                '--include-tasks="task1,type:index" '
                                                                '--user-tag="key1:value1,key2:value2" '
                                                                '--client-options="timeout:300"')

    def test_execute_with_all_benchmark_optional_params(self) -> None:
        TestBenchmarkTestSuite.setUp(self, config="/home/test/benchmark.ini", tags="key1:value1,key2:value2",
                                     workload_params="{\"number_of_replicas\":\"1\"}", test_procedure="test-proc1,test-proc2",
                                     include_tasks="task1,type:index", exclude_tasks="task2,type:search")
        with patch("subprocess.check_call") as mock_check_call:
            self.benchmark_test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 1)
            self.assertEqual(self.benchmark_test_suite.command, 'docker run --rm -v /home/test/benchmark.ini:'
                                                                '/opensearch-benchmark/.benchmark/benchmark.ini '
                                                                'opensearchproject/opensearch-benchmark:latest execute-test '
                                                                '--workload=nyc_taxis '
                                                                '--pipeline=benchmark-only --target-hosts=abc.com '
                                                                '--workload-params \'{"number_of_replicas":"1"}\' '
                                                                '--test-procedure="test-proc1,test-proc2" '
                                                                '--exclude-tasks="task2,type:search" '
                                                                '--include-tasks="task1,type:index" '
                                                                '--user-tag="key1:value1,key2:value2" '
                                                                '--client-options="timeout:300"')
