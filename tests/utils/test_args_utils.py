import unittest
from unittest.mock import MagicMock, patch

from utils.args_utils import get_folder_name_from_build_name, get_output_dir


class ArgsUtilsTests(unittest.TestCase):

    def test_get_folder_name_from_build_name(self):
        self.assertEqual(get_folder_name_from_build_name("OpenSearch"), "opensearch")
        self.assertEqual(get_folder_name_from_build_name("OpenSearch Dashboards"), "opensearch-dashboards")

    @patch("utils.args_utils.os")
    def test_get_output_dir(self, mock_os):

        mock_cwd = MagicMock()

        mock_os.getcwd.return_value = mock_cwd

        get_output_dir("builds", "OpenSearch")

        mock_os.path.join.called_once(
            mock_cwd,
            "builds",
            get_folder_name_from_build_name("OpenSearch")
        )
