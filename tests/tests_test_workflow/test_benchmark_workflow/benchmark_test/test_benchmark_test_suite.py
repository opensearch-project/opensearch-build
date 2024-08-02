# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

import os
import tempfile
import unittest
from typing import Any
from unittest.mock import MagicMock, Mock, patch

from test_workflow.benchmark_test.benchmark_test_suite_execute import BenchmarkTestSuiteExecute
from test_workflow.integ_test.utils import get_password


class TestBenchmarkTestSuite(unittest.TestCase):
    def setUp(self, **kwargs: Any) -> None:
        with patch('test_workflow.integ_test.utils.get_password') as mock_get_password:
            self.args = Mock()
            self.args.command = 'execute-test'
            self.args.insecure = True
            self.args.workload = "nyc_taxis"
            self.args.version = '2.9.0'
            self.args.benchmark_config = kwargs['config'] if 'config' in kwargs else None
            mock_get_password.return_value = get_password('2.11.0')
            self.args.username = "admin"
            self.password = "myStrongPassword123!"
            self.args.cluster_endpoint = None
            self.args.user_tag = kwargs['tags'] if 'tags' in kwargs else None
            self.args.workload_params = kwargs['workload_params'] if 'workload_params' in kwargs else None
            self.args.telemetry = kwargs['telemetry'] if 'telemetry' in kwargs else None
            self.args.telemetry_params = kwargs['telemetry_params'] if 'telemetry_params' in kwargs else None
            self.args.test_procedure = kwargs['test_procedure'] if 'test_procedure' in kwargs else None
            self.args.exclude_tasks = kwargs['exclude_tasks'] if 'exclude_tasks' in kwargs else None
            self.args.include_tasks = kwargs['include_tasks'] if 'include_tasks' in kwargs else None
            self.endpoint = "abc.com"

    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.subprocess.check_call')
    def test_execute_default(self, mock_check_call: Mock) -> None:

        self.args.insecure = True
        mock_check_call.return_value = 0
        mock_convert = MagicMock()
        with patch.object(BenchmarkTestSuiteExecute, 'convert', mock_convert):
            test_suite = BenchmarkTestSuiteExecute("abc.com:80", False, self.args, "")
            test_suite.execute()
        self.assertEqual(mock_check_call.call_count, 2)
        self.assertEqual(test_suite.command,
                         f'docker run --name docker-container-{test_suite.args.stack_suffix} opensearchproject/opensearch-benchmark:1.6.0 execute-test '
                         f'--workload=nyc_taxis --pipeline=benchmark-only --target-hosts=abc.com:80 --client-options="timeout:300" --results-file=final_result.md')

    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.subprocess.check_call')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.BenchmarkTestSuiteExecute.convert')
    def test_execute_security_enabled_version_212_or_greater(self, mock_convert: Mock, mock_check_call: Mock) -> None:
        mock_check_call.return_value = 0
        self.args.insecure = False
        test_suite = BenchmarkTestSuiteExecute("abc.com:443", True, self.args, self.password)
        test_suite.execute()
        self.assertEqual(mock_check_call.call_count, 2)
        mock_check_call.assert_called_with(
            f"docker rm -f docker-container-{test_suite.args.stack_suffix}", cwd=os.getcwd(), shell=True)
        self.assertEqual(test_suite.command,
                         f'docker run --name docker-container-{test_suite.args.stack_suffix} opensearchproject/opensearch-benchmark:1.6.0 execute-test'
                         f' --workload=nyc_taxis --pipeline=benchmark-only '
                         f'--target-hosts=abc.com:443 '
                         f'--client-options="timeout:300,use_ssl:true,verify_certs:false,basic_auth_user:\'admin\',basic_auth_password:\'myStrongPassword123!\'" --results-file=final_result.md')

    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.subprocess.check_call')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.BenchmarkTestSuiteExecute.convert')
    def test_execute_security_enabled(self, mock_convert: Mock, mock_check_call: Mock) -> None:
        mock_check_call.return_value = 0
        self.args.insecure = True
        test_suite = BenchmarkTestSuiteExecute("abc.com:443", True, self.args, "admin")
        test_suite.execute()
        self.assertEqual(mock_check_call.call_count, 2)
        mock_check_call.assert_called_with(
            f"docker rm -f docker-container-{test_suite.args.stack_suffix}", cwd=os.getcwd(), shell=True)
        self.assertEqual(test_suite.command,
                         f'docker run --name docker-container-{test_suite.args.stack_suffix} opensearchproject/opensearch-benchmark:1.6.0 execute-test '
                         '--workload=nyc_taxis --pipeline=benchmark-only '
                         '--target-hosts=abc.com:443 --client-options="timeout:300,use_ssl:true,'
                         'verify_certs:false,basic_auth_user:\'admin\',basic_auth_password:\'admin\'" --results-file=final_result.md')

    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.subprocess.check_call')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.BenchmarkTestSuiteExecute.convert')
    def test_execute_default_with_optional_args(self, mock_convert: Mock, mock_check_call: Mock) -> None:
        mock_check_call.return_value = 0
        self.args.telemetry = []
        self.args.telemetry.append('node-stats')
        TestBenchmarkTestSuite.setUp(self, config="/home/test/benchmark.ini", tags="key1:value1,key2:value2",
                                     workload_params="{\"number_of_replicas\":\"1\"}", telemetry=['node-stats'],
                                     telemetry_params="{\"example_key\":\"example_value\"}")
        test_suite = BenchmarkTestSuiteExecute("abc.com:80", False, self.args, "")
        test_suite.execute()
        self.assertEqual(mock_check_call.call_count, 2)
        mock_check_call.assert_called_with(
            f"docker rm -f docker-container-{test_suite.args.stack_suffix}", cwd=os.getcwd(), shell=True)
        self.assertEqual(test_suite.command,
                         f'docker run --name docker-container-{test_suite.args.stack_suffix} -v /home/test/benchmark.ini:'
                         '/opensearch-benchmark/.benchmark/benchmark.ini '
                         'opensearchproject/opensearch-benchmark:1.6.0 execute-test '
                         '--workload=nyc_taxis '
                         '--pipeline=benchmark-only --target-hosts=abc.com:80 '
                         '--workload-params \'{"number_of_replicas":"1"}\' '
                         '--user-tag="key1:value1,key2:value2" --telemetry node-stats, --telemetry-params \'{"example_key":"example_value"}\' '
                         '--client-options="timeout:300" --results-file=final_result.md')

    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.subprocess.check_call')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.BenchmarkTestSuiteExecute.convert')
    def test_execute_default_with_no_telemetry_params(self, mock_convert: Mock, mock_check_call: Mock) -> None:
        mock_check_call.return_value = 0
        TestBenchmarkTestSuite.setUp(self, config="/home/test/benchmark.ini", tags="key1:value1,key2:value2",
                                     workload_params="{\"number_of_replicas\":\"1\"}", telemetry=['node-stats', 'test'])
        test_suite = BenchmarkTestSuiteExecute("abc.com:80", False, self.args, "")
        test_suite.execute()
        self.assertEqual(mock_check_call.call_count, 2)
        mock_check_call.assert_called_with(
            f"docker rm -f docker-container-{test_suite.args.stack_suffix}", cwd=os.getcwd(), shell=True)
        self.assertEqual(test_suite.command,
                         f'docker run --name docker-container-{test_suite.args.stack_suffix} -v /home/test/benchmark.ini:'
                         '/opensearch-benchmark/.benchmark/benchmark.ini '
                         'opensearchproject/opensearch-benchmark:1.6.0 execute-test '
                         '--workload=nyc_taxis '
                         '--pipeline=benchmark-only --target-hosts=abc.com:80 '
                         '--workload-params \'{"number_of_replicas":"1"}\' '
                         '--user-tag="key1:value1,key2:value2" --telemetry node-stats,test, '
                         '--client-options="timeout:300" --results-file=final_result.md')

    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.subprocess.check_call')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.BenchmarkTestSuiteExecute.convert')
    def test_execute_with_test_procedure_params(self, mock_convert: Mock, mock_check_call: Mock) -> None:
        mock_check_call.return_value = 0
        self.args.insecure = True
        TestBenchmarkTestSuite.setUp(self, config="/home/test/benchmark.ini", tags="key1:value1,key2:value2",
                                     workload_params="{\"number_of_replicas\":\"1\"}", test_procedure="test-proc1,test-proc2")
        test_suite = BenchmarkTestSuiteExecute("abc.com:80", False, self.args, "")
        test_suite.execute()
        self.assertEqual(mock_check_call.call_count, 2)
        mock_check_call.assert_called_with(
            f"docker rm -f docker-container-{test_suite.args.stack_suffix}", cwd=os.getcwd(), shell=True)
        self.assertEqual(test_suite.command,
                         f'docker run --name docker-container-{test_suite.args.stack_suffix} -v /home/test/benchmark.ini:'
                         '/opensearch-benchmark/.benchmark/benchmark.ini '
                         'opensearchproject/opensearch-benchmark:1.6.0 execute-test '
                         '--workload=nyc_taxis '
                         '--pipeline=benchmark-only --target-hosts=abc.com:80 '
                         '--workload-params \'{"number_of_replicas":"1"}\' '
                         '--test-procedure="test-proc1,test-proc2" '
                         '--user-tag="key1:value1,key2:value2" '
                         '--client-options="timeout:300" --results-file=final_result.md')

    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.subprocess.check_call')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.BenchmarkTestSuiteExecute.convert')
    def test_execute_with_include_exclude_params(self, mock_convert: Mock, mock_check_call: Mock) -> None:
        mock_check_call.return_value = 0
        self.args.insecure = True
        TestBenchmarkTestSuite.setUp(self, config="/home/test/benchmark.ini", tags="key1:value1,key2:value2",
                                     workload_params="{\"number_of_replicas\":\"1\"}", include_tasks="task1,type:index",
                                     exclude_tasks="task2,type:search")
        test_suite = BenchmarkTestSuiteExecute("abc.com:80", False, self.args, "")
        test_suite.execute()
        self.assertEqual(mock_check_call.call_count, 2)
        mock_check_call.assert_called_with(
            f"docker rm -f docker-container-{test_suite.args.stack_suffix}", cwd=os.getcwd(), shell=True)
        self.assertEqual(test_suite.command,
                         f'docker run --name docker-container-{test_suite.args.stack_suffix} -v /home/test/benchmark.ini:'
                         '/opensearch-benchmark/.benchmark/benchmark.ini '
                         'opensearchproject/opensearch-benchmark:1.6.0 execute-test '
                         '--workload=nyc_taxis '
                         '--pipeline=benchmark-only --target-hosts=abc.com:80 '
                         '--workload-params \'{"number_of_replicas":"1"}\' '
                         '--exclude-tasks="task2,type:search" '
                         '--include-tasks="task1,type:index" '
                         '--user-tag="key1:value1,key2:value2" '
                         '--client-options="timeout:300" --results-file=final_result.md')

    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.BenchmarkTestSuiteExecute.convert')
    def test_execute_with_all_benchmark_optional_params(self, mock_convert: Mock) -> None:
        self.args.insecure = True
        TestBenchmarkTestSuite.setUp(self, config="/home/test/benchmark.ini", tags="key1:value1,key2:value2",
                                     workload_params="{\"number_of_replicas\":\"1\"}", test_procedure="test-proc1,test-proc2",
                                     include_tasks="task1,type:index", exclude_tasks="task2,type:search")
        with patch("subprocess.check_call") as mock_check_call:
            test_suite = BenchmarkTestSuiteExecute("abc.com:80", False, self.args, "")
            test_suite.execute()
            self.assertEqual(mock_check_call.call_count, 2)
            mock_check_call.assert_called_with(
                f"docker rm -f docker-container-{test_suite.args.stack_suffix}", cwd=os.getcwd(), shell=True)
            self.assertEqual(test_suite.command, f'docker run --name docker-container-{test_suite.args.stack_suffix} -v /home/test/benchmark.ini:'
                                                 '/opensearch-benchmark/.benchmark/benchmark.ini '
                                                 'opensearchproject/opensearch-benchmark:1.6.0 execute-test '
                                                 '--workload=nyc_taxis '
                                                 '--pipeline=benchmark-only --target-hosts=abc.com:80 '
                                                 '--workload-params \'{"number_of_replicas":"1"}\' '
                                                 '--test-procedure="test-proc1,test-proc2" '
                                                 '--exclude-tasks="task2,type:search" '
                                                 '--include-tasks="task1,type:index" '
                                                 '--user-tag="key1:value1,key2:value2" '
                                                 '--client-options="timeout:300" --results-file=final_result.md')

    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.subprocess.check_call')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.BenchmarkTestSuiteExecute.convert')
    def test_execute_cluster_endpoint(self, mock_convert: Mock, mock_check_call: Mock) -> None:
        mock_check_call.return_value = 0
        self.args.cluster_endpoint = "abc.com"
        self.args.insecure = True
        test_suite = BenchmarkTestSuiteExecute("abc.com:443", True, self.args, "admin")
        test_suite.execute()
        self.assertEqual(mock_check_call.call_count, 2)
        self.assertEqual(mock_convert.call_count, 1)
        mock_check_call.assert_called_with(
            f"docker rm -f docker-container-{test_suite.args.stack_suffix}", cwd=os.getcwd(), shell=True)
        self.assertEqual(test_suite.command,
                         f'docker run --name docker-container-{test_suite.args.stack_suffix} opensearchproject/opensearch-benchmark:1.6.0 execute-test '
                         '--workload=nyc_taxis --pipeline=benchmark-only '
                         '--target-hosts=abc.com:443 --client-options="timeout:300,use_ssl:true,'
                         'verify_certs:false,basic_auth_user:\'admin\',basic_auth_password:\'admin\'" --results-file=final_result.md')

    @patch('pandas.json_normalize')
    @patch('pandas.read_csv')
    @patch('json.load')
    @patch('builtins.open')
    @patch('logging.info')
    @patch('shutil.get_terminal_size')
    @patch('shutil.copy')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_execute.subprocess.check_call')
    def test_convert(self, mock_check_call: Mock, mock_copy: Mock, mock_get_terminal_size: Mock, mock_logging_info: Mock, mock_open: Mock, mock_json_load: Mock, mock_read_csv: Mock,
                     mock_json_normalize: Mock) -> None:
        self.args.cluster_endpoint = "abc.com"
        mock_get_terminal_size.return_value = MagicMock(columns=80)
        mock_open.return_value = MagicMock()
        mock_json_load.return_value = {"results": {"op_metrics": [{"metric": "value"}]}}
        mock_json_normalize.return_value = MagicMock()
        mock_read_csv.return_value = MagicMock()

        test_suite = BenchmarkTestSuiteExecute("abc.com:80", False, self.args, "")
        with patch('test_workflow.benchmark_test.benchmark_test_suite_execute.TemporaryDirectory') as mock_temp_directory:
            mock_temp_directory.return_value.__enter__.return_value.name = tempfile.gettempdir()
            mock_temp_directory.return_value.__enter__.return_value.path = '/mock/temp/dir'
            with patch('test_workflow.benchmark_test.benchmark_test_suite_execute.glob.glob') as mock_glob:
                mock_glob.return_value = ['/mock/test_execution.json', '/mock/final_result.md']
                test_suite.convert()
                mock_temp_directory.assert_called_once()
            mock_check_call.assert_any_call(f"docker cp docker-container-{test_suite.args.stack_suffix}:opensearch-benchmark/test_executions/. /mock/temp/dir", cwd=os.getcwd(), shell=True)
            mock_check_call.assert_any_call(f"docker cp docker-container-{test_suite.args.stack_suffix}:opensearch-benchmark/final_result.md /mock/temp/dir", cwd=os.getcwd(), shell=True)

            mock_open.assert_called_once_with("/mock/test_execution.json")
            mock_json_load.assert_called_once()
            mock_json_normalize.assert_called_once()
            mock_read_csv.assert_called_once()
            mock_logging_info.assert_called()
