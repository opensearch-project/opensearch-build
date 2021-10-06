import os
import tempfile
import unittest

from test_workflow.test_component import TestComponent


class TestTestComponent(unittest.TestCase):
    def setUp(self):
        self.test_component = TestComponent(
            "https://github.com/opensearch-project/.github",
            "8ac515431bf24caf92fea9d9b0af3b8f10b88453",
        )

    def test_checkout(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            subdir = os.path.join(tmpdir, ".github")
            repo = self.test_component.checkout(subdir)
            self.assertEqual(repo.url, "https://github.com/opensearch-project/.github")
            self.assertEqual(repo.ref, "8ac515431bf24caf92fea9d9b0af3b8f10b88453")
