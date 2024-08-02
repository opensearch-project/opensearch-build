import os
import unittest
from unittest.mock import Mock, patch

from test_workflow.benchmark_test.benchmark_test_suite_compare import BenchmarkTestSuiteCompare


class TestBenchmarkTestSuiteCompare(unittest.TestCase):

    def setUp(self) -> None:
        self.args = Mock()
        self.args.command = "compare"
        self.args.stack_suffix = "test-suffix"
        self.args.baseline = "baseline-id"
        self.args.contender = "contender-id"
        self.args.results_format = "markdown"
        self.args.results_numbers_align = "right"
        self.args.results_file = "~/results/comparison.md"
        self.args.show_in_results = "all"

    def test_form_command(self) -> None:
        expected_command = (
            f'docker run --name docker-container-{self.args.stack_suffix} '
            '-v ~/.benchmark/benchmark.ini:/opensearch-benchmark/.benchmark/benchmark.ini '
            'opensearchproject/opensearch-benchmark:1.6.0 '
            f'compare --baseline={self.args.baseline} --contender={self.args.contender} '
            f'--results-format={self.args.results_format} '
            f'--results-numbers-align={self.args.results_numbers_align} '
            '--results-file=final_result.md '
            f'--show-in-results={self.args.show_in_results} '
        )

        with patch('test_workflow.benchmark_test.benchmark_test_suite_compare.BenchmarkTestSuiteCompare.form_command') as mock_form_command:
            mock_form_command.return_value = expected_command
            compare = BenchmarkTestSuiteCompare(self.args)
            command = compare.form_command()
            self.assertEqual(command, expected_command)

    @patch('subprocess.check_call')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_compare.BenchmarkTestSuiteCompare.copy_comparison_results_to_local')
    @patch('test_workflow.benchmark_test.benchmark_test_suite_compare.BenchmarkTestSuiteCompare.cleanup')
    def test_execute(self, mock_cleanup: Mock, mock_copy_results: Mock, mock_check_call: Mock) -> None:
        compare = BenchmarkTestSuiteCompare(self.args)
        compare.execute()
        mock_check_call.assert_called_once()
        mock_copy_results.assert_called_once()
        mock_cleanup.assert_called_once()

    @patch('subprocess.check_call')
    @patch('glob.glob')
    @patch('shutil.copy')
    @patch('os.path.isdir')
    @patch('os.path.expanduser')
    def test_copy_comparison_results_to_local(self, mock_expanduser: Mock, mock_isdir: Mock, mock_shutil_copy: Mock, mock_glob: Mock, mock_check_call: Mock) -> None:
        compare = BenchmarkTestSuiteCompare(self.args)
        mock_isdir.return_value = True
        mock_glob.return_value = ['/tmp/final_result.md']
        mock_expanduser.return_value = '/home/user/results/comparison.md'
        normalized_path = os.path.normpath(mock_expanduser.return_value)

        with patch('test_workflow.benchmark_test.benchmark_test_suite_compare.TemporaryDirectory') as mock_temp_dir:
            mock_temp_dir.return_value.__enter__.return_value.path = '/tmp'
            compare.copy_comparison_results_to_local()

        mock_check_call.assert_called_once()
        mock_glob.assert_called_once_with(os.path.join('/tmp', 'final_result.md'))
        mock_shutil_copy.assert_called_once_with('/tmp/final_result.md', normalized_path)

    def test_from_args_compare(self) -> None:
        from test_workflow.benchmark_test.benchmark_test_suite_runners import BenchmarkTestSuiteRunners

        runner = BenchmarkTestSuiteRunners.from_args(self.args)

        self.assertIsInstance(runner, BenchmarkTestSuiteCompare)
        self.assertEqual(runner.args, self.args)


if __name__ == '__main__':
    unittest.main()
